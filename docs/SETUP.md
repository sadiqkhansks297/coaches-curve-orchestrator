# Setup Guide

## Prerequisites

- Python 3.10+
- A free API key from **one** of:
  - [Google AI Studio](https://aistudio.google.com/apikey) (recommended)
  - [Groq Console](https://console.groq.com/keys) (alternative)

## Step-by-Step Install

### 1. Create virtual environment

```bash
cd coaches-curve-orchestrator
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get a free Gemini API key (recommended)

1. Go to https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click **Create API key**
4. Copy the key

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=paste-your-key-here
GEMINI_MODEL=gemini-2.0-flash
KNOWLEDGE_PROVIDER=local
BRAIN_DIR=brain
```

### 4. Verify knowledge base loads

```bash
python scripts/test_demo.py --knowledge-only
```

Expected output: list of brain files + search results for sample queries.

### 5. Verify LLM responds

```bash
python scripts/test_demo.py
```

Expected: grounded answer about Coaches Curve using brain context.

## Switching to Groq

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key
GROQ_MODEL=llama-3.3-70b-versatile
```

No code changes needed — provider is swappable via config.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `GEMINI_API_KEY not set` | Copy `.env.example` → `.env` and add key |
| `No brain files found` | Run from project root; check `brain/` exists |
| Gemini 429 rate limit | Wait 60s or switch to Groq |
| Import errors | Activate venv: `source .venv/bin/activate` |

## Next Step

Once `test_demo.py` passes → proceed to **Step 2: Telegram bot** (see README).
