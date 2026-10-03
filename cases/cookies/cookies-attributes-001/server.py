import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from serve import Handler, run


class CookieHandler(Handler):
    def do_GET(self):
        cookie = self.headers.get("Cookie")
        self.log(f"Cookie={cookie}")
        if self.path == "/login":
            self.reply(200, "logged in\n", headers=[
                ("Set-Cookie", "app_cookie=a; Path=/app; HttpOnly"),
                ("Set-Cookie", "secure_cookie=b; Path=/; Secure"),
                ("Set-Cookie", "root_cookie=c; Path=/"),
            ])
        else:
            self.reply(200, f"Cookie header received: {cookie}\n")


run(CookieHandler)
