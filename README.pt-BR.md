# CRM + Chatbot WhatsApp com IA

> [English](README.md) | **Português (BR)**

CRM web com chatbot de WhatsApp integrado para uma concessionária de veículos.

> **Visão geral do case** - o código de produção é privado (projeto de cliente). Esta página
> documenta o problema, a arquitetura e as decisões de engenharia.

## O problema

A concessionária atendia todo lead de WhatsApp na mão: primeira resposta lenta, sem
qualificação, sem visibilidade de pipeline e o conhecimento preso no celular de uma
pessoa. O lead esfriava antes de alguém responder.

## A solução

- **Chatbot de WhatsApp com IA** que responde na hora, qualifica o lead e passa
  pro humano no momento certo.
- **Cadeia de fallback de LLM**: Groq (principal) -> Cloudflare Workers AI -> Gemini.
  Se um provedor falha ou limita, o próximo responde - o cliente nunca vê indisponibilidade.
- **Prompt editável pelo painel do CRM**, incluindo campo de "o que NÃO fazer" -
  o dono ajusta o comportamento do bot sem tocar em código.
- **Pipeline de vendas automático**: conversas criam e movem negócios entre etapas
  sem digitação manual.

## Arquitetura

```
WhatsApp <--> [ Ponte Baileys (Node.js) ] <--> [ Backend FastAPI ] <--> SQLite
                                                       |
                                       [ Roteador LLM: Groq -> CF Workers AI -> Gemini ]
                                                       |
                                              [ Painel CRM web ]
                                        (pipeline, editor de prompt, histórico)
```

Roda atrás de Nginx com PM2 e Docker; backups automatizados.

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python, FastAPI |
| Transporte WhatsApp | Baileys (ponte Node.js) |
| IA | Groq, Cloudflare Workers AI, Gemini (cadeia de fallback) |
| Banco | SQLite |
| Infra | Nginx, PM2, Docker, backups automatizados |

## Notas de engenharia

- **Fallback como feature de primeira classe**: a cadeia de LLM foi desenhada pra
  degradação graciosa - disponibilidade acima do pico de qualidade de um provedor só.
- **Segurança de sessão**: um número de WhatsApp mapeia pra exatamente uma sessão do
  bot; credenciais de sessão vivem fora do versionamento.
- **Controle do operador**: tudo que a IA pode (e não pode) dizer é configurável
  pelo cliente, não hardcoded.

## Status

Entregue e rodando no ambiente do cliente. Engenheiro único: backend, integração
de IA, ponte WhatsApp e infraestrutura.
