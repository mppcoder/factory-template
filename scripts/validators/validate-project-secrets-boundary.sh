#!/usr/bin/env bash
set -euo pipefail

ROOT="."
PROJECT_SLUG=""
ENV_PATH=""

usage() {
  cat <<'USAGE'
Usage: validate-project-secrets-boundary.sh [--root path] [--project-slug slug] [--env-path /etc/project.env]

Checks repo secret boundary for project runtime templates and tracked files.
USAGE
}

failures=0
fail() { echo "FAIL: $*"; failures=$((failures + 1)); }
ok() { echo "OK: $*"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --project-slug) PROJECT_SLUG="$2"; shift 2 ;;
    --env-path) ENV_PATH="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$ROOT" && pwd)"

if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  while IFS= read -r tracked; do
    base="$(basename "$tracked")"
    if [[ "$base" == ".env" || "$tracked" == *.env ]]; then
      case "$tracked" in
        *.env.example|deploy/templates/env.project.example) ;;
        *) fail "tracked real env-like file: $tracked" ;;
      esac
    fi
  done < <(git -C "$ROOT" ls-files)
else
  fail "root is not a git worktree: $ROOT"
fi

if [[ -n "$ENV_PATH" ]]; then
  [[ "$ENV_PATH" == /etc/*.env ]] || fail "real env path must be /etc/<project>.env"
  case "$ENV_PATH" in
    "$ROOT"/*) fail "real env path is inside repo" ;;
    *) ok "real env path is outside repo" ;;
  esac
fi

if [[ -n "$PROJECT_SLUG" && -d "$ROOT/var/backups/projects/$PROJECT_SLUG" ]]; then
  fail "backup directory is inside repo: var/backups/projects/$PROJECT_SLUG"
fi

scan_paths=(
  "deploy/templates"
  "docs/architecture/vps-project-hosting-topologies.md"
  "docs/runbooks/migrate-projects-vps-topologies.md"
  "docs/runbooks/pilot-project-vps-migration-checklist.md"
  "docs/runbooks/restore-proof-vps-project-runtime.md"
  "scripts/deploy"
  "scripts/validators"
  "docs/decisions"
  "factory/producer/registry/known-risks"
)

secret_line_regex='(PASSWORD|TOKEN|SECRET|PRIVATE_KEY|DATABASE_URL|API_KEY|ACCESS_KEY)[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*[^[:space:]#]+'
allowed_placeholder_regex='(change-me|example|placeholder|PROJECT_|REDACTED|<project>|<record|ops@example|registry.example.com)'

for rel in "${scan_paths[@]}"; do
  path="$ROOT/$rel"
  [[ -e "$path" ]] || continue
  while IFS= read -r file; do
    while IFS= read -r line; do
      if [[ "$line" =~ $secret_line_regex && ! "$line" =~ $allowed_placeholder_regex ]]; then
        fail "secret-like assignment without placeholder marker in ${file#$ROOT/}"
        break
      fi
    done < "$file"
  done < <(find "$path" -type f)
done

if [[ "$failures" -gt 0 ]]; then
  echo "project_secrets_boundary_validation=failed failures=$failures"
  exit 1
fi
echo "project_secrets_boundary_validation=passed"
