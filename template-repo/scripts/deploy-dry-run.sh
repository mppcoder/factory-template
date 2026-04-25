#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash template-repo/scripts/deploy-dry-run.sh [--init-env] [--env-file path] [--preset starter|app-db|reverse-proxy|production] [--strict-env]

Options:
  --init-env    If deploy/.env is missing, create it from deploy/.env.example.
  --env-file    Validate and render compose with a specific env file.
  --preset      Override OPERATOR_PRESET from env for this run.
  --strict-env  Treat example placeholders as failures.
  -h, --help    Show help.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../project-presets.yaml" && -d "$SCRIPT_DIR/../scenario-pack" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

INIT_ENV=0
ENV_FILE_OVERRIDE=""
PRESET_OVERRIDE=""
STRICT_ENV=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --init-env)
      INIT_ENV=1
      shift
      ;;
    --env-file)
      ENV_FILE_OVERRIDE="$2"
      shift 2
      ;;
    --preset)
      PRESET_OVERRIDE="$2"
      shift 2
      ;;
    --strict-env)
      STRICT_ENV=1
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
VALIDATE_ENV_SCRIPT="$REPO_ROOT/template-repo/scripts/validate-operator-env.py"
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

if [[ -n "$ENV_FILE_OVERRIDE" ]]; then
  ACTIVE_ENV="$ENV_FILE_OVERRIDE"
  ENV_MODE="custom"
  if [[ ! -f "$ACTIVE_ENV" ]]; then
    echo "Env file not found: $ACTIVE_ENV" >&2
    exit 1
  fi
else
  ACTIVE_ENV="$ENV_FILE"
  ENV_MODE="custom"
fi
if [[ ! -f "$ACTIVE_ENV" && -z "$ENV_FILE_OVERRIDE" ]]; then
  if [[ -f "$ENV_EXAMPLE" ]]; then
    ACTIVE_ENV="$ENV_EXAMPLE"
    ENV_MODE="example"
  else
    echo "No env file found (deploy/.env or deploy/.env.example)." >&2
    exit 1
  fi
fi

env_value() {
  local key="$1"
  local file="$2"
  awk -F= -v key="$key" '
    $1 == key {
      value = substr($0, index($0, "=") + 1)
      gsub(/^["'\'' ]+|["'\'' ]+$/, "", value)
      print value
      exit
    }
  ' "$file"
}

compose_files_for_preset() {
  local preset="$1"
  COMPOSE_ARGS=(-f "$BASE_COMPOSE" -f "$PROD_COMPOSE")
  case "$preset" in
    starter)
      ;;
    app-db)
      COMPOSE_ARGS+=(-f "$REPO_ROOT/deploy/presets/app-db.yaml")
      ;;
    reverse-proxy)
      COMPOSE_ARGS+=(-f "$REPO_ROOT/deploy/presets/reverse-proxy.yaml")
      ;;
    production)
      COMPOSE_ARGS+=(-f "$REPO_ROOT/deploy/presets/app-db.yaml" -f "$REPO_ROOT/deploy/presets/reverse-proxy.yaml")
      ;;
    *)
      echo "Unknown operator preset: $preset" >&2
      echo "Use one of: starter, app-db, reverse-proxy, production." >&2
      exit 2
      ;;
  esac
}

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

PRESET="${PRESET_OVERRIDE:-$(env_value OPERATOR_PRESET "$ACTIVE_ENV")}"
PRESET="${PRESET:-starter}"
compose_files_for_preset "$PRESET"

VALIDATE_ARGS=("$REPO_ROOT" "--env-file" "$ACTIVE_ENV" "--preset" "$PRESET")
if [[ "$ENV_MODE" == "example" && "$STRICT_ENV" -ne 1 ]]; then
  VALIDATE_ARGS+=("--allow-example-placeholders")
fi

echo "Deploy dry-run"
echo "------------------------------------------------------------------------"
echo "Repo root: $REPO_ROOT"
echo "Compose base: deploy/compose.yaml"
echo "Compose prod: deploy/compose.production.yaml"
echo "Operator preset: $PRESET"
echo "Env source: ${ACTIVE_ENV#$REPO_ROOT/} ($ENV_MODE)"
echo "Compose binary: $COMPOSE_BIN"
echo

if [[ ! -f "$VALIDATE_ENV_SCRIPT" ]]; then
  echo "Missing env validator: $VALIDATE_ENV_SCRIPT" >&2
  exit 1
fi

set +e
python3 "$VALIDATE_ENV_SCRIPT" "${VALIDATE_ARGS[@]}"
VALIDATE_RC=$?
set -e
if [[ "$VALIDATE_RC" -ne 0 ]]; then
  echo "Dry-run FAILED: operator env validation failed." >&2
  {
    echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "status=fail"
    echo "preset=$PRESET"
    echo "failure=env-validation"
    echo "env_mode=$ENV_MODE"
    echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  } > "$REPORT_FILE"
  exit 1
fi

set +e
"${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" --env-file "$ACTIVE_ENV" config >"$TMP_CONFIG" 2>"$TMP_ERR"
CONFIG_RC=$?
set -e

if [[ "$CONFIG_RC" -ne 0 ]]; then
  echo "Dry-run FAILED: compose config is not valid." >&2
  cat "$TMP_ERR" >&2
  {
    echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "status=fail"
    echo "preset=$PRESET"
    echo "failure=compose-config"
    echo "env_mode=$ENV_MODE"
    echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  } > "$REPORT_FILE"
  exit 1
fi

SERVICES="$("${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" --env-file "$ACTIVE_ENV" config --services | tr '\n' ' ' | sed 's/[[:space:]]\+$//')"
SERVICES="${SERVICES:-none}"
SERVICES_CSV="$(echo "$SERVICES" | tr ' ' ',' | sed 's/,$//')"

echo "Dry-run ПРОЙДЕН: compose config валиден."
echo "Сервисы: $SERVICES"
echo
echo "Следующий шаг:"
DEPLOY_PRESET_ARG=""
if [[ "$PRESET" != "starter" ]]; then
  DEPLOY_PRESET_ARG=" --preset $PRESET"
fi
if [[ -x "$REPO_ROOT/template-repo/scripts/deploy-local-vps.sh" ]]; then
  echo "  bash template-repo/scripts/deploy-local-vps.sh --yes$DEPLOY_PRESET_ARG"
else
  echo "  bash scripts/deploy-local-vps.sh --yes$DEPLOY_PRESET_ARG"
fi

{
  echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "status=pass"
  echo "preset=$PRESET"
  echo "env_mode=$ENV_MODE"
  echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  echo "compose_bin=$COMPOSE_BIN"
  echo "services=$SERVICES_CSV"
} > "$REPORT_FILE"
