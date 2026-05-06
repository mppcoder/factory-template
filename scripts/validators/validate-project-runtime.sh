#!/usr/bin/env bash
set -euo pipefail

PROJECT_SLUG=""
TOPOLOGY_MODE=""
RUNTIME_PATH=""
ENV_PATH=""
SERVICE_NAME=""
SERVICE_FILE=""
NGINX_CONF=""
NGINX_ENABLED=""
COMPOSE_FILE=""
BACKUP_PATH=""
DEPLOY_SCRIPT=""
HEALTH_URL=""
RUNTIME_HOST=""
REPO_PATH=""
FIXTURE_ROOT=""
SKIP_HOST_TOOLS=0

usage() {
  cat <<'USAGE'
Usage: validate-project-runtime.sh --project-slug slug --topology-mode mode --runtime-path path --env-path path --service-name name --nginx-conf path --compose-file path --backup-path path [options]

Options:
  --service-file path
  --nginx-enabled path
  --deploy-script path
  --health-url url
  --runtime-host host
  --repo-path path
  --fixture-root path
  --skip-host-tools
USAGE
}

failures=0
fail() { echo "FAIL: $*"; failures=$((failures + 1)); }
ok() { echo "OK: $*"; }
warn() { echo "WARN: $*"; }

map_path() {
  local value="$1"
  if [[ -n "$FIXTURE_ROOT" && "$value" == /* ]]; then
    printf '%s%s' "$FIXTURE_ROOT" "$value"
  else
    printf '%s' "$value"
  fi
}

mode_of() {
  stat -c '%a' "$1" 2>/dev/null || stat -f '%Lp' "$1" 2>/dev/null || true
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-slug) PROJECT_SLUG="$2"; shift 2 ;;
    --topology-mode) TOPOLOGY_MODE="$2"; shift 2 ;;
    --runtime-path) RUNTIME_PATH="$2"; shift 2 ;;
    --env-path) ENV_PATH="$2"; shift 2 ;;
    --service-name) SERVICE_NAME="$2"; shift 2 ;;
    --service-file) SERVICE_FILE="$2"; shift 2 ;;
    --nginx-conf) NGINX_CONF="$2"; shift 2 ;;
    --nginx-enabled) NGINX_ENABLED="$2"; shift 2 ;;
    --compose-file) COMPOSE_FILE="$2"; shift 2 ;;
    --backup-path) BACKUP_PATH="$2"; shift 2 ;;
    --deploy-script) DEPLOY_SCRIPT="$2"; shift 2 ;;
    --health-url) HEALTH_URL="$2"; shift 2 ;;
    --runtime-host) RUNTIME_HOST="$2"; shift 2 ;;
    --repo-path) REPO_PATH="$2"; shift 2 ;;
    --fixture-root) FIXTURE_ROOT="$2"; shift 2 ;;
    --skip-host-tools) SKIP_HOST_TOOLS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

for required in PROJECT_SLUG TOPOLOGY_MODE RUNTIME_PATH ENV_PATH SERVICE_NAME NGINX_CONF COMPOSE_FILE BACKUP_PATH; do
  [[ -n "${!required}" ]] || { echo "missing --${required,,}" >&2; usage >&2; exit 2; }
done
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/$SERVICE_NAME.service}"

case "$TOPOLOGY_MODE" in
  single-host|split-host) ok "topology mode is $TOPOLOGY_MODE" ;;
  *) fail "topology mode must be single-host or split-host" ;;
esac
if [[ "$TOPOLOGY_MODE" == "split-host" && -z "$RUNTIME_HOST" ]]; then
  fail "split-host requires --runtime-host"
fi

runtime_mapped="$(map_path "$RUNTIME_PATH")"
env_mapped="$(map_path "$ENV_PATH")"
service_mapped="$(map_path "$SERVICE_FILE")"
nginx_mapped="$(map_path "$NGINX_CONF")"
compose_mapped="$(map_path "$COMPOSE_FILE")"
backup_mapped="$(map_path "$BACKUP_PATH")"

[[ "$RUNTIME_PATH" == "/srv/$PROJECT_SLUG-prod" ]] || fail "runtime path must be /srv/$PROJECT_SLUG-prod"
[[ -d "$runtime_mapped" ]] && ok "runtime path exists" || fail "runtime path missing: $RUNTIME_PATH"
[[ -f "$env_mapped" ]] && ok "env file exists outside repo path" || fail "env file missing: $ENV_PATH"
if [[ -f "$env_mapped" ]]; then
  mode="$(mode_of "$env_mapped")"
  [[ "$mode" == "600" ]] && ok "env chmod is 600" || fail "env chmod must be 600, got ${mode:-unknown}"
fi
if [[ -n "$REPO_PATH" && "$ENV_PATH" == "$REPO_PATH"* ]]; then
  fail "env file is inside repo path"
fi
[[ "$ENV_PATH" == /etc/*.env ]] || fail "env path must be /etc/<project>.env"
[[ -f "$service_mapped" ]] && ok "systemd service file exists" || fail "service file missing: $SERVICE_FILE"
[[ -f "$nginx_mapped" ]] && ok "nginx conf exists" || fail "nginx conf missing: $NGINX_CONF"
if [[ -n "$NGINX_ENABLED" ]]; then
  [[ -e "$(map_path "$NGINX_ENABLED")" ]] && ok "nginx enabled path exists" || fail "nginx enabled path missing: $NGINX_ENABLED"
fi
[[ -f "$compose_mapped" ]] && ok "compose file exists" || fail "compose file missing: $COMPOSE_FILE"
[[ -d "$backup_mapped" ]] && ok "backup path exists" || fail "backup path missing: $BACKUP_PATH"
if [[ -n "$DEPLOY_SCRIPT" ]]; then
  [[ -x "$DEPLOY_SCRIPT" ]] && ok "deploy script executable" || fail "deploy script not executable: $DEPLOY_SCRIPT"
fi

if [[ "$SKIP_HOST_TOOLS" -ne 1 ]]; then
  if command -v systemctl >/dev/null 2>&1; then
    systemctl cat "$SERVICE_NAME" >/dev/null 2>&1 && ok "systemctl cat works" || warn "systemctl cat did not find installed service"
  else
    warn "systemctl not available"
  fi
  if command -v nginx >/dev/null 2>&1; then
    nginx -t && ok "nginx -t passed" || fail "nginx -t failed"
  else
    warn "nginx not available"
  fi
  if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    docker compose --env-file "$env_mapped" -f "$compose_mapped" config >/dev/null \
      && ok "docker compose config passed" \
      || fail "docker compose config failed"
  else
    warn "docker compose not available"
  fi
  if [[ -n "$HEALTH_URL" ]]; then
    curl -fsS "$HEALTH_URL" >/dev/null && ok "health endpoint passed" || fail "health endpoint failed"
  fi
fi

if [[ "$failures" -gt 0 ]]; then
  echo "project_runtime_validation=failed failures=$failures"
  exit 1
fi
echo "project_runtime_validation=passed"
