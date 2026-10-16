"""Offline web server skeleton for the Operations Evidence Tracer."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PAGE = """<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Offline Operations Evidence Tracer</title>
<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:3rem auto;padding:0 1rem;color:#172033}main{border:1px solid #d6dbe5;border-radius:12px;padding:2rem}code{background:#eef2f7;padding:.15rem .3rem;border-radius:4px}</style>
</head><body><main><h1>Operations Evidence Tracer</h1><p>Offline evidence trails for synthetic operational records.</p><p>Evidence storage and transaction analysis will appear here after M1.</p><p>Health endpoint: <code>/health</code></p></main></body></html>"""


class EvidenceTracerHandler(BaseHTTPRequestHandler):
    """Serve only local UI and diagnostic responses."""

    def do_GET(self):  # noqa: N802 - required HTTP handler spelling
        if self.path == "/health":
            self._send(200, b'{"status":"ok",' + '"mode":"offline"'.encode(), "application/json")
        elif self.path == "/":
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain; charset=utf-8")

    def _send(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A002
        """Suppress routine request logging for a quiet local demo."""


def run(host="127.0.0.1", port=8000):
    """Start the local-only server."""
    server = ThreadingHTTPServer((host, port), EvidenceTracerHandler)
    print(f"Serving Offline Operations Evidence Tracer at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

