# Repeated, mixed-case and empty headers

`headers-duplicate-and-empty-001`

## Question

Are repeated headers, unusual header-name casing and empty header values preserved in both directions between curl and Python's `http.server`?

## Why it matters

Header names are case-insensitive and a repeated header can usually be combined into a comma-separated list, but not every field allows that (`Set-Cookie` is the well-known exception). Code that reads headers into a plain dictionary may lose information. Knowing what actually crosses the wire helps tell a client problem from a parsing problem in the receiving code.

## Setup

curl sends `X-Dup` twice, `x-Odd-CaSe`, and an empty `X-Empty` (curl's `-H 'X-Empty;'` syntax). The server logs and echoes the request header lines in the order its parser reports them, and replies with `X-Dup` twice, `x-MiXeD-cAsE` and an empty `X-Empty`.

Requires `python3` and `curl`. The `Host` port and `Date` vary between runs.

## Reproduction

```sh
./reproduce.sh
```

## Expected result

Expectation (not verified by this repository): all fields arrive as sent in both directions.

## Actual observation

Observed with the environment below:

- Request, as listed by the server: both `X-Dup` lines, `x-Odd-CaSe: yes` and `X-Empty:` arrived with the casing curl sent.
- Response, as printed by `curl -i`: both `X-Dup` lines, `x-MiXeD-cAsE: kept?` and `X-Empty:` were shown as the server wrote them.

The server side is Python's `http.server` parser listing `self.headers.items()`, so this reflects that parser and curl 8.7.1 over HTTP/1.1, not servers or clients in general. It also says nothing about what proxies do to the same fields.

## Environment

Observed on one machine; other clients, versions and platforms may differ.

- curl 8.7.1 (x86_64-apple-darwin25.0, libcurl/8.7.1, SecureTransport)
- Python 3.14.7 (server)
- Darwin 25.6.0
- HTTP/1.1 over loopback, no proxy
