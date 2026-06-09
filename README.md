# Coaches Curve AI Orchestrator

A prototype AI orchestration system for **The Coaches Curve** — designed to demo for CEO's Little Helpers and adapt into production.

## What This Demo Does (Step 1)

- Stores Coaches Curve business knowledge in a local `brain/` folder
- Retrieves relevant context for any question or task
- Sends context + user message to a free LLM (Gemini or Groq)
- Returns grounded answers about the business

**Step 2** adds a web chat UI deployable to **Vercel** for client demos.

## Deploy for Client Demo (Vercel)

```bash
# Push to GitHub, import on vercel.com, add GEMINI_API_KEY env var
# Full guide: docs/VERCEL_DEPLOY.md
```

Your client gets a live URL like `https://your-app.vercel.app` — no install needed.

## Quick Start

```bash
# 1. Clone / enter project
cd coaches-curve-orchestrator

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY (see docs/SETUP.md)

# 4. Test knowledge + LLM
python scripts/test_demo.py
```

## Project Structure

```
coaches-curve-orchestrator/
├── brain/                  # Knowledge base (→ GBrain in production)
│   ├── methodology/        # C.O.A.C.H.E.S. Curve framework
│   ├── offers/             # Accelerator, Concierge, equity
│   ├── sales/              # ICP, objections, qualification
│   └── sops/               # Delivery workflows
├── src/
│   ├── config.py           # Environment configuration
│   ├── knowledge/          # Knowledge layer (swappable)
│   ├── llm/                # LLM providers (swappable)
│   └── orchestrator/       # Intent routing + response logic
├── api/
│   ├── chat.py             # Vercel serverless — POST /api/chat
│   └── health.py           # GET /api/health
├── public/
│   ├── index.html          # Client demo chat UI
│   ├── style.css
│   └── app.js
├── scripts/
│   └── test_demo.py        # Verify everything works
├── vercel.json
└── docs/
    ├── ARCHITECTURE.md     # System design
    ├── SETUP.md            # Install guide
    └── PRODUCTION_MIGRATION.md  # Upgrade path
```

## LLM Provider Recommendation

| Provider | Best for | Free tier |
|----------|----------|-----------|
| **Gemini** (default) | Business copy, long context | [Google AI Studio](https://aistudio.google.com/apikey) |
| **Groq** | Fast responses, fallback | [Groq Console](https://console.groq.com/keys) |

Set `LLM_PROVIDER=gemini` or `LLM_PROVIDER=groq` in `.env`.

## Build Phases

| Phase | Status | What |
|-------|--------|------|
| **Step 1** | ✅ Now | Knowledge base + LLM + test script |
| **Step 2** | ✅ Now | Web chat UI + Vercel deploy |
| **Step 3** | After | Lead prep demo workflow |
| **Production** | Later | Manus, Claude, GBrain, n8n, DigitalOcean |

See [docs/PRODUCTION_MIGRATION.md](docs/PRODUCTION_MIGRATION.md) for the full upgrade path.

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Production Migration](docs/PRODUCTION_MIGRATION.md)
- [Vercel Deploy (client demo)](docs/VERCEL_DEPLOY.md)
