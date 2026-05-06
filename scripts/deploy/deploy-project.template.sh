#!/usr/bin/env bash
set -euo pipefail

PROJECT_SLUG="${PROJECT_SLUG:-PROJECT_SLUG}"
PROJECT_REPO_PATH="${PROJECT_REPO_PATH:-PROJECT_REPO_PATH}"
PROJECT_RUNTIME_PATH="${PROJECT_RUNTIME_PATH:-PROJECT_RUNTIME_PATH}"
PROJECT_ENV_FILE="${PROJECT_ENV_FILE:-PROJECT_ENV_FILE}"
PROJECT_DOMAIN="${PROJECT_DOMAIN:-PROJECT_DOMAIN}"
PROJECT_HEALTH_PATH="${PROJECT_HEALTH_PATH:-PROJECT_HEALTH_PATH}"
COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-COMPOSE_PROJECT_NAME}"
TOPOLOGY_MODE="${TOPOLOGY_MODE:-TOPOLOGY_MODE}"
RUNTIME_HOST="${RUNTIME_HOST:-RUNTIME_HOST}"
REPORT_PATH="${REPORT_PATH:-.factory-runtime/reports/PROJECT_SLUG-deploy-report-latest.txt}"
DRY_RUN=0
AUTO_YES=0
SKIP_GIT_CHECK=0

usage() {
  cat <<'USAGE'
Usage: deploy-project.template.sh [--dry-run] [--yes] [--skip-git-check]

Dry-run-first project runtime deploy template.
Render PROJECT_* placeholders before production use.
Supports:
  TOPOLOGY_MODE=single-host with local /srv runtime.
  TOPOLOGY_MODE=split-host with RUNTIME_HOST SSH target.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --yes) AUTO_YES=1; shift ;;
    --skip-git-check) SKIP_GIT_CHECK=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

fail() {
  echo "deploy_project_error=$1" >&2
  exit 1
}

redacted_path() {
  case "$1" in
    "$PROJECT_ENV_FILE") printf '%s' "$PROJECT_ENV_FILE" ;;
    *) printf '%s' "$1" ;;
  esac
}

run_local() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf 'dry_run_local:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

run_runtime() {
  if [[ "$TOPOLOGY_MODE" == "split-host" ]]; then
    [[ -n "$RUNTIME_HOST" && "$RUNTIME_HOST" != "RUNTIME_HOST" ]] || fail "split_host_runtime_host_missing"
    if [[ "$DRY_RUN" -eq 1 ]]; then
      printf 'dry_run_remote %q:' "$RUNTIME_HOST"
      printf ' %q' "$@"
      printf '\n'
    else
      ssh "$RUNTIME_HOST" "$@"
    fi
  else
    run_local "$@"
  fi
}

case "$TOPOLOGY_MODE" in
  single-host|split-host) ;;
  *) fail "TOPOLOGY_MODE must be single-host or split-host" ;;
esac

[[ "$PROJECT_RUNTIME_PATH" == /srv/*-prod ]] || fail "runtime_path_must_be_under_srv_project_prod"
[[ "$PROJECT_REPO_PATH" == /projects/* ]] || fail "repo_path_must_be_under_projects"
[[ "$PROJECT_ENV_FILE" == /etc/*.env ]] || fail "env_file_must_be_under_etc"
[[ "$PROJECT_ENV_FILE" != "$PROJECT_REPO_PATH"* ]] || fail "env_file_must_not_be_inside_repo"

if [[ "$SKIP_GIT_CHECK" -ne 1 ]]; then
  git -C "$PROJECT_REPO_PATH" status --short --branch >/tmp/"$PROJECT_SLUG-git-status.txt"
  if grep -Ev '^(##|$)' /tmp/"$PROJECT_SLUG-git-status.txt" >/dev/null; then
    cat /tmp/"$PROJECT_SLUG-git-status.txt" >&2
    fail "repo_worktree_dirty"
  fi
fi

if [[ "$TOPOLOGY_MODE" == "single-host" ]]; then
  [[ -f "$PROJECT_ENV_FILE" ]] || fail "env_file_missing"
  mode="$(stat -c '%a' "$PROJECT_ENV_FILE" 2>/dev/null || stat -f '%Lp' "$PROJECT_ENV_FILE")"
  [[ "$mode" == "600" ]] || fail "env_file_must_be_chmod_600"
fi

if [[ "$AUTO_YES" -ne 1 && "$DRY_RUN" -ne 1 ]]; then
  read -r -p "Deploy $PROJECT_SLUG to $TOPOLOGY_MODE runtime? [y/N]: " answer
  [[ "${answer:-n}" =~ ^[Yy]$ ]] || fail "operator_cancelled"
fi

mkdir -p "$(dirname "$REPORT_PATH")"
{
  echo "project=$PROJECT_SLUG"
  echo "topology_mode=$TOPOLOGY_MODE"
  echo "runtime_host=$RUNTIME_HOST"
  echo "runtime_path=$PROJECT_RUNTIME_PATH"
  echo "env_file=$(redacted_path "$PROJECT_ENV_FILE")"
  echo "domain=$PROJECT_DOMAIN"
  echo "secret_values_printed=false"
  echo "dry_run=$DRY_RUN"
} > "$REPORT_PATH"

run_runtime mkdir -p "$PROJECT_RUNTIME_PATH"
if [[ "$TOPOLOGY_MODE" == "single-host" ]]; then
  run_local bash scripts/deploy/backup-project-runtime.template.sh --dry-run
fi

if [[ -f "$PROJECT_RUNTIME_PATH/compose.yaml" || "$DRY_RUN" -eq 1 ]]; then
  run_runtime docker compose --env-file "$PROJECT_ENV_FILE" -p "$COMPOSE_PROJECT_NAME" -f "$PROJECT_RUNTIME_PATH/compose.yaml" config
fi
run_runtime docker compose --env-file "$PROJECT_ENV_FILE" -p "$COMPOSE_PROJECT_NAME" -f "$PROJECT_RUNTIME_PATH/compose.yaml" up -d --remove-orphans
run_runtime systemctl daemon-reload
run_runtime systemctl enable --now "$PROJECT_SLUG.service"
run_runtime nginx -t
run_runtime systemctl reload nginx

if [[ "$PROJECT_HEALTH_PATH" != "PROJECT_HEALTH_PATH" ]]; then
  run_runtime curl -fsS "http://127.0.0.1:PROJECT_INTERNAL_PORT$PROJECT_HEALTH_PATH"
fi

echo "deploy_report=$REPORT_PATH"
echo "deploy_complete=true"
