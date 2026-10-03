# ETag validator and a 304 Not Modified response

`caching-etag-304-001`

## Question

When a client sends `If-None-Match` with the ETag it was given, does the server answer `304 Not Modified` without a body, and what does curl show for it?

## Why it matters

Conditional requests let a cache revalidate a stored response without downloading it again. Bugs here are quiet: a server that ignores `If-None-Match`, or a 304 that carries a body or lacks the validator, still "works" but wastes bandwidth or confuses caches. This case makes the exchange visible on the wire.

## Setup

`server.py` serves `/resource` with `ETag: "v1"`. If the request carries `If-None-Match: "v1"` it answers 304 with the `ETag` header and no body; otherwise it answers 200 with a body. The server is a fixture written for this case, so it shows what a server *can* do, not what any particular production server does.

Requires `python3` and `curl`.

## Reproduction

```sh
./reproduce.sh
```

Three requests: a plain GET, a GET with the ETag from the first response, and a GET with a different validator.

## Expected result

Expectation (not verified by this repository): request 2 gets 304 with no body, request 3 gets 200 with the body.

## Actual observation

Observed with the environment below:

1. Plain GET: `200 OK`, `ETag: "v1"`, 14-byte body.
2. `If-None-Match: "v1"`: `304 Not Modified`, `ETag: "v1"`, no body, no `Content-Length`.
3. `If-None-Match: "other"`: `200 OK` with the full body.

Because this is a hand-written fixture, it records how the fixture behaves and how curl displays the exchange. It is not a finding about caches or real servers.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
