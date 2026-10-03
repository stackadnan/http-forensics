import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from serve import Handler, run


class HeaderHandler(Handler):
    def do_GET(self):
        received = [f"{name}: {value}" for name, value in self.headers.items()]
        self.log(*[f"[{line}]" for line in received])
        self.reply(200, "\n".join(received) + "\n", headers=[
            ("X-Dup", "one"),
            ("X-Dup", "two"),
            ("x-MiXeD-cAsE", "kept?"),
            ("X-Empty", ""),
        ])


run(HeaderHandler)
