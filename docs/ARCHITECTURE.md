# Architecture

## Overview

The system follows a **layered, swappable** design so the prototype demo can upgrade to production without rewriting core logic.

```
┌─────────────────────────────────────────────────────────────┐
│                    CEO Interface Layer                       │
│   Prototype: Telegram bot (polling)                          │
│   Production: Telegram + WhatsApp via n8n webhooks           │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Orchestrator (router.py)                   │
│   - Classifies intent (question | lead_prep | draft)         │
│   - Pulls knowledge context                                  │
│   - Calls LLM with grounded prompt                           │
│   - Routes complex tasks to action arm (Manus in prod)       │
└───────┬──────────────────────────────┬──────────────────────┘
        │                              │
┌───────▼──────────┐          ┌────────▼─────────┐
│  Knowledge Layer │          │    LLM Layer      │
│  Prototype:      │          │  Prototype:       │
│  local markdown  │          │  Gemini / Groq    │
│  Production:     │          │  Production:      │
│  GBrain + MCP    │          │  Claude API       │
└──────────────────┘          └──────────────────┘
                                        │
                               ┌────────▼─────────┐
                               │   Action Arm      │
                               │  Prototype:       │
                               │  mock research    │
                               │  Production:      │
                               │  Manus API        │
                               └──────────────────┘
```

## Layers

### 1. Knowledge Layer (`src/knowledge/`)

**Purpose:** Persistent memory of everything about The Coaches Curve.

| Mode | Implementation | When |
|------|----------------|------|
| Prototype | `LocalKnowledgeStore` — markdown files in `brain/` | Demo |
| Production | `GBrainStore` — GBrain MCP/HTTP API | Client engagement |

**Interface:** `KnowledgeStore.search(query) → str`

### 2. LLM Layer (`src/llm/`)

**Purpose:** Language generation — answers, briefs, drafts.

| Mode | Implementation | When |
|------|----------------|------|
| Prototype | Gemini or Groq (free API) | Demo |
| Production | Claude API (Anthropic) | Client engagement |

**Interface:** `LLMProvider.generate(system, user) → str`

### 3. Orchestrator (`src/orchestrator/`)

**Purpose:** Routes messages, builds prompts, coordinates layers.

**Intents (prototype):**
- `question` — general business Q&A
- `lead_prep` — strategy session briefing

**Intents (production, later):**
- `framework_extract` — Concierge midpoint delivery
- `milestone_check` — client retention
- `draft_message` — follow-up emails

### 4. Interface Layer (Step 2+)

**Prototype:** Python Telegram polling loop in `scripts/telegram_bot.py`

**Production:** n8n webhooks on DigitalOcean droplet

## Data Flow: Lead Prep (Target Demo)

```
Mo (Telegram): "Prep call with Sarah, business coach, can't explain her method"
       │
       ▼
Orchestrator.classify() → intent: lead_prep
       │
       ├── knowledge.search("ideal client qualification")
       ├── knowledge.search("strategy session prep")
       ├── research_agent.run(name, role, notes)   [mock → Manus]
       └── llm.generate(system + context + research)
       │
       ▼
Telegram: 1-page strategy session brief
```

## Hosting

| Mode | Where | Public URL |
|------|-------|------------|
| Prototype | Your laptop | Not required (polling) |
| Demo with webhooks | Laptop + Cloudflare Tunnel | Free |
| Production | DigitalOcean Droplet | Client domain + SSL |

## Design Principles

1. **Swappable providers** — change LLM or knowledge via `.env`, not code rewrites
2. **Grounded responses** — always inject brain context before LLM call
3. **Honest prototyping** — mock Manus clearly; swap to real API in production
4. **Document everything** — every layer has a migration path in `PRODUCTION_MIGRATION.md`
