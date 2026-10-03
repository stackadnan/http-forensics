#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py

# "X-Empty;" is curl's syntax for sending a header with an empty value.
curl -sS -i \
    -H 'X-Dup: a' -H 'X-Dup: b' \
    -H 'x-Odd-CaSe: yes' \
    -H 'X-Empty;' \
    "http://127.0.0.1:$PORT/"
show_server_log
