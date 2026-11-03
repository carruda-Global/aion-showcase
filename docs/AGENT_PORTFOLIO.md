# Portfólio de agentes

Organizado por domínio, a partir do **registro de agentes** da plataforma (jun/2026). A coluna *Situação* é literal: **Ativo** = ativo no registro; **Co-sell** = disponível via parceria Microsoft; **Planejado** = construído para a trilha do marketplace correspondente, com lançamento agendado; **Interno** = existe na plataforma mas não é vendido.

Os produtos testados ponta a ponta contra a API implantada estão em [MATURITY.md](MATURITY.md).

## Engenharia, projetos e obras (AEC)

Do projeto ao documento: especificações, compras, estoque, logística, BIM, execução em campo, RFIs e conformidade.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Analista de Especificações** | Análise de especificações técnicas, extração de requisitos, sinalização de contradições conforme NBR | DeepSeek | Ativo |
| **Agente de Compras** | Processamento de pedidos de compra, comparação de cotações, geração de requisições e otimização de custos | DeepSeek | Ativo |
| **Gestão de Estoque** | Monitoramento em tempo real de estoque de obras, identificação de escassez e sugestão de substitutos | DeepSeek | Ativo |
| **Logística e Rastreamento** | Acompanhamento de envios, identificação de problemas de entrega e geração de alertas de atraso | DeepSeek | Ativo |
| **Execução em Campo** | Tradução de modelos BIM em instruções de campo, identificação de desvios de projeto | DeepSeek | Ativo |
| **Coordenador BIM** | Criação de elementos 3D via texto, clash detection entre disciplinas, validação de modelos BIM | DeepSeek | Ativo |
| **Análise de Requisitos** | Avaliação de requisitos contra padrões de qualidade, geração de scores e identificação de ambiguidades | DeepSeek | Ativo |
| **Assistente de Engenharia** | Assistente conversacional para perguntas técnicas, busca semântica em documentos e sumarização | DeepSeek | Ativo |
| **Resumo de Tarefas** | Geração de resumos estruturados de tarefas e defeitos de obra com captura de riscos e prazos | DeepSeek | Ativo |
| **Inteligência Visual de Obras** | Análise visual de fotos de obras para detecção de riscos de segurança e progresso | DeepSeek | Ativo |
| **Criação de RFIs** | Geração profissional de RFIs a partir de dúvidas de campo com busca em especificações | DeepSeek | Ativo |
| **Conformidade PGRS/PGRSS** | Gestão de conformidade legal, documentação, alertas de prazos regulatórios e obrigações ambientais | DeepSeek | Ativo |

## Compliance e regulatório

Catálogos regulatórios reais (NR-1, LGPD, CBS/IBS, ESG/IFRS, carbono, escopo 3, canal de denúncias, equidade salarial, anticorrupção).

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **NR-1 Riscos Psicossociais** | Inventário de riscos psicossociais (FRPRT) conforme Portaria MTE 1.419/2024, plano de ação e relatórios | Gemini | Ativo |
| **Tributário CBS/IBS** | Conformidade com LC 214/2025: classificação NCM, alíquotas, declarações DeRE e simulação de impacto fiscal | DeepSeek | Planejado Q4/2026 |
| **LGPD Operacional** | Mapeamento de fluxos de dados, RoPA conforme ANPD, identificação de lacunas e monitoramento de incidentes | Gemini | Ativo |
| **ESG IFRS S1/S2** | Diagnóstico ESG, relatórios IFRS S1/S2, resposta a questionários de clientes corporativos | DeepSeek | Planejado Q1/2027 |
| **Inventário de Carbono** | Cálculo de emissões GEE Escopo 1/2 conforme GHG Protocol e Lei 15.042/2024 (SBCE) | DeepSeek | Planejado Q1/2027 |
| **Escopo 3 Fornecedores** | Rastreamento de emissões Escopo 3 na cadeia de fornecedores conforme SBCE + CBAM + IFRS S2 | DeepSeek | Planejado Q1/2027 |
| **Canal de Denúncias** | Canal omnichannel com anonimato, triagem automática, investigação e relatórios CIPA (Lei 14.457/2022) | Gemini | Ativo |
| **Igualdade Salarial** | Análise de equidade salarial conforme Lei 14.611/2023 com relatórios MTE e planos de ação | DeepSeek | Ativo |
| **Compliance Anticorrupção** | Programa de integridade conforme Lei 12.846/2013: diagnóstico CGU, código de ética, due diligence | DeepSeek | Planejado Q4/2026 |

## Microsoft: Teams, Copilot e Dynamics 365

