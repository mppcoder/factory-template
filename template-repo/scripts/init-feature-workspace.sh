#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  cat <<USAGE
Usage:
  $0 --feature-id <feature-id> [--title <feature title>] [--idea <rough idea>] [--base-dir <path>] [--force]

Examples:
  $0 --feature-id feat-login
  $0 --feature-id feat-billing --title "Простой биллинг" --idea "Сократить ошибки оплаты"
USAGE
}

FEATURE_ID=""
FEATURE_TITLE=""
FEATURE_IDEA=""
BASE_DIR="work/features"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --feature-id)
      FEATURE_ID="${2:-}"
      shift 2
      ;;
    --title)
      FEATURE_TITLE="${2:-}"
      shift 2
      ;;
    --idea)
      FEATURE_IDEA="${2:-}"
      shift 2
      ;;
    --base-dir)
      BASE_DIR="${2:-}"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Неизвестный аргумент: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$FEATURE_ID" ]]; then
  echo "--feature-id обязателен" >&2
  usage
  exit 2
fi

if [[ "$BASE_DIR" = /* ]]; then
  WORKSPACE="$BASE_DIR/$FEATURE_ID"
else
  WORKSPACE="$ROOT/$BASE_DIR/$FEATURE_ID"
fi

if [[ -d "$WORKSPACE" && "$FORCE" != "true" ]]; then
  echo "Workspace уже существует: $WORKSPACE"
  echo "Добавьте --force, если хотите продолжить и перезаписать шаблоны."
  exit 1
fi

mkdir -p "$WORKSPACE/specs" "$WORKSPACE/tasks" "$WORKSPACE/notes"

resolve_template() {
  local rel="$1"
  local candidate
  for candidate in \
    "$ROOT/work-templates/$rel" \
    "$ROOT/template/work-templates/$rel" \
    "$ROOT/template-repo/template/work-templates/$rel"
  do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

copy_template_if_needed() {
  local src="$1"
  local dst="$2"
  if [[ -f "$dst" && "$FORCE" != "true" ]]; then
    return 0
  fi
  cp "$src" "$dst"
}

USER_TEMPLATE="$(resolve_template "user-spec.md.template")"
TECH_TEMPLATE="$(resolve_template "tech-spec.md.template")"
TASK_TEMPLATE="$(resolve_template "tasks/task.md.template")"

copy_template_if_needed "$USER_TEMPLATE" "$WORKSPACE/specs/user-spec.md"
copy_template_if_needed "$TECH_TEMPLATE" "$WORKSPACE/specs/tech-spec.md"
copy_template_if_needed "$TASK_TEMPLATE" "$WORKSPACE/tasks/task.template.md"

RESUME_SCRIPT="$SCRIPT_DIR/resume-setup.py"
if [[ ! -f "$RESUME_SCRIPT" ]]; then
  RESUME_SCRIPT="$ROOT/scripts/resume-setup.py"
fi
GENERATE_SCRIPT="$SCRIPT_DIR/generate-user-spec.py"
if [[ ! -f "$GENERATE_SCRIPT" ]]; then
  GENERATE_SCRIPT="$ROOT/scripts/generate-user-spec.py"
fi
DECOMPOSE_SCRIPT="$SCRIPT_DIR/decompose-feature.py"
if [[ ! -f "$DECOMPOSE_SCRIPT" ]]; then
  DECOMPOSE_SCRIPT="$ROOT/scripts/decompose-feature.py"
fi

cat > "$WORKSPACE/README.md" <<README
# Feature workspace: $FEATURE_ID

Этот workspace поддерживает resumable planning:
1. Заполните интервью (можно частями):
   python3 "$RESUME_SCRIPT" --workspace "$WORKSPACE" --answer problem="..."
2. Сгенерируйте user-spec:
   python3 "$GENERATE_SCRIPT" --workspace "$WORKSPACE"
3. Сгенерируйте tech-spec и задачи:
   python3 "$DECOMPOSE_SCRIPT" --workspace "$WORKSPACE"

Можно остановиться в любой момент и вернуться позже: состояние хранится в interview-state.yaml.
README

RESUME_ARGS=("$RESUME_SCRIPT" "--workspace" "$WORKSPACE" "--feature-id" "$FEATURE_ID")
if [[ -n "$FEATURE_TITLE" ]]; then
  RESUME_ARGS+=("--feature-title" "$FEATURE_TITLE")
fi
if [[ -n "$FEATURE_IDEA" ]]; then
  RESUME_ARGS+=("--idea" "$FEATURE_IDEA")
fi

python3 "${RESUME_ARGS[@]}" >/dev/null

echo "Feature workspace инициализирован: $WORKSPACE"
echo "Файлы:" 
echo "- $WORKSPACE/interview-state.yaml"
echo "- $WORKSPACE/specs/user-spec.md"
echo "- $WORKSPACE/specs/tech-spec.md"
echo "- $WORKSPACE/tasks/task.template.md"
echo "Следующий шаг:"
echo "python3 $RESUME_SCRIPT --workspace \"$WORKSPACE\""
