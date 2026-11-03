"""Brazilian-aware PII detection and masking. Document numbers are validated by checksum
to avoid masking arbitrary digit strings."""
import re
from typing import Callable

ALL_KINDS: tuple[str, ...] = ("cpf", "cnpj", "email", "phone", "card")

_CPF = re.compile(r"(?<!\d)(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})(?!\d)")
_CNPJ = re.compile(r"(?<!\d)(\d{2})\.?(\d{3})\.?(\d{3})/?(\d{4})-?(\d{2})(?!\d)")
_EMAIL = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,255}\.[A-Za-z]{2,}")
_PHONE = re.compile(r"(?<!\d)(?:\+55\s?)?(?:\(\d{2}\)\s?|\d{2}\s)9?\d{4}-\d{4}(?!\d)")
_CARD = re.compile(r"(?<!\d)(?<!\d[ -])\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}(?![ -]?\d)")

_CNPJ_W1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_CNPJ_W2 = (6,) + _CNPJ_W1


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def valid_cpf(value: str) -> bool:
    d = _digits(value)
    if len(d) != 11 or d == d[0] * 11:
        return False
    for n in (9, 10):
        total = sum(int(d[i]) * (n + 1 - i) for i in range(n))
        if (total * 10 % 11) % 10 != int(d[n]):
            return False
    return True


def valid_cnpj(value: str) -> bool:
    d = _digits(value)
    if len(d) != 14 or d == d[0] * 14:
        return False

    def check(base: str, weights: tuple[int, ...]) -> int:
        rest = sum(int(a) * b for a, b in zip(base, weights)) % 11
        return 0 if rest < 2 else 11 - rest

    return check(d[:12], _CNPJ_W1) == int(d[12]) and check(d[:13], _CNPJ_W2) == int(d[13])


def valid_card(value: str) -> bool:
    d = _digits(value)
    total = 0
    for i, ch in enumerate(reversed(d)):
        n = int(ch)
        if i % 2 == 1:
            n = n * 2 - 9 if n * 2 > 9 else n * 2
        total += n
    return len(d) >= 13 and total % 10 == 0


_DDDS = frozenset(
    "11 12 13 14 15 16 17 18 19 21 22 24 27 28 31 32 33 34 35 37 38 41 42 43 44 45 46 47 48 49 51 53 54 55 "
    "61 62 63 64 65 66 67 68 69 71 73 74 75 77 79 81 82 83 84 85 86 87 88 89 91 92 93 94 95 96 97 98 99".split()
)
_CPF_CONTEXT = ("cpf",)
_CARD_CONTEXT = ("cart", "card", "visa", "master")


def _cpf_ok(value: str, before: str) -> bool:
    formatted = "." in value or "-" in value
    return valid_cpf(value) and (formatted or any(k in before for k in _CPF_CONTEXT))


def _card_ok(value: str, before: str) -> bool:
    grouped = " " in value or "-" in value
    return valid_card(value) and (grouped or any(k in before for k in _CARD_CONTEXT))


def _phone_ok(value: str, before: str) -> bool:
    digits = _digits(value)
    if value.lstrip().startswith("+55"):
        digits = digits[2:]
    if digits[:2] not in _DDDS:
        return False
    first, second = digits[-8:-4], digits[-4:]
    looks_like_year_range = all(1900 <= int(part) <= 2100 for part in (first, second))
    return not looks_like_year_range


_RULES: dict[str, tuple[re.Pattern[str], Callable[[str, str], bool]]] = {
    "cnpj": (_CNPJ, lambda v, _b: valid_cnpj(v)),
    "cpf": (_CPF, _cpf_ok),
    "card": (_CARD, _card_ok),
    "email": (_EMAIL, lambda _v, _b: True),
    "phone": (_PHONE, _phone_ok),
}


def mask_pii(text: str, kinds: tuple[str, ...] = ALL_KINDS) -> tuple[str, dict[str, int]]:
    """Returns (masked_text, counts_by_kind). The input string is never modified."""
    counts: dict[str, int] = {}
    masked = text
    for kind, (pattern, is_valid) in _RULES.items():
        if kind not in kinds:
            continue

        def replace(match: re.Match[str], kind: str = kind, is_valid: Callable[[str, str], bool] = is_valid) -> str:
            before = match.string[max(0, match.start() - 24) : match.start()].lower()
            if not is_valid(match.group(0), before):
                return match.group(0)
            counts[kind] = counts.get(kind, 0) + 1
            return f"[{kind.upper()}]"

        masked = pattern.sub(replace, masked)
    return masked, counts


def find_pii(text: str, kinds: tuple[str, ...] = ALL_KINDS) -> dict[str, int]:
    return mask_pii(text, kinds)[1]
