# Portfólio de agentes

Organizado por domínio, a partir do **registro de agentes** (jun/2026) cruzado com uma varredura do código de produção (out/2026). A coluna *Evidência no código* é literal:

- **Implementado:** módulo com chamada a LLM e/ou banco de dados e lógica própria.
- **Parcial:** módulo existe, mas é enxuto ou depende de integração ainda não completa.
- **Esqueleto:** estrutura criada, sem lógica de produto.
- **Catalogado:** definido no registro, na configuração e no registry do Kubernetes, ainda sem módulo de código.

Os produtos testados ponta a ponta contra a API implantada estão em [MATURITY.md](MATURITY.md).

## Engenharia, projetos e obras (AEC)

Do projeto ao documento: especificações, compras, estoque, logística, BIM, execução em campo, RFIs e conformidade.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Analista de Especificações** | Análise de especificações técnicas, extração de requisitos, sinalização de contradições conforme NBR | DeepSeek | Parcial, com testes |
| **Agente de Compras** | Processamento de pedidos de compra, comparação de cotações, geração de requisições e otimização de custos | DeepSeek | Parcial, com testes |
| **Gestão de Estoque** | Monitoramento em tempo real de estoque de obras, identificação de escassez e sugestão de substitutos | DeepSeek | Parcial, com testes |
| **Logística e Rastreamento** | Acompanhamento de envios, identificação de problemas de entrega e geração de alertas de atraso | DeepSeek | Parcial, com testes |
| **Execução em Campo** | Tradução de modelos BIM em instruções de campo, identificação de desvios de projeto | DeepSeek | Parcial, com testes |
| **Coordenador BIM** | Criação de elementos 3D via texto, clash detection entre disciplinas, validação de modelos BIM | DeepSeek | Parcial, com testes |
| **Análise de Requisitos** | Avaliação de requisitos contra padrões de qualidade, geração de scores e identificação de ambiguidades | DeepSeek | Parcial, com testes |
| **Assistente de Engenharia** | Assistente conversacional para perguntas técnicas, busca semântica em documentos e sumarização | DeepSeek | Parcial, com testes |
| **Resumo de Tarefas** | Geração de resumos estruturados de tarefas e defeitos de obra com captura de riscos e prazos | DeepSeek | Parcial, com testes |
| **Inteligência Visual de Obras** | Análise visual de fotos de obras para detecção de riscos de segurança e progresso | DeepSeek | Parcial, com testes |
| **Criação de RFIs** | Geração profissional de RFIs a partir de dúvidas de campo com busca em especificações | DeepSeek | Parcial, com testes |
| **Conformidade PGRS/PGRSS** | Gestão de conformidade legal, documentação, alertas de prazos regulatórios e obrigações ambientais | DeepSeek | Parcial, com testes |

## Compliance e regulatório

Catálogos regulatórios (NR-1, LGPD, CBS/IBS, ESG/IFRS, carbono, escopo 3, canal de denúncias, equidade salarial, anticorrupção).

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **NR-1 Riscos Psicossociais** | Inventário de riscos psicossociais (FRPRT) conforme Portaria MTE 1.419/2024, plano de ação e relatórios | Gemini | Implementado, com testes |
| **Tributário CBS/IBS** | Conformidade com LC 214/2025: classificação NCM, alíquotas, declarações DeRE e simulação de impacto fiscal | DeepSeek | Implementado, com testes |
| **LGPD Operacional** | Mapeamento de fluxos de dados, RoPA conforme ANPD, identificação de lacunas e monitoramento de incidentes | Gemini | Implementado, com testes |
| **ESG IFRS S1/S2** | Diagnóstico ESG, relatórios IFRS S1/S2, resposta a questionários de clientes corporativos | DeepSeek | Implementado, com testes |
| **Inventário de Carbono** | Cálculo de emissões GEE Escopo 1/2 conforme GHG Protocol e Lei 15.042/2024 (SBCE) | DeepSeek | Implementado, com testes |
| **Escopo 3 Fornecedores** | Rastreamento de emissões Escopo 3 na cadeia de fornecedores conforme SBCE + CBAM + IFRS S2 | DeepSeek | Parcial, com testes |
| **Canal de Denúncias** | Canal omnichannel com anonimato, triagem automática, investigação e relatórios CIPA (Lei 14.457/2022) | Gemini | Implementado, com testes |
| **Igualdade Salarial** | Análise de equidade salarial conforme Lei 14.611/2023 com relatórios MTE e planos de ação | DeepSeek | Implementado, com testes |
| **Compliance Anticorrupção** | Programa de integridade conforme Lei 12.846/2013: diagnóstico CGU, código de ética, due diligence | DeepSeek | Implementado, com testes |

## Microsoft: Teams, Copilot e Dynamics 365

