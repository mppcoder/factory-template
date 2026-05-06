#!/usr/bin/env bash
set -euo pipefail

PROJECT_SLUG="${PROJECT_SLUG:-PROJECT_SLUG}"
PROJECT_RUNTIME_PATH="${PROJECT_RUNTIME_PATH:-PROJECT_RUNTIME_PATH}"
PROJECT_ENV_FILE="${PROJECT_ENV_FILE:-PROJECT_ENV_FILE}"
BACKUP_DIR="${BACKUP_DIR:-}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/PROJECT_SLUG.service}"
NGINX_CONF="${NGINX_CONF:-/etc/nginx/sites-available/PROJECT_SLUG.conf}"
DRY_RUN=0
AUTO_YES=0

usage() {
  cat <<'USAGE'
Usage: restore-project-runtime.template.sh --backup-dir path [--dry-run] [--yes]

Restores runtime dir, env, systemd, nginx and compose from a project backup.
Render PROJECT_* placeholders before production use.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backup-dir) BACKUP_DIR="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --yes) AUTO_YES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$BACKUP_DIR" ]] || { echo "missing --backup-dir" >&2; exit 2; }
[[ -d "$BACKUP_DIR" || "$DRY_RUN" -eq 1 ]] || { echo "backup dir not found" >&2; exit 1; }

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf 'dry_run:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

if [[ "$AUTO_YES" -ne 1 && "$DRY_RUN" -ne 1 ]]; then
  read -r -p "Restore $PROJECT_SLUG runtime from $BACKUP_DIR? [y/N]: " answer
  [[ "${answer:-n}" =~ ^[Yy]$ ]] || { echo "restore_cancelled=true"; exit 1; }
fi

echo "restore_project=$PROJECT_SLUG"
echo "backup_dir=$BACKUP_DIR"
echo "secret_values_printed=false"

run systemctl stop "$PROJECT_SLUG.service"
if [[ -f "$BACKUP_DIR/runtime.tgz" ]]; then
  run mkdir -p "$(dirname "$PROJECT_RUNTIME_PATH")"
  run tar -C "$(dirname "$PROJECT_RUNTIME_PATH")" -xzf "$BACKUP_DIR/runtime.tgz"
fi
if [[ -f "$BACKUP_DIR/env.backup" ]]; then
  run install -m 0600 "$BACKUP_DIR/env.backup" "$PROJECT_ENV_FILE"
fi
if [[ -f "$BACKUP_DIR/systemd.service" ]]; then
  run cp "$BACKUP_DIR/systemd.service" "$SERVICE_FILE"
fi
if [[ -f "$BACKUP_DIR/nginx.conf" ]]; then
  run cp "$BACKUP_DIR/nginx.conf" "$NGINX_CONF"
fi
if [[ -f "$BACKUP_DIR/compose.yaml" ]]; then
  run cp "$BACKUP_DIR/compose.yaml" "$PROJECT_RUNTIME_PATH/compose.yaml"
fi
run systemctl daemon-reload
run nginx -t
run systemctl reload nginx
run systemctl start "$PROJECT_SLUG.service"

echo "restore_complete=true"
