"""Health check — GET /api/health"""

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            from src.config import config
            from src.knowledge import get_knowledge_store

            store = get_knowledge_store()
            sources = store.list_sources()

            import os
            payload = {
                "status": "ok",
                "llm_provider": config.LLM_PROVIDER,
                "knowledge_docs": len(sources),
                "api_key_configured": bool(
                    config.GEMINI_API_KEY if config.LLM_PROVIDER == "gemini" else config.GROQ_API_KEY
                ),
                "password_required": bool(os.getenv("DEMO_PASSWORD", "").strip()),
            }
            status = 200
        except Exception as e:
            payload = {"status": "error", "message": str(e)}
            status = 500

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))
