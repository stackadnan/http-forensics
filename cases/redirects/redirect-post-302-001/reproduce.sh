#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py

echo "== curl -L -d name=forensics (default)"
curl -sS -L -d name=forensics "http://127.0.0.1:$PORT/submit"
show_server_log

reset_server_log
echo
echo "== curl -L --post302 -d name=forensics"
curl -sS -L --post302 -d name=forensics "http://127.0.0.1:$PORT/submit"
show_server_log
