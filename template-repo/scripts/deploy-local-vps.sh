#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash template-repo/scripts/deploy-local-vps.sh [--yes] [--skip-pull] [--init-env] [--preset preset-list]

Options:
  --yes        Run non-interactively (skip confirmation).
  --skip-pull  Skip `docker compose pull`.
  --init-env   If deploy/.env is missing, create it from deploy/.env.example.
  --preset     Override OPERATOR_PRESET from env for this deploy.
               Values: starter, app-db, reverse-proxy-tls, backup, healthcheck, production.
               Multiple overlays may be comma-separated, for example app-db,backup.
  -h, --help   Show help.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../project-presets.yaml" && -d "$SCRIPT_DIR/../scenario-pack" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

AUTO_YES=0
SKIP_PULL=0
INIT_ENV=0
PRESET_OVERRIDE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes)
      AUTO_YES=1
      shift
      ;;
    --skip-pull)
      SKIP_PULL=1
      shift
      ;;
    --init-env)
      INIT_ENV=1
      shift
      ;;
    --preset)
      PRESET_OVERRIDE="$2"
      shift 2
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
REPORT_FILE="$REPORT_DIR/deploy-last-run.txt"
DRY_RUN_SCRIPT="$SCRIPT_DIR/deploy-dry-run.sh"

if [[ ! -x "$DRY_RUN_SCRIPT" ]]; then
  echo "Missing helper script: $DRY_RUN_SCRIPT" >&2
  exit 1
fi

echo "Step 1/3: dry-run safety check"
DRY_ARGS=(--strict-env)
if [[ "$INIT_ENV" -eq 1 ]]; then
  DRY_ARGS+=("--init-env")
fi
if [[ -n "$PRESET_OVERRIDE" ]]; then
  DRY_ARGS+=("--preset" "$PRESET_OVERRIDE")
fi
bash "$DRY_RUN_SCRIPT" "${DRY_ARGS[@]}"

ACTIVE_ENV="$ENV_FILE"
if [[ ! -f "$ACTIVE_ENV" ]]; then
  if [[ -f "$ENV_EXAMPLE" ]]; then
    ACTIVE_ENV="$ENV_EXAMPLE"
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

if [[ "$AUTO_YES" -ne 1 ]]; then
  echo
  read -r -p "Dry-run passed. Continue with deploy? [y/N]: " CONFIRM
  CONFIRM="${CONFIRM:-n}"
  if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Deploy cancelled by operator."
    exit 0
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

PRESET="${PRESET_OVERRIDE:-$(env_value OPERATOR_PRESET "$ACTIVE_ENV")}"
PRESET="${PRESET:-starter}"
COMPOSE_ARGS=(-f "$BASE_COMPOSE" -f "$PROD_COMPOSE")

compose_files_for_preset() {
  local preset="$1"
  local normalized="${preset//+/,}"
  local token
  local seen=","
  IFS=',' read -r -a PRESET_TOKENS <<<"$normalized"

  add_preset_file() {
    local file="$1"
    if [[ "$seen" != *",$file,"* ]]; then
      COMPOSE_ARGS+=(-f "$file")
      seen+="$file,"
    fi
  }

  add_token() {
    case "$1" in
      starter|"")
        add_preset_file "$REPO_ROOT/deploy/presets/starter.yaml"
        ;;
      app-db)
        add_preset_file "$REPO_ROOT/deploy/presets/app-db.yaml"
        ;;
      reverse-proxy-tls)
        add_preset_file "$REPO_ROOT/deploy/presets/reverse-proxy-tls.yaml"
        ;;
      reverse-proxy)
        add_preset_file "$REPO_ROOT/deploy/presets/reverse-proxy-tls.yaml"
        ;;
      backup)
        add_preset_file "$REPO_ROOT/deploy/presets/backup.yaml"
        ;;
      healthcheck)
        add_preset_file "$REPO_ROOT/deploy/presets/healthcheck.yaml"
        ;;
      production)
        add_token app-db
        add_token reverse-proxy-tls
        add_token backup
        add_token healthcheck
        ;;
      *)
        echo "Unknown operator preset: $1" >&2
        echo "Use starter, app-db, reverse-proxy-tls, backup, healthcheck, production, or a comma-separated list." >&2
        exit 2
        ;;
    esac
  }

  for token in "${PRESET_TOKENS[@]}"; do
    token="${token//[[:space:]]/}"
    add_token "$token"
  done
}

compose_files_for_preset "$PRESET"
COMPOSE_ARGS+=(--env-file "$ACTIVE_ENV")

echo
echo "Step 2/3: deploy"
echo "------------------------------------------------------------------------"
echo "Repo root: $REPO_ROOT"
echo "Compose binary: $COMPOSE_BIN"
echo "Operator preset: $PRESET"
echo "Env source: ${ACTIVE_ENV#$REPO_ROOT/}"
echo

if [[ "$SKIP_PULL" -ne 1 ]]; then
  "${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" pull
fi
"${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" up -d --remove-orphans

echo
echo "Step 3/3: running services"
SERVICES="$("${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" config --services | tr '\n' ' ' | sed 's/[[:space:]]\+$//')"
SERVICES="${SERVICES:-none}"
SERVICES_CSV="$(echo "$SERVICES" | tr ' ' ',' | sed 's/,$//')"
"${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" ps

mkdir -p "$REPORT_DIR"
{
  echo "timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "status=deployed"
  echo "preset=$PRESET"
  echo "env_file=${ACTIVE_ENV#$REPO_ROOT/}"
  echo "compose_bin=$COMPOSE_BIN"
  echo "services=$SERVICES_CSV"
} > "$REPORT_FILE"

echo
echo "Deploy completed."
if [[ -x "$REPO_ROOT/template-repo/scripts/operator-dashboard.py" ]]; then
  echo "Next: python3 template-repo/scripts/operator-dashboard.py --verify-summary"
else
  echo "Next: python3 scripts/operator-dashboard.py --verify-summary"
fi