Agentes para o ecossistema Microsoft.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Regulatory Analyst** | Análise de contratos e documentos via SharePoint/OneDrive, identificação de riscos LGPD/NR-1/ESG | DeepSeek | Implementado, com testes |
| **Compliance PM** | Gestão de projetos de compliance com tarefas automáticas no Microsoft Planner e alertas no Teams | DeepSeek | Implementado, com testes |
| **Channel Agent Regulatório** | Monitoramento de canais Teams para detecção de riscos de conformidade trabalhista e tributária | DeepSeek | Implementado, com testes |
| **Knowledge Agent** | Indexação de documentos SharePoint com RAG e busca inteligente para consultas de compliance | DeepSeek | Implementado, com testes |
| **Facilitator Agent** | Facilitação de reuniões de compliance, atas, minutas e tarefas automáticas no Planner | DeepSeek | Implementado, com testes |
| **Dev Experience Agent** | Automação de PRs, code reviews e conformidade LGPD em código no GitHub | DeepSeek | Implementado, com testes |
| **Dynamics Sales Compliance** | Análise de pipeline de vendas do Dynamics 365 com alertas de risco regulatório | DeepSeek | Parcial (módulo enxuto), com testes |
| **Dynamics Finance Regulatory** | Conformidade fiscal e financeira integrada ao Dynamics 365 Finance | DeepSeek | Parcial (módulo enxuto), com testes |
| **Dynamics Supply Chain ESG** | Rastreamento ESG na cadeia de suprimentos do Dynamics 365 Supply Chain | DeepSeek | Parcial (módulo enxuto), com testes |
| **Dynamics HR Compliance** | Conformidade trabalhista e NR-1 integrada ao Dynamics 365 Human Resources | DeepSeek | Parcial (módulo enxuto), com testes |
| **Dynamics Customer Service** | Automação de atendimento ao cliente com conformidade regulatória no Dynamics 365 | DeepSeek | Parcial (módulo enxuto), com testes |
| **Power BI Compliance** | Dashboards de compliance no Power BI com indicadores regulatórios e ESG | DeepSeek | Catalogado (sem módulo de código) |

## Salesforce Agentforce

Vendas, serviço em campo, contratos, receita e sustentabilidade.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Agentforce SDR** | Prospecção e qualificação de leads BANT via Salesforce Agentforce | DeepSeek | Catalogado (sem módulo de código) |
| **Agentforce Field Service** | Gestão de serviços de campo com conformidade regulatória via Salesforce | DeepSeek | Catalogado (sem módulo de código) |
| **Agentforce Contract Intelligence** | Análise inteligente de contratos com detecção de riscos legais via Salesforce | DeepSeek | Catalogado (sem módulo de código) |
| **Agentforce Revenue Intelligence** | Inteligência de receita com forecasting e detecção de oportunidades via Salesforce | DeepSeek | Catalogado (sem módulo de código) |
| **Agentforce Sustainability** | Gestão de metas de sustentabilidade e relatórios ESG via Salesforce Net Zero Cloud | DeepSeek | Catalogado (sem módulo de código) |

## Oracle e SAP

Compliance e cadeia de suprimentos sobre ERPs corporativos.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Oracle ERP Compliance** | Conformidade fiscal e regulatória integrada ao Oracle Fusion ERP | DeepSeek | Catalogado (sem módulo de código) |
| **Oracle HCM Regulatory** | Conformidade trabalhista e NR-1 integrada ao Oracle Fusion HCM | DeepSeek | Catalogado (sem módulo de código) |
| **Oracle Supply Chain ESG** | Rastreamento ESG na cadeia de suprimentos do Oracle Fusion SCM | DeepSeek | Catalogado (sem módulo de código) |
| **Oracle CX Sales** | Automação de vendas com conformidade regulatória no Oracle Fusion CX | DeepSeek | Catalogado (sem módulo de código) |
| **SAP Joule Compliance Bridge** | Ponte de compliance entre SAP S/4HANA e regulamentações brasileiras via Joule Studio | DeepSeek | Catalogado (sem módulo de código) |
| **SAP Predictive Maintenance** | Manutenção preditiva com conformidade regulatória integrada ao SAP PM | DeepSeek | Catalogado (sem módulo de código) |
| **SAP CBAM Export** | Conformidade com CBAM (Carbon Border Adjustment Mechanism) para exportadores da UE via SAP GTS | DeepSeek | Catalogado (sem módulo de código) |

## Microagentes (plugáveis)

