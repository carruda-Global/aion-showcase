# Deployment evidence (checked 2026-11-03)

Reproduce any line below yourself.

| Check | Command | Result on 2026-11-03 |
|---|---|---|
| Marketing site | `curl -s -o /dev/null -w "%{http_code}" https://aion.global` | 200 |
| Ecosystem page | `curl -s -o /dev/null -w "%{http_code}" https://global-engenharia.com/ecosystem` | 200 |
| Voice receptionist site | `curl -s -o /dev/null -w "%{http_code}" https://aionreceptionist.com` | 200, valid TLS |
| API root | `curl -s -o /dev/null -w "%{http_code}" https://engenheiro-producao-ai.onrender.com/` | 200 |
| API surface | `curl -s https://engenheiro-producao-ai.onrender.com/openapi.json` | version `7.0.0`, 346 paths |
| Voice agent endpoints | filter the OpenAPI paths for `/api/voice-agent` | 21 endpoints (provision, Vapi webhook, calls, dashboard, billing, knowledge) |
| Real call cost | `GET /api/voice-agent/billing/cost-per-minute` | 30-day window: 2 calls, 1.8 min, US$ 0.074/min (small sample) |
| Customers | `GET /api/voice-agent/billing/customer-count` | 1 active customer (pilot stage) |

## Codebase facts (private repo, counts from the working tree)

- ~130 commits; ~110 agent modules, ~50 routers, ~35 security modules, 41 test files.
- GitHub Actions: system health (daily + pulse), scheduled content jobs.
- Deploy: Docker on Render with a persistent disk.

## Scheduled content agent (observed)

The LinkedIn agent log shows consecutive weekdays with the three text-post slots (08h, 12h, 15h) published on schedule through 2026-10-06; the 17h carousel slot was failing until fixed (see the post-mortem).
