# Segurança e governança de agentes

A plataforma trata o agente como um ativo a proteger e como um ator a vigiar. Os controles foram construídos em fases e estão em **níveis de integração diferentes**. Esta página diz em qual nível cada um está.

## Nível 1: no caminho de execução

| Controle | O que faz |
|---|---|
| **Gate de assinatura por agente** | Recusa a execução se o plano do cliente não inclui o agente |
| **Circuit breaker** | Corta um agente que falha repetidamente |
| **Trilha de auditoria e log de execução** | Cada tarefa do orquestrador é registrada |
| **Recibos de conformidade** | Ações de IA relevantes gravam recibo (ferramenta, argumentos, resultado, risco); o fluxo de voz usa trilha encadeada → [../examples/merkle_audit_chain.py](../examples/merkle_audit_chain.py) |
| **Proteção de endpoints administrativos** | Segredo de administração nas rotas sensíveis |

## Nível 2: aplicado na validação de saída (Quality Critic)

Controles integrados ao agente revisor, que valida as saídas de texto livre no orquestrador: **trust agent** (intercepta ações suspeitas), **detecção de extração de modelo**, **PragLocker** (ofuscação e validação de prompts), **CoTGuard** (monitoramento da cadeia de raciocínio), **RedAct** (redação de trajetórias), **marcas d'água** de autoria (AgentMark, SeqWM, backdoor) e **ITR** (compactação de contexto para custo).

## Nível 3: implementado e testado em isolamento

Marca d'água de pesos, **MASLEAK** (defesa contra extração da topologia multiagente), **DIRF** (consentimento e direitos de identidade), motor de decisão de política (permitir, perguntar, negar) e registro de agentes AIP. Têm testes e scripts de validação, e ainda não são chamados pelas requisições de produção.

## Nível 4: construído, ainda não ligado

ABAC e RBAC, DLP, mascaramento de PII, kill-switch de custo e controlador de orçamento, sanitização de entrada e detecção de ameaças.

## Próximos passos (prioridade)

1. **Controle de custo** (orçamento e kill-switch por tenant): evita gasto descontrolado de LLM.
2. **Sanitização de entrada e mascaramento de PII** antes de chamar o modelo: proteção contra injeção de prompt e dados pessoais em transcrições e documentos.
3. **RBAC por tenant** nas rotas de produto.
4. Proteção de propriedade intelectual (níveis 2 e 3): fica por último, pois protege contra roubo de modelo e não contra o risco operacional atual.

## Segurança de aplicação

- Configuração sensível por variável de ambiente; os manifestos de Kubernetes usam apenas placeholders.
- Middleware de privacidade e rotas de consentimento e de solicitação de titular (ver [COMPLIANCE.md](COMPLIANCE.md)).
