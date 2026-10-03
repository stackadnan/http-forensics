# Shared helpers for reproduce.sh scripts. Source this file, do not execute it.
#
#   . ../../_lib/common.sh
#   start_server server.py     # sets PORT, starts the server in the background
#   ... run the client against http://127.0.0.1:$PORT ...
#   show_server_log            # prints what the server saw
#   reset_server_log           # forget what it saw so far
#
# Servers bind 127.0.0.1 on an ephemeral port and never talk to the network.

set -eu

WORK_DIR=$(mktemp -d)
SERVER_LOG="$WORK_DIR/server.log"
SERVER_PID=

cleanup() {
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

start_server() {
    python3 -u "$1" >"$WORK_DIR/port" 2>>"$SERVER_LOG" &
    SERVER_PID=$!
    tries=0
    while [ ! -s "$WORK_DIR/port" ]; do
        tries=$((tries + 1))
        if [ "$tries" -gt 50 ]; then
            echo "server did not start" >&2
            cat "$SERVER_LOG" >&2
            exit 1
        fi
        sleep 0.1
    done
    PORT=$(head -n 1 "$WORK_DIR/port")
}

reset_server_log() {
    : >"$SERVER_LOG"
}

show_server_log() {
    echo
    echo "== requests seen by the server"
    cat "$SERVER_LOG"
}

print_environment() {
    echo "== environment"
    curl --version | head -n 1
    python3 --version
    uname -sr
    echo
}
