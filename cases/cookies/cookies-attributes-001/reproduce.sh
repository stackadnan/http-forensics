#!/bin/sh
cd "$(dirname "$0")"
. ../../_lib/common.sh

print_environment
start_server server.py
base="http://127.0.0.1:$PORT"
jar="$WORK_DIR/cookies.txt"

echo "== GET /login (curl -c stores cookies in a jar)"
curl -sS -i -c "$jar" "$base/login"

echo
echo "== cookie jar"
cat "$jar"

for path in /app/page /other; do
    echo
    echo "== GET $path with the jar (curl -b)"
    curl -sS -b "$jar" "$base$path"
done
show_server_log
