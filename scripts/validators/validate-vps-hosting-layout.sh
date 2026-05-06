#!/usr/bin/env bash
set -euo pipefail

TOPOLOGY_MODE=""
RUNTIME_HOST=""
FIXTURE_ROOT=""
SKIP_HOST_TOOLS=0
ENFORCE_PUBLIC_PORTS=0
PROJECTS_ROOT="/projects"
SRV_ROOT="/srv"
BACKUP_ROOT="/var/backups/projects"

usage() {
  cat <<'USAGE'
Usage: validate-vps-hosting-layout.sh --topology-mode single-host|split-host [options]

Options:
  --runtime-host host       Required for split-host.
  --fixture-root path       Map /projects, /srv and /var/backups/projects under a test fixture.
  --skip-host-tools         Do not require docker/nginx/systemd/firewall tools.
  --enforce-public-ports    Fail if public listeners other than 22/80/443 are detected.
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

while [[ $# -gt 0 ]]; do
  case "$1" in
    --topology-mode) TOPOLOGY_MODE="$2"; shift 2 ;;
    --runtime-host) RUNTIME_HOST="$2"; shift 2 ;;
    --fixture-root) FIXTURE_ROOT="$2"; shift 2 ;;
    --skip-host-tools) SKIP_HOST_TOOLS=1; shift ;;
    --enforce-public-ports) ENFORCE_PUBLIC_PORTS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$TOPOLOGY_MODE" ]] || { usage >&2; exit 2; }
case "$TOPOLOGY_MODE" in
  single-host|split-host) ok "topology mode is $TOPOLOGY_MODE" ;;
  *) fail "topology mode must be single-host or split-host" ;;
esac

projects_mapped="$(map_path "$PROJECTS_ROOT")"
srv_mapped="$(map_path "$SRV_ROOT")"
backup_mapped="$(map_path "$BACKUP_ROOT")"

[[ -d "$projects_mapped" ]] && ok "/projects exists" || fail "/projects missing"
if [[ "$TOPOLOGY_MODE" == "single-host" ]]; then
  [[ -d "$srv_mapped" ]] && ok "/srv exists for single-host" || fail "/srv missing for single-host"
else
  [[ -n "$RUNTIME_HOST" ]] && ok "split-host runtime host configured" || fail "split-host requires explicit runtime host"
fi
[[ -d "$backup_mapped" ]] && ok "/var/backups/projects exists" || warn "/var/backups/projects missing; creation must be part of runtime prep"

if [[ -d "$srv_mapped" ]]; then
  if find "$srv_mapped" -path '*/.git' -type d 2>/dev/null | grep -q .; then
    fail "found git workspace under /srv; runtime area must not be dev workspace"
  else
    ok "no git workspaces detected under /srv"
  fi
fi

if [[ "$SKIP_HOST_TOOLS" -ne 1 ]]; then
  if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    ok "docker compose is available"
  elif command -v docker-compose >/dev/null 2>&1; then
    warn "legacy docker-compose is available; docker compose plugin is preferred"
  else
    fail "docker compose is not available"
  fi
  command -v nginx >/dev/null 2>&1 && ok "nginx is available" || fail "nginx is not available"
  command -v systemctl >/dev/null 2>&1 && ok "systemd/systemctl is available" || fail "systemctl is not available"

  if command -v ss >/dev/null 2>&1; then
    unexpected_ports="$(ss -H -ltn 2>/dev/null | awk '{print $4}' | sed -nE 's/.*:([0-9]+)$/\1/p' | sort -n | uniq | grep -Ev '^(22|80|443)$' || true)"
    if [[ -n "$unexpected_ports" ]]; then
      if [[ "$ENFORCE_PUBLIC_PORTS" -eq 1 ]]; then
        fail "unexpected public/listening ports detected: $unexpected_ports"
      else
        warn "extra listening ports detected; enforce on real runtime if needed: $unexpected_ports"
      fi
    else
      ok "no unexpected listening ports detected"
    fi
  else
    warn "ss not available; public port validation skipped"
  fi
fi

if [[ "$failures" -gt 0 ]]; then
  echo "vps_hosting_layout_validation=failed failures=$failures"
  exit 1
fi
echo "vps_hosting_layout_validation=passed"
