# Case format (schema_version 1)

A case is a directory containing a `case.yaml`, a `README.md`, and whatever the reproduction needs:

```
cases/<category>/<id>/
  case.yaml
  README.md
  reproduce.sh
  server.py
```

The directory name must equal the case `id`, and the parent directory must equal the `category`. `python3 -m unittest discover -s tests` checks this for every case.

## Example

```yaml
schema_version: 1
id: redirect-post-301-001
title: POST followed by a 301 redirect
category: redirects

question: >-
  Does curl preserve the POST method, and the request body, after a 301 redirect?

tags:
  - redirects
  - post
  - status-301

protocol:
  - http/1.1

clients:
  - curl

servers:
  - python-http.server

environment:
  requires:
    - python3
    - curl

reproduce: reproduce.sh

expected: >-
  curl -L is expected to follow the 301 with GET and no body.
```

## Fields

| Field | Required | Notes |
| --- | --- | --- |
| `schema_version` | yes | Always `1` for this format. |
| `id` | yes | Lowercase words separated by `-`, ending in a three-digit number: `cookies-attributes-001`. Unique across the repository. |
| `title` | yes | Short, non-empty string. |
| `question` | yes | The single question the case investigates. |
| `category` | yes | One of `redirects`, `cookies`, `caching`, `headers`, `requests`, `responses`. |
| `tags` | yes | Lowercase strings (`a-z`, `0-9`, `.`, `-`). Quote or prefix numeric tags: a bare `301` is read by YAML as a number, so use `status-301`. |
| `protocol` | yes | `http/1.0` and/or `http/1.1`. Other versions are not supported by this format yet. |
| `clients` | yes | The client programs the case exercises, for example `curl`. |
| `servers` | yes | The server implementations used, for example `python-http.server`. |
| `environment.requires` | yes | Programs that must be on `PATH` to reproduce the case. |
| `reproduce` | yes | Path of the entry point script, relative to the case directory. Must exist. |
| `expected` | no | What you expect to happen, where it is known. This is an expectation, not an observation. Observations belong in the README, together with the environment they came from. |

Unknown fields are rejected so typos do not pass silently.

`schemas/case.schema.json` is a JSON Schema description of the same format for editors and other tooling. The Python validator in `src/http_forensics/cases.py` is what the tests use, and a test checks that the two agree on the enumerations and field lists.

## Case README

Every case README has these sections:

1. Question
2. Why it matters
3. Setup
4. Reproduction
5. Expected result
6. Actual observation
7. Environment

Actual observations must come from running the case. Write down the client and server versions and the OS you ran it on, and state which part of the result is client behavior, server behavior or a property of your environment. If you could not run the case, say so under "Actual observation" instead of filling it in.
