# POST followed by a 303 See Other

`redirect-post-303-001`

## Question

Does curl preserve the POST method, and the request body, after a 303 redirect?

## Why it matters

303 is the status meant for 'the result of your POST is over there, fetch it with GET'. RFC 9110 (section 15.4.4) says a user agent can follow it with a retrieval request (GET or HEAD), and that it is primarily used to send the user agent from the result of a POST to a separate resource.

Code that POSTs through a redirect (form submissions, webhooks, API calls behind a URL change) can silently turn into a GET without the body. The server then sees a different request than the one the client sent.

## Setup

`server.py` listens on an ephemeral port on 127.0.0.1. `POST /submit` answers `303 See Other` with `Location: /target`. `/target` answers 200 and echoes the method and body it received. Every request the server sees is logged.

Requires `python3` and `curl`. No network access beyond loopback.

## Reproduction

```sh
./reproduce.sh
```

The script sends `curl -L -d name=forensics` twice: once with default options and once with `--post303`. After each run it prints the requests the server saw.

## Expected result

Expectation (not verified by this repository): by default curl follows the redirect with GET and no body; with `--post303` it re-sends POST with the body. See RFC 9110 section 15.4 for what the specification allows.

## Actual observation

Observed with the environment below.

| curl options | request to `/submit` | request to `/target` |
| --- | --- | --- |
| `-L -d name=forensics` | POST, body `name=forensics` | GET, no body |
| `-L --post303 -d name=forensics` | POST, body `name=forensics` | POST, body `name=forensics` |

This describes curl 8.7.1 only. It says nothing about browsers or other HTTP libraries.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
