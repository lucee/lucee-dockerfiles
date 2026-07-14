#!/bin/sh
set -e

LUCEE_SERVER_DIR="${LUCEE_SERVER_DIR:-/opt/lucee/server}"
LUCEE_RUNTIME_DIR="${LUCEE_RUNTIME_DIR:-}"

if [ -n "$LUCEE_RUNTIME_DIR" ] && [ "$LUCEE_RUNTIME_DIR" != "$LUCEE_SERVER_DIR" ]; then
    START=$(date +%s%N)
    mkdir -p "$LUCEE_RUNTIME_DIR/lucee-server"
    cp -a "$LUCEE_SERVER_DIR/lucee-server/." "$LUCEE_RUNTIME_DIR/lucee-server/"
    rm -rf "$LUCEE_RUNTIME_DIR/lucee-server/felix-cache"
    END=$(date +%s%N)
    # Write to stderr (unbuffered) rather than stdout (block-buffered when
    # connected to a pipe) so the message survives the subsequent `exec`
    # that replaces this shell with Tomcat.
    echo "Seeded LUCEE_RUNTIME_DIR ($LUCEE_RUNTIME_DIR) from LUCEE_SERVER_DIR ($LUCEE_SERVER_DIR) in $(( (END - START) / 1000000 ))ms" >&2
    export LUCEE_SERVER_DIR="$LUCEE_RUNTIME_DIR"
fi

exec "$@"
