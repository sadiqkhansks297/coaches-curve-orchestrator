"""
Vercel serverless API — chat endpoint.

POST /api/chat
Body: { "message": "your question or instruction" }
Response: { "reply": "...", "intent": "question|lead_prep" }
"""

import json
import sys
import traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Ensure project root is on Python path (Vercel serverless)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _cors_headers(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        _cors_headers(self)
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            message = (data.get("message") or "").strip()
            if not message:
                self._json_response(400, {"error": "message is required"})
                return

            # Optional demo password (set DEMO_PASSWORD in Vercel env)
            import os
            demo_password = os.getenv("DEMO_PASSWORD", "").strip()
            if demo_password:
                auth = self.headers.get("Authorization", "")
                token = (
                    auth.replace("Bearer ", "").strip()
                    if auth.startswith("Bearer ")
                    else str(data.get("password", "")).strip()
                )
                if token != demo_password:
                    self._json_response(401, {"error": "Invalid demo password"})
                    return

            from src.orchestrator import classify_intent, handle_message

            intent = classify_intent(message)
            reply = handle_message(message)

            self._json_response(200, {"reply": reply, "intent": intent})

        except ValueError as e:
            self._json_response(400, {"error": str(e)})
        except Exception as e:
            traceback.print_exc()
            self._json_response(500, {"error": f"Orchestrator error: {str(e)}"})

    def _json_response(self, status: int, payload: dict) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        _cors_headers(self)
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))
