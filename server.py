"""Static server + Groq proxy + Google Sheets proxy. Run: python server.py"""  
import json
import os
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

def _load_dotenv():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(p):
        return
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()
PORT = int(os.environ.get("PORT", "8080"))
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
SHEETS_URL = os.environ.get("GOOGLE_APPS_SCRIPT_URL", "")


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n) if n else b"{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json(400, {"error": "Invalid JSON"})
            return

        if self.path == "/api/chat":
            self._chat(data)
        elif self.path == "/api/booking":
            self._booking(data)
        else:
            self.send_error(404)

    def _json(self, code, obj):
        out = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def _chat(self, data):
        if not GROQ_KEY:
            self._json(500, {"error": "GROQ_API_KEY not set on server"})
            return
        payload = json.dumps({
            "model": data.get("model", "llama-3.3-70b-versatile"),
            "messages": data.get("messages", []),
            "temperature": data.get("temperature", 0.7),
            "max_tokens": data.get("max_tokens", 2048),
            "top_p": data.get("top_p", 0.9),
            "frequency_penalty": data.get("frequency_penalty", 0.2),
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                self._json(res.status, json.loads(res.read().decode()))
        except urllib.error.HTTPError as e:
            self._json(e.code, {"error": e.read().decode()[:500]})
        except Exception as e:
            self._json(502, {"error": str(e)})

    def _booking(self, data):
        if not SHEETS_URL or "YOUR_" in SHEETS_URL:
            self._json(200, {"status": "skipped", "ok": False})
            return
        payload = json.dumps(data).encode()
        req = urllib.request.Request(
            SHEETS_URL, data=payload,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                self._json(200, json.loads(res.read().decode()) or {"status": "success", "ok": True})
        except Exception as e:
            self._json(502, {"error": str(e), "ok": False})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"http://localhost:{PORT}/newbot.html")
    if not GROQ_KEY:
        print("WARN: set GROQ_API_KEY for AI chat")
    HTTPServer(("", PORT), Handler).serve_forever()
