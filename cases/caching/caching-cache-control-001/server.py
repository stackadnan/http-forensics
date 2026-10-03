import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from serve import Handler, run
from collections import Counter

POLICIES = {
    "/max-age": "max-age=3600",
    "/no-store": "no-store",
    "/none": None,
}
hits = Counter()


class CacheControlHandler(Handler):
    def do_GET(self):
        policy = POLICIES.get(self.path)
        if self.path not in POLICIES:
            self.reply(404)
            return
        hits[self.path] += 1
        self.log(f"served_count={hits[self.path]}")
        headers = [("Cache-Control", policy)] if policy else []
        self.reply(200, f"served_count={hits[self.path]}\n", headers=headers)


run(CacheControlHandler)
