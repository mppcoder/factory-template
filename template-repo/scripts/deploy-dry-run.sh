#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash template-repo/scripts/deploy-dry-run.sh [--init-env]

Options:
  --init-env  If deploy/.env is missing, create it from deploy/.env.example.
  -h, --help  Show help.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../project-presets.yaml" && -d "$SCRIPT_DIR/../scenario-pack" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

INIT_ENV=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --init-env)
      INIT_ENV=1
      shift
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

BASE_COMPOSE="$REPO_ROOT/deploy/compose.yaml"
PROD_COMPOSE="$REPO_ROOT/deploy/compose.production.yaml"
ENV_FILE="$REPO_ROOT/deploy/.env"
ENV_EXAMPLE="$REPO_ROOT/deploy/.env.example"
REPORT_DIR="$REPO_ROOT/.factory-runtime/reports"
REPORT_FILE="$REPORT_DIR/deploy-dry-run-latest.txt"

if [[ ! -f "$BASE_COMPOSE" ]]; then
  echo "Missing file: $BASE_COMPOSE" >&2
  exit 1
fi
if [[ ! -f "$PROD_COMPOSE" ]]; then
  echo "Missing file: $PROD_COMPOSE" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" && "$INIT_ENV" -eq 1 ]]; then
  if [[ ! -f "$ENV_EXAMPLE" ]]; then
    echo "Cannot init env: missing $ENV_EXAMPLE" >&2
    exit 1
  fi
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created $ENV_FILE from example."
fi

ACTIVE_ENV="$ENV_FILE"
ENV_MODE="custom"
if [[ ! -f "$ACTIVE_ENV" ]]; then
  if [[ -f "$ENV_EXAMPLE" ]]; then
    ACTIVE_ENV="$ENV_EXAMPLE"
    ENV_MODE="example"
  else
    echo "No env file found (deploy/.env or deploy/.env.example)." >&2
    exit 1
  fi
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN="docker compose"
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_BIN="docker-compose"
  COMPOSE=(docker-compose)
else
  echo "Docker Compose is not available. Install 'docker compose' or 'docker-compose'." >&2
  exit 1
fi

mkdir -p "$REPORT_DIR"
TMP_CONFIG="$(mktemp)"
TMP_ERR="$(mktemp)"
trap 'rm -f "$TMP_CONFIG" "$TMP_ERR"' EXIT

echo "Deploy dry-run"
echo "------------------------------------------------------------------------"
echo "Repo root: $REPO_ROOT"
echo "Compose base: deploy/compose.yaml"
echo "Compose prod: deploy/compose.production.yaml"
echo "Env source: ${ACTIVE_ENV#$REPO_ROOT/} ($ENV_MODE)"
echo "Compose binary: $COMPOSE_BIN"
echo

set +e
"${COMPOSE[@]}" -f "$BASE_COMPOSE" -f "$PROD_COMPOSE" --env-file "$ACTIVE_ENV" config >"$TMP_CONFIG" 2>"$TMP_ERR"
CONFIG_RC=$?
set -e

if [[ "$CONFIG_RC" -ne 0 ]]; then
  echo "Dry-run FAILED: compose config is not valid." >&2
  cat "$TMP_ERR" >&2
  {
    echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "status=fail"
    echo "env_mode=$ENV_MODE"
    echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  } > "$REPORT_FILE"
  exit 1
fi

SERVICES="$("${COMPOSE[@]}" -f "$BASE_COMPOSE" -f "$PROD_COMPOSE" --env-file "$ACTIVE_ENV" config --services | tr '\n' ' ' | sed 's/[[:space:]]\+$//')"
SERVICES="${SERVICES:-none}"
SERVICES_CSV="$(echo "$SERVICES" | tr ' ' ',' | sed 's/,$//')"

echo "Dry-run PASS: compose config is valid."
echo "Services: $SERVICES"
echo
echo "Next step:"
if [[ -x "$REPO_ROOT/template-repo/scripts/deploy-local-vps.sh" ]]; then
  echo "  bash template-repo/scripts/deploy-local-vps.sh --yes"
else
  echo "  bash scripts/deploy-local-vps.sh --yes"
fi

{
  echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "status=pass"
  echo "env_mode=$ENV_MODE"
  echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  echo "compose_bin=$COMPOSE_BIN"
  echo "services=$SERVICES_CSV"
} > "$REPORT_FILE"
