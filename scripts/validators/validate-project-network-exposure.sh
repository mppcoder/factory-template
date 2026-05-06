#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE=""
NGINX_CONF=""
ALLOW_DEV_PUBLIC_BIND=0

usage() {
  cat <<'USAGE'
Usage: validate-project-network-exposure.sh --compose-file path [--nginx-conf path] [--allow-dev-public-bind]

Checks that project runtime binds app ports to loopback and uses nginx as public edge.
USAGE
}

failures=0
fail() { echo "FAIL: $*"; failures=$((failures + 1)); }
ok() { echo "OK: $*"; }
warn() { echo "WARN: $*"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --compose-file) COMPOSE_FILE="$2"; shift 2 ;;
    --nginx-conf) NGINX_CONF="$2"; shift 2 ;;
    --allow-dev-public-bind) ALLOW_DEV_PUBLIC_BIND=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$COMPOSE_FILE" ]] || { usage >&2; exit 2; }
[[ -f "$COMPOSE_FILE" ]] || fail "compose file not found: $COMPOSE_FILE"

if [[ -f "$COMPOSE_FILE" ]]; then
  if grep -Eq '"?0\.0\.0\.0:' "$COMPOSE_FILE"; then
    if [[ "$ALLOW_DEV_PUBLIC_BIND" -eq 1 ]]; then
      warn "compose has 0.0.0.0 bind allowed as dev-only"
    else
      fail "compose exposes app directly on 0.0.0.0"
    fi
  fi
  if grep -Eq '127\.0\.0\.1:[A-Z_0-9{}:$:-]+' "$COMPOSE_FILE"; then
    ok "compose uses loopback bind"
  else
    fail "compose must bind app port to 127.0.0.1"
  fi
  if grep -Eq 'ports:[[:space:]]*$' "$COMPOSE_FILE"; then
    ok "compose declares port mapping for validator inspection"
  else
    warn "compose has no explicit ports block; ensure nginx can reach the app by another documented path"
  fi
fi

if [[ -n "$NGINX_CONF" ]]; then
  [[ -f "$NGINX_CONF" ]] || fail "nginx conf not found: $NGINX_CONF"
  if [[ -f "$NGINX_CONF" ]]; then
    grep -q "proxy_pass http://127.0.0.1:" "$NGINX_CONF" \
      && ok "nginx proxies to loopback" \
      || fail "nginx must proxy to 127.0.0.1:<port>"
    grep -Eq 'listen[[:space:]]+80|listen[[:space:]]+443' "$NGINX_CONF" \
      && ok "nginx is configured as public edge" \
      || warn "nginx conf does not expose 80/443 in this template"
  fi
fi

if [[ "$failures" -gt 0 ]]; then
  echo "network_exposure_validation=failed failures=$failures"
  exit 1
fi
echo "network_exposure_validation=passed"
