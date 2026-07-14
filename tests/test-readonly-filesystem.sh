#!/usr/bin/env bash
# Smoke test for a built Lucee image.
#
# Verifies the Lucee 6.2+ non-root user and read-only root filesystem
# features against a locally-built image tag, plus a baseline regression
# check that the image still runs with default settings.
#
# Requires: docker, curl. Assumes the test page from www/ is in the image.
#
# Usage: ./test-readonly-filesystem.sh <image-tag> <tomcat|nginx>
#
#   e.g. ./test-readonly-filesystem.sh lucee/lucee:6.2.6.19-test       tomcat
#        ./test-readonly-filesystem.sh lucee/lucee:6.2.6.19-nginx-test nginx
#        ./test-readonly-filesystem.sh lucee/lucee:7.0.3.43-test       tomcat
#        ./test-readonly-filesystem.sh lucee/lucee:7.0.3.43-nginx-test nginx
#
# Three scenarios are run against the image:
#   1. Baseline - `docker run` with no opt-in. Regression check that
#      defaults still work; expects HTTP 200 from the test page.
#   2. Non-root - adds `--user lucee`. Expects HTTP 200 and `id -u`
#      inside the container to be non-zero.
#   3. Read-only rootfs - adds `--read-only` plus
#      `-e LUCEE_RUNTIME_DIR=/opt/lucee/server-runtime`. Expects HTTP 200
#      and the entrypoint's seed log line in `docker logs`.
#
# Exits 0 if all checks pass, non-zero otherwise. Cleans up its own
# container on exit.

set -uo pipefail

IMAGE="${1:-}"
VARIANT="${2:-}"

if [[ -z "$IMAGE" || -z "$VARIANT" ]]; then
    echo "Usage: $0 <image-tag> <tomcat|nginx>"
    exit 2
fi

case "$VARIANT" in
    tomcat) HTTP_PORT=8888; HOST_PORT=18888 ;;
    nginx)  HTTP_PORT=80;   HOST_PORT=18080 ;;
    *) echo "variant must be 'tomcat' or 'nginx'"; exit 2 ;;
esac

CONTAINER_NAME="lucee-smoke-$$"
PASS=0
FAIL=0

cleanup() {
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

report_pass() { echo "    PASS: $1"; PASS=$((PASS + 1)); }
report_fail() { echo "    FAIL: $1"; FAIL=$((FAIL + 1)); }

wait_for_http() {
    # Poll HTTP for up to 90s. Returns 0 on first 200, 1 on timeout.
    local url="$1"
    local deadline=$((SECONDS + 90))
    while (( SECONDS < deadline )); do
        if [[ "$(curl -sS -o /dev/null -w '%{http_code}' "$url" 2>/dev/null)" == "200" ]]; then
            return 0
        fi
        sleep 2
    done
    return 1
}

dump_logs_on_fail() {
    echo "    --- last 30 log lines ---"
    docker logs --tail 30 "$CONTAINER_NAME" 2>&1 | sed 's/^/      /'
    echo "    --- end logs ---"
}

run_scenario() {
    local label="$1"; shift
    echo "  Scenario: $label"
    cleanup
    docker run -d --name "$CONTAINER_NAME" -p "$HOST_PORT:$HTTP_PORT" "$@" "$IMAGE" >/dev/null
}

echo "===== $IMAGE ($VARIANT) ====="

# --- Scenario 1: baseline (regression test for default behavior) ---
run_scenario "baseline (defaults, no opt-in)"
if wait_for_http "http://localhost:$HOST_PORT/"; then
    report_pass "baseline responds 200"
else
    report_fail "baseline did not respond within 90s"
    dump_logs_on_fail
fi

# --- Scenario 2: non-root user only ---
run_scenario "non-root user (--user lucee)" --user lucee
if wait_for_http "http://localhost:$HOST_PORT/"; then
    report_pass "non-root responds 200"

    uid_observed=$(docker exec "$CONTAINER_NAME" id -u 2>/dev/null || echo error)
    user_observed=$(docker exec "$CONTAINER_NAME" id -un 2>/dev/null || echo error)
    if [[ "$uid_observed" != "0" && "$uid_observed" != "error" ]]; then
        report_pass "container running as non-root (uid=$uid_observed user=$user_observed)"
    else
        report_fail "container is still running as root (uid=$uid_observed)"
    fi
else
    report_fail "non-root did not respond within 90s"
    dump_logs_on_fail
fi

# --- Scenario 3: full read-only rootfs + non-root + LUCEE_RUNTIME_DIR ---
run_scenario "--read-only + --user lucee + LUCEE_RUNTIME_DIR" \
    --user lucee \
    --read-only \
    -e LUCEE_RUNTIME_DIR=/opt/lucee/server-runtime
if wait_for_http "http://localhost:$HOST_PORT/"; then
    report_pass "read-only rootfs responds 200"
else
    report_fail "read-only rootfs did not respond within 90s"
    dump_logs_on_fail
fi

# Check for the seed log line (regardless of HTTP outcome, because logs are still useful).
# Retry briefly to absorb a small race we've observed where Docker's log driver
# hasn't surfaced the entrypoint's pre-exec stderr write by the time the HTTP
# check returns. If the line is genuinely absent it will still report FAIL after
# all retries.
seed_line=""
for _ in 1 2 3 4 5; do
    seed_line=$(docker logs "$CONTAINER_NAME" 2>&1 | grep "Seeded LUCEE_RUNTIME_DIR" | head -1)
    [[ -n "$seed_line" ]] && break
    sleep 1
done
if [[ -n "$seed_line" ]]; then
    report_pass "seed log line present"
    echo "      > $seed_line"
else
    report_fail "seed log line missing"
fi

cleanup

echo "===== $IMAGE: $PASS passed, $FAIL failed ====="
[[ "$FAIL" -eq 0 ]]
