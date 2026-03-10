"""
Discord Interactions API endpoint for Vercel serverless.
Discord sends POST requests here when users use slash commands.
"""
import json
import os
from http.server import BaseHTTPRequestHandler

try:
    import nacl.encoding
    import nacl.signing
except ImportError:
    nacl = None

# Import shared calculator logic (path works from project root on Vercel)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.calculator import (
    calculate_lot_size,
    build_lot_embed,
    build_pairs_embed,
    build_quick_embed,
)


def verify_discord_request(body: bytes, signature: str, timestamp: str, public_key: str) -> bool:
    """Verify Discord interaction signature (ed25519)."""
    if not nacl:
        return False
    try:
        message = timestamp.encode() + body
        verify_key = nacl.signing.VerifyKey(public_key.encode("utf-8"), encoder=nacl.encoding.HexEncoder)
        verify_key.verify(message, bytes.fromhex(signature))
        return True
    except Exception:
        return False


def get_option(data: dict, name: str):
    """Get option value from interaction data options list."""
    options = data.get("options") or []
    for opt in options:
        if opt.get("name") == name:
            return opt.get("value")
    return None


def handle_lot(data: dict) -> dict:
    """Handle /lot command. Returns response payload."""
    acc_size = get_option(data, "acc_size")
    risk = get_option(data, "risk")
    pair = get_option(data, "pair")
    sl = get_option(data, "sl")

    if acc_size is None or risk is None or pair is None or sl is None:
        return {
            "type": 4,
            "data": {"content": "❌ Missing parameters. Use: acc_size, risk, pair, sl", "flags": 64},
        }
    if risk > 20:
        return {"type": 4, "data": {"content": "❌ Risk should not exceed 20%!", "flags": 64}}
    if sl <= 0:
        return {"type": 4, "data": {"content": "❌ Stop loss must be greater than 0!", "flags": 64}}

    lot_size, risk_amount, _ = calculate_lot_size(acc_size, risk, sl, pair)
    embed = build_lot_embed(acc_size, risk, pair, sl, lot_size, risk_amount)
    return {"type": 4, "data": {"embeds": [embed]}}


def handle_pairs() -> dict:
    """Handle /pairs command."""
    embed = build_pairs_embed()
    return {"type": 4, "data": {"embeds": [embed]}}


def handle_quick() -> dict:
    """Handle /quick command."""
    embed = build_quick_embed()
    return {"type": 4, "data": {"embeds": [embed]}}


def handle_interaction(payload: dict) -> dict:
    """Route interaction to the right handler. Returns response dict."""
    t = payload.get("type")
    if t == 1:
        return {"type": 1}  # PING -> PONG
    if t != 2:
        return {"type": 4, "data": {"content": "Unknown interaction type", "flags": 64}}

    data = payload.get("data", {})
    name = data.get("name", "")
    if name == "lot":
        return handle_lot(data)
    if name == "pairs":
        return handle_pairs()
    if name == "quick":
        return handle_quick()
    return {"type": 4, "data": {"content": f"Unknown command: {name}", "flags": 64}}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Accept /api/interactions (Vercel may send path with or without trailing slash)
        path = self.path.split("?")[0].rstrip("/")
        if not path.endswith("interactions"):
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""

        signature = self.headers.get("X-Signature-Ed25519", "")
        timestamp = self.headers.get("X-Signature-Timestamp", "")
        public_key = os.environ.get("DISCORD_PUBLIC_KEY", "").strip()

        if not public_key:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "DISCORD_PUBLIC_KEY not set"}).encode())
            return

        if not verify_discord_request(body, signature, timestamp, public_key):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid signature"}).encode())
            return

        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        response = handle_interaction(payload)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"ok": True, "message": "CULT TRADERS CALCULATOR - use Discord slash commands"}).encode()
        )
