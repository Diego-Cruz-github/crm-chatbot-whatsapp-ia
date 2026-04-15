# CRM + WhatsApp Chatbot with AI

Web CRM with integrated WhatsApp chatbot for a vehicle dealership. AI-powered with automatic fallback between multiple LLM providers.

## Stack

- **Backend:** Python, FastAPI
- **WhatsApp:** Baileys (Node.js bridge)
- **AI:** Groq (primary), Cloudflare Workers AI (fallback), Gemini (last resort)
- **Database:** SQLite
- **Infra:** Nginx, Docker, PM2, automated backups
- **Monitoring:** 24/7 uptime with auto-recovery

## Features

- AI chatbot with editable prompt via CRM dashboard
- "What NOT to do" field for AI behavior control
- Automatic sales pipeline (never regresses)
- Signal detection (payment confirmation keywords)
- AI fallback: Groq -> Cloudflare -> Gemini (automatic)
- Remote QR code with auto-recovery
- Prompt read from database on every message (no restart needed)

## Scripts

- `scripts/health_check.py` - Service health monitoring
- `scripts/bridge_restart.py` - WhatsApp bridge safe restart procedure

---

*Private repository - client project*
