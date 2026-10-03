# Set-Cookie Path, Secure and HttpOnly in curl's cookie jar

`cookies-attributes-001`

## Question

Which cookies does curl send back when the server sets one with `Path=/app`, one with `Secure`, and one with no restrictions?

## Why it matters

Cookie attributes decide where a cookie goes, and the rules differ between the specification (RFC 6265), browsers and other clients. Plain-HTTP local test setups are a common place where `Secure` cookies behave differently from production.

## Setup

`GET /login` sets three cookies:

- `app_cookie=a; Path=/app; HttpOnly`
- `secure_cookie=b; Path=/; Secure`
- `root_cookie=c; Path=/`

Every other path echoes the `Cookie` request header it received. The values are synthetic; never reuse this pattern with real session identifiers in a case.

Requires `python3` and `curl`. The server is on `http://127.0.0.1`, not HTTPS.

## Reproduction

```sh
./reproduce.sh
```

curl logs in with a cookie jar (`-c`), prints the jar, then requests `/app/page` and `/other` with it (`-b`).

## Expected result

Expectation (not verified by this repository): `/app/page` receives `app_cookie` and `root_cookie`; `/other` receives only `root_cookie`. Whether `secure_cookie` is sent over plain HTTP is the open question.

## Actual observation

Observed with the environment below:

- The jar stored all three cookies. `HttpOnly` shows up as a `#HttpOnly_` prefix on the domain in curl's jar file, and `Secure` as `TRUE` in the secure column.
- `GET /app/page` sent `app_cookie`, `secure_cookie` and `root_cookie`.
- `GET /other` sent `secure_cookie` and `root_cookie`.

So curl 8.7.1 sent the `Secure` cookie over plain HTTP to 127.0.0.1. This case does not establish why; it could be a localhost exception or another detail of this curl build. Do not generalize it to other hosts, curl versions or browsers.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
