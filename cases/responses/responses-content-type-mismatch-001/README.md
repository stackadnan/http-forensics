# Content-Type that does not match the body

`responses-content-type-mismatch-001`

## Question

What does curl do when the `Content-Type` of a response disagrees with its body, and which `Content-Type` does it attach to a JSON body sent with `-d`?

## Why it matters

`Content-Type` is metadata that the receiver may or may not trust. Servers that parse bodies by label, and clients that decode by label, break differently when the label is wrong. A wrong label on a request is also a common cause of "my JSON arrives as a form" bugs.

## Setup

`server.py` has two response endpoints that lie about the body (`/json-as-text`: JSON labelled `text/plain`; `/html-as-json`: HTML labelled `application/json`) and a `POST /submit` endpoint that logs the `Content-Type` and body it receives.

Requires `python3` and `curl`.

## Reproduction

```sh
./reproduce.sh
```

## Expected result

Expectation (not verified by this repository): curl prints both bodies untouched. A POST with `-d` and no explicit header is labelled `application/x-www-form-urlencoded`.

## Actual observation

Observed with the environment below:

- Both mismatched responses were printed unchanged, with the wrong `Content-Type` visible in the headers.
- `curl -d '{"status": "ok"}'` sent `Content-Type: application/x-www-form-urlencoded`.
- Adding `-H 'Content-Type: application/json'` replaced it with `application/json`; the body was identical.

This is curl 8.7.1 behavior. Browsers sniff and enforce content types in ways curl does not, so this case does not describe browser behavior.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
