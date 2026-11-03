# Compliance

Dois lados: compliance **como produto** e compliance **da própria plataforma**.

## Compliance como produto

Agentes que transformam um catálogo regulatório real em avaliação, pontuação e documento (PDF/DOCX):

| Tema | Base |
|---|---|
| Segurança da informação | SOC 2 (critérios comuns), ISO/IEC 27001:2022 (Anexo A), risco de fornecedor, risco contratual |
| IA | EU AI Act (Art. 5, Anexo III, Art. 50, obrigações do Cap. III) |
| Sustentabilidade | CSRD / ESRS Set 1 (dupla materialidade), inventário de carbono GHG Protocol (escopos 1, 2 e 3), exposição CBAM |
| Trabalhista e social | NR-1 (riscos psicossociais, gera PGR), equidade salarial (Lei 14.611/2023) |
| Integridade | Canal de denúncias (Diretiva UE 2019/1937), anticorrupção (Decreto 11.129/2022, alinhado à ISO 37001) |
| Tributário | Prontidão para CBS/IBS (EC 132/2023, LC 214/2025) |
| Privacidade | LGPD operacional |

**Princípio:** o catálogo regulatório é fixo e vem de norma real; o LLM só responde se um item se aplica à empresa e se há política ou métrica; limiares (por exemplo, "100+ funcionários" na equidade salarial) e pontuações são calculados em código. Nenhuma decisão regulatória fica a cargo do modelo. → [../examples/csrd_deterministic_agent.py](../examples/csrd_deterministic_agent.py)

## Compliance da plataforma

- **Privacidade:** política, termos e uso aceitável publicados; registro e revogação de consentimento; solicitações de acesso e de exclusão de dados do titular.
- **Recibos de auditoria de IA:** ações automatizadas (por exemplo, classificação de intenção em uma chamada de voz) gravam recibo com ferramenta, argumentos, resultado e classificação de risco.
- **Trilha encadeada** (Merkle) para auditoria à prova de adulteração.
- **Roteamento por sensibilidade:** no registro, os agentes de dados pessoais sensíveis (LGPD) são atribuídos a um provedor de LLM dedicado.
- **Telefonia:** páginas de privacidade e termos no produto de voz, e tratamento de pedidos de dados do chamador.

## Limites declarados

Os produtos auxiliam a preparação e a documentação; não substituem parecer jurídico ou auditoria formal.