Agentes para o ecossistema Microsoft, incluindo Dynamics 365 e Power BI.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Regulatory Analyst** | Análise de contratos e documentos via SharePoint/OneDrive, identificação de riscos LGPD/NR-1/ESG | DeepSeek | Co-sell Microsoft |
| **Compliance PM** | Gestão de projetos de compliance com tarefas automáticas no Microsoft Planner e alertas no Teams | DeepSeek | Co-sell Microsoft |
| **Channel Agent Regulatório** | Monitoramento de canais Teams para detecção de riscos de conformidade trabalhista e tributária | DeepSeek | Co-sell Microsoft |
| **Knowledge Agent** | Indexação de documentos SharePoint com RAG e busca inteligente para consultas de compliance | DeepSeek | Co-sell Microsoft |
| **Facilitator Agent** | Facilitação de reuniões de compliance, atas, minutas e tarefas automáticas no Planner | DeepSeek | Co-sell Microsoft |
| **Dev Experience Agent** | Automação de PRs, code reviews e conformidade LGPD em código no GitHub | DeepSeek | Co-sell Microsoft |
| **Dynamics Sales Compliance** | Análise de pipeline de vendas do Dynamics 365 com alertas de risco regulatório | DeepSeek | Planejado Q4/2026 |
| **Dynamics Finance Regulatory** | Conformidade fiscal e financeira integrada ao Dynamics 365 Finance | DeepSeek | Planejado Q4/2026 |
| **Dynamics Supply Chain ESG** | Rastreamento ESG na cadeia de suprimentos do Dynamics 365 Supply Chain | DeepSeek | Planejado Q4/2026 |
| **Dynamics HR Compliance** | Conformidade trabalhista e NR-1 integrada ao Dynamics 365 Human Resources | DeepSeek | Planejado Q4/2026 |
| **Dynamics Customer Service** | Automação de atendimento ao cliente com conformidade regulatória no Dynamics 365 | DeepSeek | Planejado Q4/2026 |
| **Power BI Compliance** | Dashboards de compliance no Power BI com indicadores regulatórios e ESG | DeepSeek | Interno (não comercializado) |

## Salesforce Agentforce

Agentes para vendas, serviço em campo, contratos, receita e sustentabilidade dentro do Salesforce.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Agentforce SDR** | Prospecção e qualificação de leads BANT via Salesforce Agentforce | DeepSeek | Planejado Q4/2026 |
| **Agentforce Field Service** | Gestão de serviços de campo com conformidade regulatória via Salesforce | DeepSeek | Planejado Q4/2026 |
| **Agentforce Contract Intelligence** | Análise inteligente de contratos com detecção de riscos legais via Salesforce | DeepSeek | Planejado Q4/2026 |
| **Agentforce Revenue Intelligence** | Inteligência de receita com forecasting e detecção de oportunidades via Salesforce | DeepSeek | Planejado Q4/2026 |
| **Agentforce Sustainability** | Gestão de metas de sustentabilidade e relatórios ESG via Salesforce Net Zero Cloud | DeepSeek | Planejado Q4/2026 |

## Oracle e SAP

Compliance e cadeia de suprimentos sobre ERPs corporativos.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Oracle ERP Compliance** | Conformidade fiscal e regulatória integrada ao Oracle Fusion ERP | DeepSeek | Planejado Q1/2027 |
| **Oracle HCM Regulatory** | Conformidade trabalhista e NR-1 integrada ao Oracle Fusion HCM | DeepSeek | Planejado Q1/2027 |
| **Oracle Supply Chain ESG** | Rastreamento ESG na cadeia de suprimentos do Oracle Fusion SCM | DeepSeek | Planejado Q1/2027 |
| **Oracle CX Sales** | Automação de vendas com conformidade regulatória no Oracle Fusion CX | DeepSeek | Planejado Q1/2027 |
| **SAP Joule Compliance Bridge** | Ponte de compliance entre SAP S/4HANA e regulamentações brasileiras via Joule Studio | DeepSeek | Planejado Q1/2027 |
| **SAP Predictive Maintenance** | Manutenção preditiva com conformidade regulatória integrada ao SAP PM | DeepSeek | Planejado Q1/2027 |
| **SAP CBAM Export** | Conformidade com CBAM (Carbon Border Adjustment Mechanism) para exportadores da UE via SAP GTS | DeepSeek | Planejado Q1/2027 |

## Microagentes (plugáveis e de baixa fricção)

