# POST followed by a 308 Permanent Redirect

`redirect-post-308-001`

## Question

Does curl preserve the POST method, and the request body, after a 308 redirect?

## Why it matters

RFC 7538 defines 308 as 301 "except that it does not allow changing the request method from POST to GET" (see also RFC 9110, section 15.4.9). Comparing it with the 301, 302 and 303 cases shows which status code a server has to use when the client must repeat the POST.

## Setup

`server.py` listens on an ephemeral port on 127.0.0.1. `POST /submit` answers `308 Permanent Redirect` with `Location: /target`. `/target` answers 200 and echoes the method and body it received. Every request the server sees is logged.

Requires `python3` and `curl`. No network access beyond loopback.

## Reproduction

```sh
./reproduce.sh
```

## Expected result

Expectation (not verified by this repository): curl re-sends POST with the same body to `/target`.

## Actual observation

Observed with the environment below: the server received `POST /submit` with body `name=forensics`, then `POST /target` with body `name=forensics`. No special curl option was needed.

This describes curl 8.7.1 only.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
