# Security policy

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private reporting instead: on the repository page go to **Security → Report a vulnerability**.

Include what you found, how to reproduce it and the version affected. Expect an acknowledgement within a few days; this is a small project maintained in spare time, so there is no fixed response SLA.

## What counts

The package only loads and validates `case.yaml` files, so relevant issues are things like unsafe YAML handling or path handling in the loader.

The case servers and `reproduce.sh` scripts are meant to be run locally. They bind to 127.0.0.1 and send no traffic to other hosts. A case that does otherwise, or that contains real credentials, cookies or tokens, is a bug worth reporting.
