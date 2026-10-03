#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py
url="http://127.0.0.1:$PORT/resource"

echo "== 1. plain GET"
curl -sS -i "$url"

etag=$(curl -sS -D - -o /dev/null "$url" | tr -d '\r' | sed -n 's/^[Ee][Tt]ag: //p')
reset_server_log

echo
echo "== 2. conditional GET with If-None-Match: $etag"
curl -sS -i -H "If-None-Match: $etag" "$url"

echo
echo "== 3. conditional GET with a different validator"
curl -sS -i -H 'If-None-Match: "other"' "$url"
show_server_log
