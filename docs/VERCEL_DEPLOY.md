# Deploy to Vercel (Client Demo)

Share a live URL with Mo so he can test the orchestrator in his browser.

## What Gets Deployed

| URL | What |
|-----|------|
| `https://your-app.vercel.app/` | Chat UI for client demo |
| `https://your-app.vercel.app/api/chat` | Orchestrator API (POST) |
| `https://your-app.vercel.app/api/health` | Status check (GET) |

The web UI calls the same `handle_message()` logic as `scripts/test_demo.py`.

## Prerequisites

- [Vercel account](https://vercel.com/signup) (free)
- [GitHub](https://github.com) account (recommended)
- Gemini or Groq API key

## Deploy Steps

### 1. Push to GitHub

```bash
cd coaches-curve-orchestrator
git init
git add .
git commit -m "Coaches Curve orchestrator demo"
git remote add origin https://github.com/YOUR_USERNAME/coaches-curve-orchestrator.git
git push -u origin main
```

### 2. Import on Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Framework Preset: **Other**
4. Root Directory: `.` (default)
5. Click **Deploy** (first deploy may fail without env vars — that's OK)

### 3. Add Environment Variables

In Vercel → Project → **Settings** → **Environment Variables**:

| Variable | Value | Required |
|----------|-------|----------|
| `LLM_PROVIDER` | `gemini` | Yes |
| `GEMINI_API_KEY` | your key from AI Studio | Yes |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Optional |
| `KNOWLEDGE_PROVIDER` | `local` | Optional |
| `BRAIN_DIR` | `brain` | Optional |
| `DEMO_PASSWORD` | e.g. `curve2026` | Optional — protects demo |

Apply to **Production**, **Preview**, and **Development**.

### 4. Redeploy

Vercel → **Deployments** → latest → **Redeploy**

### 5. Share with Client

Send Mo:
- **URL:** `https://your-app.vercel.app`
- **Password:** (if you set `DEMO_PASSWORD`)

Suggested message:
> "Here's a live prototype of the Coaches Curve orchestrator. Try the example chips or ask it to prep a strategy session. Production version swaps in Claude, GBrain, and Manus on DigitalOcean."

## Test Before Sharing

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Chat test
curl -X POST https://your-app.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is Curve Concierge for?"}'
```

## Local Preview (Optional)

Install Vercel CLI:

```bash
npm i -g vercel
cd coaches-curve-orchestrator
cp .env.example .env   # add your API key
vercel dev
```

Opens at `http://localhost:3000` with the same UI + API.

## Limitations (Prototype vs Production)

| On Vercel (demo) | Production (DigitalOcean) |
|------------------|---------------------------|
| Browser chat UI | Telegram + WhatsApp |
| Serverless (10–30s timeout) | Always-on processes |
| Local `brain/` files | GBrain with live updates |
| Gemini/Groq free API | Claude API |
| No Manus research | Manus autonomous tasks |

Tell Mo this is the **orchestration core** hosted for easy access. Full production moves to a DO droplet per his spec.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `API key not configured` | Add `GEMINI_API_KEY` in Vercel env vars, redeploy |
| 500 on `/api/chat` | Check Vercel → Functions → Logs |
| Timeout | Keep messages concise; upgrade Vercel plan for 30s limit |
| `brain/` empty | Ensure `brain/` is committed to git (not in .gitignore) |
