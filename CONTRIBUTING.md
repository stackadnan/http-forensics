# Contributing

The most useful contribution is one interesting HTTP behavior turned into a reproducible case. You do not need to read the source to add one: a case is a directory of plain files.

## Adding a case

1. Pick a question you can answer with a local server and a real client. "Does X do Y when Z?" works well. If you can only answer it against a live third-party service, it does not belong here.
2. Create `cases/<category>/<id>/`. The id is lowercase words ending in a three-digit number (`cookies-samesite-001`). The category is one of `redirects`, `cookies`, `caching`, `headers`, `requests`, `responses`.
3. Add `case.yaml`. Copy an existing one; the fields are listed in [docs/case-format.md](docs/case-format.md).
4. Add `server.py`. Plain `http.server` is enough. `cases/_lib/serve.py` has a small base handler, and the existing cases show how it is used.
5. Add `reproduce.sh` (and `chmod +x` it). Source `cases/_lib/common.sh`, start the server, run the client, print the requests the server saw.
6. Run it. Look at the output.
7. Write `README.md` with the sections listed in the case format doc. Put the result under "Actual observation" together with the client, server and OS versions.
8. Run the tests and open a pull request.

```sh
.venv/bin/python -m unittest discover -s tests
```

## Ground rules

- **Local only.** Servers bind 127.0.0.1. If a case genuinely needs external connectivity, say so prominently in its README.
- **Observation is not a rule.** Say whose behavior you saw: the client, the server, a proxy, your OS. Do not write "HTTP does X" when you tested one curl version.
- **Expectations are labelled.** What the RFC says, or what you assumed before running, goes under "Expected result" and in `expected:` in `case.yaml`.
- **No real secrets.** Cookies, tokens and passwords in a case must be synthetic. Do not paste output captured from real accounts.
- **Do not fill in observations you did not make.** If you could not run a client, leave that part out and say so.
- **Keep it small.** One question per case.

## Code changes

Changes to the loader, validator or schema need tests. Keep dependencies to the minimum; the standard library is preferred.
