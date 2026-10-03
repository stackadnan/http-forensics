#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py
base="http://127.0.0.1:$PORT"

echo "== response: JSON body labelled text/plain"
curl -sS -i "$base/json-as-text"

echo
echo "== response: HTML body labelled application/json"
curl -sS -i "$base/html-as-json"

echo
echo "== request: curl -d with a JSON body and no explicit Content-Type"
curl -sS -d '{"status": "ok"}' "$base/submit"

echo "== request: same body with an explicit Content-Type"
curl -sS -H 'Content-Type: application/json' -d '{"status": "ok"}' "$base/submit"
show_server_log