Agentes pequenos e focados para plugins, Teams e automações.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Diagnóstico Rápido NR-1** | Diagnóstico inicial de riscos psicossociais (M1 - filho do #13 NR-1) | Gemini | Catalogado (sem módulo de código) |
| **LGPD Scanner** | Varredura de sistemas para listagem de dados pessoais (M2 - filho do #15 LGPD) | Gemini | Catalogado (sem módulo de código) |
| **Folha Equidade** | Cálculo de gap salarial por gênero (M3 - filho do #20 Igualdade Salarial) | Gemini | Catalogado (sem módulo de código) |
| **Contract Review** | Revisão individual de contratos (M4 - filho do #22 Regulatory Analyst) | Gemini | Catalogado (sem módulo de código) |
| **Teams Risk Monitor** | Monitoramento de 1 canal Teams para riscos (M5 - filho do #24 Channel Agent) | DeepSeek | Catalogado (sem módulo de código) |
| **Meeting Minutes** | Geração de ata e tarefas no Planner (M6 - filho do #26 Facilitator Agent) | DeepSeek | Catalogado (sem módulo de código) |
| **PR LGPD Checker** | Verificação de PII em Pull Requests (M7 - filho do #27 Dev Experience) | Claude | Catalogado (sem módulo de código) |
| **Admissão Checklist** | Checklist de admissão de funcionários (M8 - filho do N1 Onboarding) | Gemini | Catalogado (sem módulo de código) |
| **Sales Pipeline Checker** | Análise de deals em risco no pipeline (M9 - filho do #31 Dynamics Sales) | DeepSeek | Catalogado (sem módulo de código) |
| **Expense Anomaly Detector** | Detecção de anomalias em despesas (M10 - filho do #32 Dynamics Finance) | DeepSeek | Catalogado (sem módulo de código) |
| **Compliance Score** | Score de compliance 0-100 (M11 - filho do #36 Power BI Compliance) | DeepSeek | Catalogado (sem módulo de código) |
| **Lead Qualifier** | Qualificação de leads com scoring (M12 - filho do #58 Sales Agent) | DeepSeek | Parcial |
| **Code Reviewer** | Code review de PRs (M13 - filho do #57 Software Engineering) | Claude | Catalogado (sem módulo de código) |
| **Headcount Alert** | Alerta de sobrecarga de equipe (M14 - filho do #59 Workforce Orchestrator) | Claude | Catalogado (sem módulo de código) |
| **Regulatory Alert** | Alerta de mudança de norma regulatória (M15 - filho do #51 Regulatory Watch) | Gemini | Catalogado (sem módulo de código) |

## Venda cruzada e operações

Onboarding, atendimento PT-BR e conciliação financeira.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Onboarding de Funcionários** | Automação de admissão: contratos, checklist de documentos, provisionamento de acessos e eSocial | DeepSeek | Implementado, com testes |
| **Atendimento ao Cliente PT-BR** | Resolução automática de tickets L1 via WhatsApp e Teams em português brasileiro | DeepSeek | Implementado, com testes |
| **Conciliação Financeira** | Automação de fechamento mensal com conciliação de NFs, extratos, cartão e boletos (PIX/TED) | DeepSeek | Implementado, com testes |

## Orquestração, inteligência e autoaperfeiçoamento

Coordenação, monitoramento regulatório, revisão de qualidade e aprendizado.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Master Orchestrator** | Orquestrador central que coordena todos os 60+ agentes para workflows multi-etapa | Claude | Parcial, com testes |
| **Cross-Platform Bridge** | Ponte de integração entre plataformas Google, Microsoft, Salesforce, Oracle e SAP | DeepSeek | Parcial (módulo enxuto), com testes |
| **Regulatory Watch** | Monitoramento 24/7 de mudanças regulatórias no DOU, ANPD, MTE e Receita Federal | Gemini | Parcial (módulo enxuto), com testes |
| **Client Intelligence** | Análise de comportamento e necessidades do cliente para recomendações personalizadas | DeepSeek | Parcial (módulo enxuto), com testes |
| **Quality Critic** | Revisor crítico de qualidade das respostas de todos os agentes com métricas de precisão | Claude | Parcial, com testes |
| **Meta-Learning Agent** | Auto-aprendizado baseado em interações anteriores para melhoria contínua dos agentes | Claude | Parcial (módulo enxuto), com testes |
| **Ecosystem Evolution** | Evolução autônoma do ecossistema com criação de novos agentes baseada em demanda | Claude | Parcial (módulo enxuto), com testes |
| **Federated Knowledge** | Compartilhamento federado de conhecimento entre instâncias do EcoSystem | DeepSeek | Parcial (módulo enxuto), com testes |

## Tecnologia, conectores e IA física

Engenharia de software, governança e conectores.

| Agente | O que faz | LLM | Evidência no código |
|---|---|---|---|
| **Software Engineering Agent** | Arquitetura, code review, boas práticas e documentação automática de software | Claude | Esqueleto |
| **Sales Agent** | Vendedor autônomo do EcoSystem: sugere planos, calcula descontos e dispara cross-sell chain | DeepSeek | Parcial (módulo enxuto), com testes |
| **Workforce Orchestrator** | Coordenação de RH: onboarding, NR-1, igualdade salarial, denúncias, Dynamics HR e Oracle HCM | Claude | Parcial (módulo enxuto) |
| **Universal Governance Layer** | Camada de governança universal para políticas cross-plataforma | Claude | Catalogado (sem módulo de código) |
| **Antigravity Bridge** | Ponte de integração Google <-> Microsoft para sincronização de dados e workflows | DeepSeek | Implementado |
| **MAI Code Reviewer** | Revisor de código para garantia de qualidade e conformidade em projetos multi-plataforma | Claude | Implementado |
| **Physical AI Connector** | Conector NVIDIA Omniverse + Azure Foundry + Google GKE para robótica e IoT industrial | DeepSeek | Parcial |

## Agentes de crescimento, voz e operação (fora do registro)

Implementados no código de produção e usados pelos produtos de voz, SEO, vendas e monitoramento. A descrição vem do próprio módulo.

| Módulo | O que faz | Testes |
|---|---|---|
| `aec_core_agents` | — | — |
| `agente_invest` | Agente Analitico Invest -- the AION-orchestrated wrapper around Orbit, the forex/ICT-SMC/Wyckoff trading-analysis dashboard vendored under orbit/ and running as a second  | — |
| `architecture_support_agents` | Real, LLM-backed replacements for the 3 architecture-support agents worth keeping (client_intelligence, quality_critic, regulatory_watch). The other 6 in this cluster (me | — |
| `content_syndication_agent` | — | — |
| `contract_risk_agent` | Global Contract Risk Copilot — contract upload -> real clause catalog -> deterministic gap scoring -> PDF with free/premium paywall. | — |
| `csrd_reporting_agent` | CSRD Double Materiality Copilot — company profile -> real ESRS topic catalog -> deterministic materiality + readiness scoring -> PDF with free/premium paywall. | — |
| `directory_submission_agent` | Directory/review-site listing + PR distribution for the AI Voice Receptionist product. Repurposed 2026-07 — the 19-Copilot compliance catalog is retired, this product is  | — |
| `engcopilot_embeddings` | Real embedding-based retrieval for the engcopilot schema -- powers the 8 AEC core agents (src/agents/aec_rag.py). Uses the SAME asyncpg pool the engineering_copilot modul | — |
| `eu_ai_act_agent` | Global EU AI Act Copilot — AI system documentation upload -> real risk-tier catalog (Article 5 prohibited practices, Annex III high-risk categories, Article 50 transparen | sim |
| `iso27001_agent` | Global ISO27001 Copilot — questionário estruturado (catálogo real Anexo A) -> motor de gap relacional -> PDF com paywall free/premium. Mesma arquitetura do NR1/SOC2. | — |
| `monitoring` | — | — |
| `outbound_sdr_agent` | — | — |
| `partnership_agent` | — | — |
| `pmoc_seo_agent` | — | — |
| `seo_content_agent` | — | sim |
| `seo_feedback_agent` | Phase 2 — Google Search Console feedback loop for the SEO content engine. | sim |
| `soc2_agent` | Global SOC2 Copilot — structured questionnaire (real AICPA TSC catalog) -> deterministic gap engine -> PDF with free/premium paywall. | — |
| `system_health_agent` | Real daily/pulse health check across every real, connected surface of the system (site, backend, database, payments, AgentVerse, the 11 real orchestrator agents). Persist | — |
| `universal_governance` | — | — |
| `vendor_risk_agent` | Global Vendor Risk Copilot — vendor questionnaire/certification upload -> real risk criteria catalog -> deterministic gap scoring -> PDF with free/premium paywall. Same a | — |
| `voice_call_intelligence` | Real post-call intent classification for the Voice Receptionist. | — |
| `voice_compliance_receipts` | Persistent wrapper around src.security.audit.ComplianceReceipt for the Voice Receptionist call pipeline. | — |
| `voice_i18n` | Per-language content for the Voice Receptionist assistant prompt. | — |
| `voice_overage_billing_agent` | Real overage billing for the Voice Receptionist product -- billed per unique caller over the plan's monthly cap, not per minute. | — |
| `voice_usage_alerts_agent` | Customer-facing usage alerts for the Voice Receptionist product -- voice_overage_billing_agent.py bills overage silently but never tells the customer anything. This file  | — |
| `whistleblower_agent` | Whistleblower Channel Copilot — report intake -> real EU Whistleblower Directive (2019/1937) category catalog -> deterministic severity scoring and statutory-deadline cal | — |
| `zapier_integration_agent` | — | — |
