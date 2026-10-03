import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from serve import Handler, run

ETAG = '"v1"'


class EtagHandler(Handler):
    def do_GET(self):
        sent = self.headers.get("If-None-Match")
        self.log(f"If-None-Match={sent}")
        if sent == ETAG:
            self.reply(304, headers=[("ETag", ETAG)])
        else:
            self.reply(200, "resource body\n", headers=[("ETag", ETAG)])


run(EtagHandler)
