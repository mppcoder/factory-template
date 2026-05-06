#!/usr/bin/env bash
set -euo pipefail

PROJECT_SLUG="${PROJECT_SLUG:-PROJECT_SLUG}"
PROJECT_RUNTIME_PATH="${PROJECT_RUNTIME_PATH:-PROJECT_RUNTIME_PATH}"
PROJECT_ENV_FILE="${PROJECT_ENV_FILE:-PROJECT_ENV_FILE}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/projects/PROJECT_SLUG}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/PROJECT_SLUG.service}"
NGINX_CONF="${NGINX_CONF:-/etc/nginx/sites-available/PROJECT_SLUG.conf}"
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: backup-project-runtime.template.sh [--dry-run]

Backs up one rendered project runtime without printing secrets.
Render PROJECT_* placeholders before production use.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
target="$BACKUP_ROOT/$timestamp"

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf 'dry_run: %q\n' "$*"
  else
    "$@"
  fi
}

echo "backup_project=$PROJECT_SLUG"
echo "backup_target=$target"
echo "secret_values_printed=false"

run mkdir -p "$target"
if [[ -d "$PROJECT_RUNTIME_PATH" ]]; then
  run tar -C "$(dirname "$PROJECT_RUNTIME_PATH")" -czf "$target/runtime.tgz" "$(basename "$PROJECT_RUNTIME_PATH")"
fi
if [[ -f "$PROJECT_ENV_FILE" ]]; then
  run install -m 0600 "$PROJECT_ENV_FILE" "$target/env.backup"
fi
if [[ -f "$SERVICE_FILE" ]]; then
  run cp "$SERVICE_FILE" "$target/systemd.service"
fi
if [[ -f "$NGINX_CONF" ]]; then
  run cp "$NGINX_CONF" "$target/nginx.conf"
fi
if [[ -f "$PROJECT_RUNTIME_PATH/compose.yaml" ]]; then
  run cp "$PROJECT_RUNTIME_PATH/compose.yaml" "$target/compose.yaml"
fi

echo "backup_complete=true"
