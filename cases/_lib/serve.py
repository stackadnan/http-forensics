"""Small helpers for the local servers used by cases.

A case server is a plain http.server handler. `run` binds it to an
ephemeral port on 127.0.0.1, prints the port on stdout so reproduce.sh can
find it, and writes one line per request to stderr (see `log`).
"""

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    # Needed for the Connection and Content-Length behavior of HTTP/1.1.
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        pass

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8", "replace")

    def log(self, *details):
        parts = [f"{self.command} {self.path}", *details]
        print("  ".join(parts), file=sys.stderr, flush=True)

    def reply(self, status, body="", headers=()):
        data = body.encode("utf-8")
        self.send_response(status)
        for name, value in headers:
            self.send_header(name, value)
        if status != 304:
            self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if status != 304:
            self.wfile.write(data)


def run(handler_class):
    server = HTTPServer(("127.0.0.1", 0), handler_class)
    print(server.server_port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def redirect_server(status):
    """POST /submit answers with `status` and Location: /target.

    GET and POST on /target answer 200 and echo the method that arrived.
    """

    class RedirectHandler(Handler):
        def do_POST(self):
            body = self.read_body()
            if self.path == "/submit":
                self.log(f"body={body!r}", f"-> {status} Location: /target")
                self.reply(status, headers=[("Location", "/target")])
            else:
                self.log(f"body={body!r}")
                self.reply(200, f"method=POST body={body!r}\n")

        def do_GET(self):
            self.log()
            self.reply(200, "method=GET body=''\n")

    run(RedirectHandler)
