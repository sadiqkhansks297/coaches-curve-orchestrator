# Production Migration Guide

This document maps every prototype component to its production replacement.

## Component Swap Table

| Prototype (Demo) | Production (Mo's Spec) | Migration effort |
|------------------|------------------------|------------------|
| `LocalKnowledgeStore` | GBrain (`gbrain serve --http`) | Medium — implement `GBrainStore` class |
| Gemini / Groq API | Claude API (Anthropic) | Low — implement `ClaudeProvider` class |
| Mock research agent | Manus API + webhooks | Medium — add `ManusClient` + webhook handler |
| Telegram polling script | n8n + Telegram webhook | Low — export n8n workflow |
| Local laptop | DigitalOcean Droplet | Low — `docker-compose up` on VPS |
| No HTTPS | Caddy reverse proxy + SSL | Low — add Caddyfile |
| Single Python process | Docker Compose stack | Low — already structured for this |

## Step-by-Step Production Upgrade

### Phase A: Swap LLM (when client provides Anthropic key)

```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
```

Implement `src/llm/claude.py` — same interface as `GeminiProvider`.

### Phase B: Swap Knowledge (deploy GBrain)

```bash
# On DigitalOcean droplet
gbrain init
gbrain serve --http --port 7333 --bind 0.0.0.0 --public-url https://brain.yourdomain.com
```

```env
KNOWLEDGE_PROVIDER=gbrain
GBRAIN_URL=https://brain.yourdomain.com
GBRAIN_TOKEN=gbrain_xxx
```

Implement `src/knowledge/gbrain_store.py` — calls GBrain MCP search API.

Migrate `brain/` markdown into GBrain:
```bash
for f in brain/**/*.md; do gbrain put_page "$f"; done
```

### Phase C: Add Manus Action Arm

```env
MANUS_API_KEY=xxx
```

1. Create `src/agents/manus_client.py`
2. Register webhook: `POST https://api.manus.ai/v2/webhook.create`
3. Add n8n workflow: Manus completion → format → Telegram

### Phase D: Deploy to DigitalOcean

```bash
# On droplet
git clone <repo>
cd coaches-curve-orchestrator
cp .env.example .env  # fill production keys
docker compose up -d
```

`docker-compose.yml` (production) will include:
- `orchestrator-api` (Python service)
- `n8n`
- `gbrain` + `postgres`
- `caddy` (SSL)

### Phase E: Add WhatsApp

Via n8n WhatsApp Business Cloud node — requires Meta Business verification.
Telegram remains primary; WhatsApp added as second channel.

## What Stays the Same

These do **not** need rewriting when going to production:

- `brain/` markdown content structure
- `src/orchestrator/router.py` intent logic
- System prompts in `src/orchestrator/prompts.py`
- Project folder layout
- Documentation

## Environment Progression

```
.env.prototype   →  Gemini + local brain + Telegram polling
.env.staging     →  Claude + GBrain local + n8n + Cloudflare tunnel
.env.production  →  Claude + GBrain on DO + Manus + n8n + Caddy SSL
```

Keep all three as templates for client handover.
