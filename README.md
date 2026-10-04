# HTTP Forensics

A reproducible toolkit for investigating and documenting HTTP behavior.

HTTP Forensics is a collection of small, self-contained HTTP experiments. Each one starts from a concrete question ("does the client keep the POST after a 301?"), reproduces it against a local server, and records what was actually observed together with the environment it was observed in.

It is not an HTTP client, a mock server or an API test framework. The point is the written-down case, not the tooling around it.

## Why HTTP behavior can be surprising

The specification leaves room, history left more, and implementations filled in the rest. A few examples this repository covers:

- HTTP redirects: 301 and 302 were commonly implemented as "turn POST into GET", while 307 and 308 exist to forbid that. Clients differ, and so do their opt-out flags.
- HTTP caching: `Cache-Control` and `ETag` only matter to something that caches. A client that does not cache just ignores them.
- HTTP cookies: `Path`, `Secure` and `HttpOnly` are defined by RFC 6265, but clients treat plain-HTTP localhost differently from other hosts.
- HTTP headers: repeated headers, odd casing and empty values are legal, and different parsers handle them differently.

Blog posts and Stack Overflow answers state these as rules. Usually they are one client's behavior in one version. A case records which.

## What a forensic case is

A case follows one line of reasoning:

**Case → Experiment → Evidence → Observation**

- **Case**: a question, with metadata (`case.yaml`) and an explanation (`README.md`).
- **Experiment**: a script that sets up a local server and drives a real client against it.
- **Evidence**: what the script prints, including the requests the server saw.
- **Observation**: what you can conclude from that evidence, with the client, server and OS versions written next to it.

Expectations (from a specification, or from experience) are labelled as expectations. An observation is only written down after the case has been run.

## Layout

```
cases/
  redirects/      redirect-post-{301,302,303,307,308}-001
  caching/        caching-etag-304-001, caching-cache-control-001
  cookies/        cookies-attributes-001
  headers/        headers-duplicate-and-empty-001
  responses/      responses-content-type-mismatch-001
  _lib/           shared server and shell helpers
schemas/          JSON Schema for case.yaml
src/              case loading and validation
tests/            tests for the above, plus a check of every case in the repo
docs/             the case format
```

Each case directory contains `case.yaml`, `README.md`, `reproduce.sh` and the server it uses. The format is described in [docs/case-format.md](https://github.com/stackadnan/http-forensics/blob/main/docs/case-format.md). The `requests` category is reserved but has no cases yet.

## Installing from PyPI

`pip install http-forensics` installs only the case loader and validator (`http_forensics.cases`). The cases, servers and reproduction scripts are not part of the package; clone the repository to run them.

## Running a case

You need `python3` and the client the case uses (all current cases use `curl`). Servers listen on an ephemeral port on 127.0.0.1; nothing leaves the machine.

```sh
cases/redirects/redirect-post-301-001/reproduce.sh
```

The output starts with the tool versions, then the client's output, then the requests the server saw.

## Tests

The tests check the case format and every case in the repository. They need PyYAML, the only dependency.

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python -m unittest discover -s tests
```

## Contributing

The main contribution is: find one interesting HTTP behavior and turn it into a reproducible case. See [CONTRIBUTING.md](https://github.com/stackadnan/http-forensics/blob/main/CONTRIBUTING.md).

## License

MIT
