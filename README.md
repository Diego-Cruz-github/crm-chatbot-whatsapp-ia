# CRM + WhatsApp Chatbot with AI
> **English** | [Português (BR)](README.pt-BR.md)

Web CRM with an integrated WhatsApp chatbot for a vehicle dealership.

> **Case overview** - the production code is private (client engagement). This page
> documents the problem, the architecture and the engineering decisions.

## The problem

The dealership handled every WhatsApp lead by hand: slow first response, no
qualification, no pipeline visibility, and knowledge locked in one person's
phone. Leads cooled off before anyone replied.

## The solution

- **WhatsApp chatbot with AI** that answers immediately, qualifies the lead and
  hands over to a human at the right moment.
- **LLM fallback chain**: Groq (primary) -> Cloudflare Workers AI -> Gemini. If a
  provider fails or rate-limits, the next one answers - the customer never sees
  an outage.
- **Prompt editable from the CRM panel**, including a "what NOT to do" field -
  the owner tunes the bot's behavior without touching code.
- **Automatic sales pipeline**: conversations create and move deals through
  stages without manual data entry.

## Architecture

```
WhatsApp <--> [ Baileys bridge (Node.js) ] <--> [ FastAPI backend ] <--> SQLite
                                                       |
                                       [ LLM router: Groq -> CF Workers AI -> Gemini ]
                                                       |
                                              [ CRM web panel ]
                                        (pipeline, prompt editor, history)
```

Runs behind Nginx with PM2 and Docker; automated backups.

## Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| WhatsApp transport | Baileys (Node.js bridge) |
| AI | Groq, Cloudflare Workers AI, Gemini (fallback chain) |
| Database | SQLite |
| Infra | Nginx, PM2, Docker, automated backups |

## Engineering notes

- **Fallback as a first-class feature**: the LLM chain was designed for graceful
  degradation - availability over any single provider's quality peak.
- **Session safety**: one WhatsApp number maps to exactly one bot session;
  session credentials live outside version control.
- **Operator control**: everything the AI is allowed (and forbidden) to say is
  configurable by the client, not hardcoded.

## Status

Delivered and running in the client's environment. Sole engineer: backend,
AI integration, WhatsApp bridge and infrastructure.
