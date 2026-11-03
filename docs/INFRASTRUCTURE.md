# Infraestrutura

## Em produção

| Camada | Como é feito |
|---|---|
| **Hospedagem** | Container Docker no Render, com disco persistente para os bancos locais |
| **Imagem** | Build em dois estágios: compila o backend Go em uma imagem Debian e roda em Python 3.12 com Node para o servidor de conhecimento |
| **Processos** | `docker-entrypoint.sh` sobe três processos juntos (servidor de conhecimento Node, backend Go e uvicorn/FastAPI) e derruba o contêiner se qualquer um morrer, em vez de rodar degradado |
| **Rede interna** | O FastAPI recebe o tráfego público e faz proxy reverso para o backend Go, que nunca é exposto diretamente |
| **Dados** | Supabase/PostgreSQL, Pinecone (memória semântica), SQLite local com recuperação de arquivo corrompido |
| **Cobrança** | Stripe e AbacatePay (PIX), com webhooks |
| **Telefonia** | Vapi, com webhook, métricas de custo por minuto e alertas de uso |
| **Jobs agendados** | GitHub Actions: health check diário e pulso de saúde, jobs de conteúdo; jobs internos no backend |
| **Observabilidade** | Verificação de saúde a cada 30 minutos e uma profunda por dia, log de execução por agente, alerta por e-mail, telemetria de custo, post-mortems escritos. Ver [Saúde e erros](HEALTH_AND_ERROR_REPORTING.md) |

## Preparado para escalar (manifestos e IaC no repositório)

- **Kubernetes:** namespace, configmap, ingress, deployment e conta de serviço do orquestrador, serviços MCP (ERP, ESG, Microsoft, regulatório), Redis e ChromaDB, registry de agentes e scripts de deploy.
- **Terraform:** projeto único com APIs, IAM e serviço.
- **Cloud Build** e **Docker Compose** para build e ambiente local.
- **Prometheus e Grafana:** configuração de coleta e painel de monitoramento dos agentes.

## Operação

- Configuração sensível por variável de ambiente nos serviços; manifestos de Kubernetes com placeholders.
- Health check e relatórios agendados detectam falhas silenciosas, como jobs que param de rodar.
- Problemas reais de infraestrutura já diagnosticados e corrigidos no histórico: roteamento da porta pública do serviço, recuperação de banco SQLite com WAL corrompido, crescimento ilimitado de histórico e falha silenciosa de job agendado.
