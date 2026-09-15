"""
app.py — Minimal HTTP server for the Supply Chain MVP.

Serves:
  GET /              → dashboard.html
  GET /login         → login.html
  GET /api/status    → JSON snapshot from engine.run_all()

Run with:
  python src/app.py

No external dependencies — Python stdlib only.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# Allow running as: python src/app.py (adds src/ to the path)
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import data  # noqa: E402
import engine  # noqa: E402

_DASHBOARD_PATH = os.path.join(_SRC_DIR, "dashboard.html")
_LOGIN_PATH     = os.path.join(_SRC_DIR, "login.html")
_PORT = int(os.environ.get("APP_PORT", 8000))


class SupplyChainHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file(_DASHBOARD_PATH)
        elif self.path == "/login":
            self._serve_file(_LOGIN_PATH)
        elif self.path == "/api/status":
            self._serve_status()
        else:
            self._send_404()

    # ── Route handlers ─────────────────────────────────────────────────────

    def _serve_file(self, path):
        try:
            with open(path, "rb") as f:
                body = f.read()
            self._respond(200, "text/html; charset=utf-8", body)
        except FileNotFoundError:
            name = os.path.basename(path)
            self._respond(500, "text/plain; charset=utf-8", f"{name} not found".encode())

    def _serve_status(self):
        shipments = data.generate_shipments()
        fleet = data.generate_fleet()
        result = engine.run_all(shipments, fleet)
        body = json.dumps(result, indent=2).encode("utf-8")
        self._respond(200, "application/json; charset=utf-8", body)

    def _send_404(self):
        self._respond(404, "text/plain; charset=utf-8", b"Not found")

    # ── Low-level helpers ──────────────────────────────────────────────────

    def _respond(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # override to add cleaner output
        print(f"  {self.address_string()} - {fmt % args}")


def run():
    server = HTTPServer(("", _PORT), SupplyChainHandler)
    print(f"Supply Chain MVP running at http://localhost:{_PORT}")
    print(f"  Dashboard : http://localhost:{_PORT}/")
    print(f"  API       : http://localhost:{_PORT}/api/status")
    print("Press Ctrl-C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