Agentes pequenos e focados, projetados para entrar em plugins, Teams e fluxos de automação.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Diagnóstico Rápido NR-1** | Diagnóstico inicial de riscos psicossociais (M1 - filho do #13 NR-1) | Gemini | Ativo |
| **LGPD Scanner** | Varredura de sistemas para listagem de dados pessoais (M2 - filho do #15 LGPD) | Gemini | Ativo |
| **Folha Equidade** | Cálculo de gap salarial por gênero (M3 - filho do #20 Igualdade Salarial) | Gemini | Ativo |
| **Contract Review** | Revisão individual de contratos (M4 - filho do #22 Regulatory Analyst) | Gemini | Co-sell Microsoft |
| **Teams Risk Monitor** | Monitoramento de 1 canal Teams para riscos (M5 - filho do #24 Channel Agent) | DeepSeek | Co-sell Microsoft |
| **Meeting Minutes** | Geração de ata e tarefas no Planner (M6 - filho do #26 Facilitator Agent) | DeepSeek | Co-sell Microsoft |
| **PR LGPD Checker** | Verificação de PII em Pull Requests (M7 - filho do #27 Dev Experience) | Claude | Co-sell Microsoft |
| **Admissão Checklist** | Checklist de admissão de funcionários (M8 - filho do N1 Onboarding) | Gemini | Ativo |
| **Sales Pipeline Checker** | Análise de deals em risco no pipeline (M9 - filho do #31 Dynamics Sales) | DeepSeek | Planejado Q4/2026 |
| **Expense Anomaly Detector** | Detecção de anomalias em despesas (M10 - filho do #32 Dynamics Finance) | DeepSeek | Planejado Q4/2026 |
| **Compliance Score** | Score de compliance 0-100 (M11 - filho do #36 Power BI Compliance) | DeepSeek | Planejado Q4/2026 |
| **Lead Qualifier** | Qualificação de leads com scoring (M12 - filho do #58 Sales Agent) | DeepSeek | Ativo |
| **Code Reviewer** | Code review de PRs (M13 - filho do #57 Software Engineering) | Claude | Ativo |
| **Headcount Alert** | Alerta de sobrecarga de equipe (M14 - filho do #59 Workforce Orchestrator) | Claude | Ativo |
| **Regulatory Alert** | Alerta de mudança de norma regulatória (M15 - filho do #51 Regulatory Watch) | Gemini | Ativo |

## Venda cruzada e operações

Onboarding, atendimento ao cliente em PT-BR e conciliação financeira.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Onboarding de Funcionários** | Automação de admissão: contratos, checklist de documentos, provisionamento de acessos e eSocial | DeepSeek | Ativo |
| **Atendimento ao Cliente PT-BR** | Resolução automática de tickets L1 via WhatsApp e Teams em português brasileiro | DeepSeek | Ativo |
| **Conciliação Financeira** | Automação de fechamento mensal com conciliação de NFs, extratos, cartão e boletos (PIX/TED) | DeepSeek | Ativo |

## Orquestração, inteligência e autoaperfeiçoamento

Camada de coordenação, monitoramento regulatório, revisão de qualidade e aprendizado do ecossistema.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Master Orchestrator** | Orquestrador central que coordena todos os 60+ agentes para workflows multi-etapa | Claude | Interno (não comercializado) |
| **Cross-Platform Bridge** | Ponte de integração entre plataformas Google, Microsoft, Salesforce, Oracle e SAP | DeepSeek | Interno (não comercializado) |
| **Regulatory Watch** | Monitoramento 24/7 de mudanças regulatórias no DOU, ANPD, MTE e Receita Federal | Gemini | Interno (não comercializado) |
| **Client Intelligence** | Análise de comportamento e necessidades do cliente para recomendações personalizadas | DeepSeek | Ativo |
| **Quality Critic** | Revisor crítico de qualidade das respostas de todos os agentes com métricas de precisão | Claude | Interno (não comercializado) |
| **Meta-Learning Agent** | Auto-aprendizado baseado em interações anteriores para melhoria contínua dos agentes | Claude | Planejado Q1/2027 |
| **Ecosystem Evolution** | Evolução autônoma do ecossistema com criação de novos agentes baseada em demanda | Claude | Planejado Q1/2027 |
| **Federated Knowledge** | Compartilhamento federado de conhecimento entre instâncias do EcoSystem | DeepSeek | Planejado Q1/2027 |

## Tecnologia, conectores e IA física

Engenharia de software, governança universal, revisão de código e conectores.

| Agente | O que faz | LLM | Situação |
|---|---|---|---|
| **Software Engineering Agent** | Arquitetura, code review, boas práticas e documentação automática de software | Claude | Interno (não comercializado) |
| **Sales Agent** | Vendedor autônomo do EcoSystem: sugere planos, calcula descontos e dispara cross-sell chain | DeepSeek | Interno (não comercializado) |
| **Workforce Orchestrator** | Coordenação de RH: onboarding, NR-1, igualdade salarial, denúncias, Dynamics HR e Oracle HCM | Claude | Interno (não comercializado) |
| **Universal Governance Layer** | Camada de governança universal para políticas cross-plataforma | Claude | Interno (não comercializado) |
| **Antigravity Bridge** | Ponte de integração Google <-> Microsoft para sincronização de dados e workflows | DeepSeek | Interno (não comercializado) |
| **MAI Code Reviewer** | Revisor de código para garantia de qualidade e conformidade em projetos multi-plataforma | Claude | Planejado Q1/2027 |
| **Physical AI Connector** | Conector NVIDIA Omniverse + Azure Foundry + Google GKE para robótica e IoT industrial | DeepSeek | Interno (não comercializado) |

