import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from serve import Handler, run


class MismatchHandler(Handler):
    def do_GET(self):
        self.log()
        if self.path == "/json-as-text":
            self.reply(200, '{"status": "ok"}\n', headers=[("Content-Type", "text/plain")])
        elif self.path == "/html-as-json":
            self.reply(200, "<h1>not json</h1>\n", headers=[("Content-Type", "application/json")])
        else:
            self.reply(404)

    def do_POST(self):
        body = self.read_body()
        self.log(f"Content-Type={self.headers.get('Content-Type')}", f"body={body!r}")
        self.reply(200, "received\n")


run(MismatchHandler)
