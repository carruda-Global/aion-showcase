# Plugins e integrações de plataforma

Os mesmos agentes do [portfólio](AGENT_PORTFOLIO.md) são empacotados para chegar ao usuário dentro das ferramentas que ele já usa. Esta página descreve **os artefatos construídos**; o status de cada listagem (em revisão, publicada) está no guia do marketplace correspondente.

| Plataforma | O que foi construído | Onde fica |
|---|---|---|
| **Microsoft** (Teams, Copilot, Dynamics 365, Power BI) | Agentes para o ecossistema Microsoft (analista regulatório, PM de compliance, agentes de canal, conhecimento e facilitação, experiência de desenvolvedor), agentes Dynamics 365 (vendas, finanças, cadeia de suprimentos, RH, atendimento) e microagentes para Teams (monitor de risco, atas de reunião); servidor MCP de referência | `src/mcp/microsoft_server.py`, [portfólio](AGENT_PORTFOLIO.md) |
| **Salesforce** (Agentforce, AppExchange) | Agentes Agentforce (SDR, serviço em campo, inteligência de contratos e receita, sustentabilidade), pacote gerenciado e ferramenta de revisão de segurança | `salesforce-package/`, `marketplace-integration/salesforce/` |
| **Google Cloud** | Criação de oferta no Marketplace por API e guia de publicação; Gemini como LLM dos agentes que lidam com dados sensíveis (LGPD) | `marketplace-integration/google/` |
| **n8n** | Nó personalizado "AION Compliance" em TypeScript, com credenciais próprias, para chamar os agentes dentro de fluxos de automação | `n8n-nodes/aion-compliance/` |
| **HubSpot** | Projeto de app "AION Compliance" (plataforma 2026.03) | `hubspot-marketplace-app/` |
| **Stripe** | App "EcoSystem Compliance" dentro do Stripe, além da cobrança por assinatura da plataforma | `stripe-app/` |
| **Oracle e SAP** | Agentes de compliance, RH, cadeia de suprimentos e CBAM; automação de listagem no Oracle Cloud Marketplace | `marketplace-integration/oracle/` |
| **Navegador** | Extensão Chrome "SallesJam Compliance": agentes de compliance em qualquer site | `chrome-extension/` |
| **Zapier** | Integração do recepcionista de voz com webhooks | endpoints `/api/voice-agent` |
| **MCP** | Servidores MCP de referência (ERP, ESG, Microsoft, regulatório) e um servidor de RAG de SEO. O servidor de ERP responde com dados simulados e serve como contrato de ferramentas | `src/mcp/`, `mcp/seo-rag-mcp/` |
| **Vitrines de IA** | Prompts para MindStudio (NR-1, LGPD, vigilância regulatória), Hugging Face Space e agente Replit de pontuação de compliance | `mindstudio/`, `huggingface_space/`, `replit/` |
| **Diretórios e parceiros** | Guias de publicação para AppSumo, G2/Capterra, diretórios de IA, Autodesk e Pipefy | `marketplace-integration/` |

## Como o plugin chega ao agente

Cada plugin é uma casca fina: autentica o usuário, chama o endpoint do agente no backend e devolve o resultado no formato da plataforma. A regra de negócio, a licença por agente e a auditoria ficam no backend, então um agente novo pode ser exposto em todos os canais sem reescrita.
