#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_ROOT="$ROOT"
TASK_FILE=""
TASK_TEXT=""
TASK_CLASS=""
LAUNCH_SOURCE=""
EXECUTE=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      TASK_ROOT="$(cd "$2" && pwd)"
      shift 2
      ;;
    --task-file)
      TASK_FILE="$2"
      shift 2
      ;;
    --task-text)
      TASK_TEXT="$2"
      shift 2
      ;;
    --task-class)
      TASK_CLASS="$2"
      shift 2
      ;;
    --launch-source)
      LAUNCH_SOURCE="$2"
      shift 2
      ;;
    --execute)
      EXECUTE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$LAUNCH_SOURCE" ]]; then
  echo "--launch-source обязателен: chatgpt-handoff или direct-task" >&2
  exit 2
fi

BOOTSTRAP_ARGS=("$TASK_ROOT" "--launch-source" "$LAUNCH_SOURCE")
RESOLVE_ARGS=("$TASK_ROOT" "--launch-source" "$LAUNCH_SOURCE")
if [[ -n "$TASK_FILE" ]]; then
  BOOTSTRAP_ARGS+=("--task-file" "$TASK_FILE")
  RESOLVE_ARGS+=("--task-file" "$TASK_FILE")
fi
if [[ -n "$TASK_TEXT" ]]; then
  BOOTSTRAP_ARGS+=("--task-text" "$TASK_TEXT")
  RESOLVE_ARGS+=("--task-text" "$TASK_TEXT")
fi
if [[ -n "$TASK_CLASS" ]]; then
  BOOTSTRAP_ARGS+=("--task-class" "$TASK_CLASS")
  RESOLVE_ARGS+=("--task-class" "$TASK_CLASS")
fi

python3 "$ROOT/scripts/bootstrap-codex-task.py" "${BOOTSTRAP_ARGS[@]}"
PROFILE="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["selected_profile"])')"
MODEL="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["selected_model"])')"
REASONING="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["selected_reasoning_effort"])')"
PLAN_REASONING="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["selected_plan_mode_reasoning_effort"])')"
APPLY_MODE="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["apply_mode"])')"
STRICT_LAUNCH_MODE="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["strict_launch_mode"])')"
LAUNCH_COMMAND="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["launch_command"])')"
CODEX_COMMAND="$(python3 "$ROOT/scripts/resolve-codex-task-route.py" "${RESOLVE_ARGS[@]}" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["launch"]["codex_profile_command"])')"

echo "launch_boundary=new-task-launch"
echo "selected_profile=$PROFILE"
echo "selected_model=$MODEL"
echo "selected_reasoning_effort=$REASONING"
echo "selected_plan_mode_reasoning_effort=$PLAN_REASONING"
echo "apply_mode=$APPLY_MODE"
echo "strict_launch_mode=$STRICT_LAUNCH_MODE"
echo "launch_command=$LAUNCH_COMMAND"
echo "codex_command=$CODEX_COMMAND"

if [[ "$DRY_RUN" -eq 1 ]]; then
  exit 0
fi

if [[ "$EXECUTE" -eq 1 ]]; then
  cd "$TASK_ROOT"
  exec codex --profile "$PROFILE"
fi
