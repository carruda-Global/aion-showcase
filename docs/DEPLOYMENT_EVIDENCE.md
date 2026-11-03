# Deployment evidence

Reproduce any line below yourself.

| What | Command | Expected |
|---|---|---|
| Marketing site | `curl -s -o /dev/null -w "%{http_code}" https://aion.global` | 200 |
| Ecosystem page | `curl -s -o /dev/null -w "%{http_code}" https://global-engenharia.com/ecosystem` | 200 |
| Voice receptionist site (demo line on the page) | `curl -s -o /dev/null -w "%{http_code}" https://aionreceptionist.com` | 200, valid TLS |
| Backend | `curl -s -o /dev/null -w "%{http_code}" https://engenheiro-producao-ai.onrender.com/` | 200 |
| API documentation | `curl -s https://engenheiro-producao-ai.onrender.com/openapi.json` | versioned OpenAPI document listing every agent endpoint |

Deploy: Docker on Render with a persistent disk. Scheduled health checks and content jobs run on GitHub Actions.
