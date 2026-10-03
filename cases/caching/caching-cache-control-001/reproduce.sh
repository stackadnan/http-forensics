#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py

for path in max-age no-store none; do
    echo "== two separate curl runs against /$path"
    curl -sS -i "http://127.0.0.1:$PORT/$path"
    curl -sS "http://127.0.0.1:$PORT/$path"
    echo
done
show_server_log
