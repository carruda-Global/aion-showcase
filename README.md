# AION — multi-agent AI platform (engineering showcase)

AION is a multi-agent platform I designed and built end to end: LLM agents for regulatory compliance, engineering documentation, voice reception and autonomous sales outreach, exposed through a FastAPI backend with billing, audit trails and per-agent access control. It is a working, deployed system, not a scaled commercial operation.

This repository is a **curated, secret-free showcase**: architecture, real code excerpts, and evidence you can verify yourself. The full product repositories are private because they contain customer and commercial logic.

> Evidence below was checked on **2026-11-03** (see [docs/DEPLOYMENT_EVIDENCE.md](docs/DEPLOYMENT_EVIDENCE.md)).
> Every number here is something you can reproduce with one command. Where something is early-stage, it says so.

## What is deployed (verify it yourself)

| Claim | How to check |
|---|---|
| Backend is live, versioned, documented | `curl https://engenheiro-producao-ai.onrender.com/openapi.json` → **346 endpoints**, version `7.0.0` |
| Marketing site and product pages are live | https://aion.global · https://global-engenharia.com/ecosystem |
| Voice receptionist product is live | https://aionreceptionist.com (demo line on the page, no signup) |
| Real usage and cost telemetry are exposed | `GET /api/voice-agent/billing/cost-per-minute` and `/billing/customer-count` |
| Engineering history is real | ~130 commits, 41 test files, GitHub Actions for health checks and scheduled jobs |
| Honest maturity tracking | [docs/MATURITY.md](docs/MATURITY.md): which agents are verified end to end, which are not |

## What it does

- **Compliance agents (19 product modules tested end to end in July 2026):** SOC 2, ISO 27001, EU AI Act, CSRD double materiality, Whistleblower (EU 2019/1937), Carbon inventory (GHG Protocol), Scope 3, CBS/IBS tax reform, Pay Equity, Anti-Corruption, Vendor/Contract risk, NR-1 psychosocial.
- **Engineering agents:** project → document → photo → compliance pipeline that generates nine DOCX deliverables (including As-Built); a ten-specialist engineering suite.
- **AI Voice Receptionist:** Vapi telephony + LangGraph post-call pipeline (classification, extraction, summary, audit receipt). Pilot stage.
- **Autonomous LinkedIn sales machine:** scheduled content engine with a 200-variation topic×hook bank, engagement-weighted topic selection, tracked links, carousel PDF generation and publishing.
- **Maturity:** agents are tracked by level; only the tested subset is counted above. See the maturity doc.

## Design principles (the part I'd want a reviewer to read)

1. **The LLM never makes the decision that matters.** In the CSRD agent a fixed regulatory catalog drives the assessment; the model only answers narrow questions per catalog item, and a deterministic function computes materiality and the readiness score. → [examples/csrd_deterministic_agent.py](examples/csrd_deterministic_agent.py)
2. **Agents are graphs, not prompts.** The voice pipeline is a LangGraph graph with a concurrent fan-out and a dedicated compliance node that writes an audit receipt as its own concern. → [examples/voice_call_langgraph_excerpt.py](examples/voice_call_langgraph_excerpt.py)
3. **Governance is code.** Paywall/license checks per agent, ABAC/RBAC, PII masking, DLP, circuit breakers, cost kill-switch, and a tamper-evident Merkle audit chain (`src/security/`, ~35 modules). → [examples/merkle_audit_chain.py](examples/merkle_audit_chain.py)
4. **Run what you build.** Health-check workflows, cost-per-minute telemetry, and written post-mortems. → [docs/INCIDENT_LINKEDIN_AGENT.md](docs/INCIDENT_LINKEDIN_AGENT.md)

## Stack

Python 3.11/3.12 · FastAPI · LangGraph · DeepSeek (primary), Claude, Gemini · Supabase/PostgreSQL · Qdrant · Stripe · Vapi · Render · Docker · GitHub Actions · MCP · ReportLab.

## Where each capability lives

| Capability | Where to look |
|---|---|
| LLM agents and prompt design | `examples/csrd_deterministic_agent.py`, `examples/voice_call_langgraph_excerpt.py` |
| Multi-agent orchestration (LangGraph) | `examples/voice_call_langgraph_excerpt.py` |
| API integrations (LinkedIn Documents API, Stripe, Vapi) | `examples/linkedin_document_upload_excerpt.py`, `examples/linkedin_sales_machine.py` |
| Automation, scheduling, recovery | `examples/linkedin_sales_machine.py` (daily 4-slot scheduler, error back-off) |
| Evaluation and quality | deterministic scoring pattern (design principle 1); post-call classification |
| Security, quality and governance | design principle 3; `docs/MATURITY.md` |
| Metrics and adoption | `/billing/cost-per-minute`, `/billing/customer-count`, health workflows |

## What this is not

- No claim of production scale, revenue or customer traction. The voice receptionist has **one activated customer** and is in pilot.
- Not every listed agent is production-grade; the maturity doc separates verified from experimental.
- Some internal modules are scaffolds and are deliberately **not** included here.

## Contact

Cristiano Almeida Arruda — AI Engineer · [linkedin.com/in/cristiano-arruda](https://www.linkedin.com/in/cristiano-arruda) · São Paulo, Brazil
