# Cache-Control on responses fetched by curl

`caching-cache-control-001`

## Question

Does curl reuse a response that the server marked `Cache-Control: max-age=3600`, or does each invocation reach the server?

## Why it matters

`Cache-Control` is an instruction to caches. Whether it has any effect depends on whether the client in use is a cache. Browsers and caching proxies are; a command-line tool or a bare HTTP library may not be. When reproducing a caching problem it matters which of these you are talking to.

## Setup

`server.py` serves three paths with different policies: `/max-age` (`max-age=3600`), `/no-store` (`no-store`) and `/none` (no `Cache-Control`). Each response body contains a per-path counter, and the server logs every request it receives.

Requires `python3` and `curl`.

## Reproduction

```sh
./reproduce.sh
```

The script runs curl twice against each path.

## Expected result

Expectation (not verified by this repository): the counter increases on every request for all three paths.

## Actual observation

Observed with the environment below: both requests to each path reached the server (`served_count=1` then `served_count=2`), including the `max-age=3600` path. The `Date` and `Server` headers and the port vary between runs.

This shows that curl 8.7.1 invoked this way does not cache. It says nothing about how a browser or a caching proxy treats the same responses.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
