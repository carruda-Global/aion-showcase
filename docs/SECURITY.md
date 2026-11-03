# Segurança e governança de agentes

A plataforma trata o agente como um ativo a proteger e como um ator a vigiar. Esta página separa o que **já está ligado ao fluxo de execução** do que está **implementado mas ainda não integrado**.

## Ligado ao fluxo de execução

| Controle | O que faz |
|---|---|
| **Gate de assinatura por agente** | Recusa a execução se o plano do cliente não inclui o agente |
| **Trust agent** | Intercepta ações de entrada e bloqueia as suspeitas |
| **Detecção de extração de modelo** | Identifica consultas que tentam reconstruir o comportamento do agente |
| **PragLocker** | Ofuscação e validação de prompts e bloqueio de habilidades |
| **CoTGuard** | Monitoramento da cadeia de raciocínio |
| **RedAct** | Redação das trajetórias de raciocínio para reduzir vazamento |
| **AgentMark, SeqWM, WeightWM, marca de backdoor** | Marcas d'água de autoria nas saídas, na sequência de ações e nos pesos, com prova de propriedade por gatilho |
| **MASLEAK** | Defesa contra extração da topologia do sistema multiagente (segmenta prompts, rastreia consultas, oculta a topologia) |
| **DIRF** | Consentimento e direitos de identidade: registro e revogação de consentimento, registro de monetização, proteção de dados biométricos |
| **ITR** | Controle de custo de LLM por compactação inteligente de contexto |
| **Circuit breaker** | Corta um agente que falha repetidamente |
| **Registro de agentes (AIP)** | Identidade e política por agente |
| **Motor de decisão de política** | Decide permitir, perguntar ou negar a partir de política declarativa |
| **Trilha de auditoria com cadeia Merkle** | Registro encadeado e à prova de adulteração → [../examples/merkle_audit_chain.py](../examples/merkle_audit_chain.py) |
| **Recibos de conformidade** | Cada ação de IA relevante grava um recibo (por exemplo, a classificação de uma chamada de voz) |

## Implementado, ainda não integrado ao fluxo

ABAC e RBAC, DLP, mascaramento de PII, kill-switch de custo e controlador de orçamento, sanitização de entrada, detecção de ameaças e o cliente/proxy do registro de agentes. Existem como módulos, mas ainda não são chamados pelo caminho de execução. Estão no plano de trabalho, e não são apresentados aqui como proteção ativa.

## Segurança de aplicação

- Configuração sensível por variável de ambiente; os manifestos de Kubernetes usam apenas placeholders.
- Endpoints administrativos protegidos por segredo.
- Middleware de privacidade e rotas de consentimento e de solicitação de titular (ver [COMPLIANCE.md](COMPLIANCE.md)).
