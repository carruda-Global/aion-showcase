# Orbit — motor de análise ICT/SMC para forex

**Atribuição.** O Orbit parte do [OpenProphet](https://github.com/JakeNesler/OpenProphet), de Jake Nesler, publicado sob a licença **CC BY-NC 4.0** (atribuição, uso não comercial). A base original é um agente autônomo de trading com painel web, ferramentas MCP e backend em Go. Este projeto é um trabalho derivado e **não é apresentado como autoria original**.

## O que eu construí sobre a base

A base original não tem análise de Smart Money Concepts nem suporte a forex. O trabalho próprio está em:

| Área | Conteúdo |
|---|---|
| **Pacote `smc/`** (Go, com testes) | Análise ICT/SMC: order blocks, breaker blocks, validação de CHoCH, fatores de confirmação e confluência, anotações de gráfico, agregação multi-timeframe, ATR e backtest de sistema combinado |
| **Ferramentas de linha de comando** | Backtest de forex, backtest sobre dados reais, relatório de correlação, importação de barras históricas (CSV) e exportação/importação de barras |
| **Serviços e controllers** | Camada de serviços e de API estendida para forex e para os alertas |
| **Painel e base de conhecimento** | Painel adaptado e servidor de conhecimento com cartões de estudo (ICT/SMC/Wyckoff) e overrides em português |
| **Integração com o AION** | Um agente analítico do AION orquestra o Orbit; o FastAPI faz proxy reverso para o backend Go, que roda como processo interno no mesmo contêiner |

## O que isso mostra

- Capacidade de pegar um sistema de terceiros, entender a arquitetura e estendê-lo com um módulo grande e testado.
- Um agente autônomo com ferramentas MCP, ligado a uma plataforma de agentes.
- Cuidado com dados: recuperação de banco corrompido, controle de crescimento de histórico e alertas sem duplicação.

## Limites declarados

É uma ferramenta de pesquisa e de estudo de forward-test, sem promessa de resultado financeiro. A licença da base é não comercial, então o Orbit aparece aqui como projeto de engenharia e pesquisa.
