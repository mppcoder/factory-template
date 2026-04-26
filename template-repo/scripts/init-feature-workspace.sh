#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  cat <<USAGE
Usage:
  $0 --feature-id <feature-id> [--title <feature title>] [--idea <rough idea>] [--base-dir <path>] [--advanced-execution] [--force]

Examples:
  $0 --feature-id feat-login
  $0 --feature-id feat-billing --title "Простой биллинг" --idea "Сократить ошибки оплаты"
  $0 --feature-id feat-risky --advanced-execution
USAGE
}

FEATURE_ID=""
FEATURE_TITLE=""
FEATURE_IDEA=""
BASE_DIR="work/features"
FORCE="false"
ADVANCED_EXECUTION="false"

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
    --advanced-execution)
      ADVANCED_EXECUTION="true"
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
if [[ "$ADVANCED_EXECUTION" == "true" ]]; then
  mkdir -p "$WORKSPACE/logs"
fi

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
DECISIONS_TEMPLATE="$(resolve_template "decisions.md.template")"

copy_template_if_needed "$USER_TEMPLATE" "$WORKSPACE/specs/user-spec.md"
copy_template_if_needed "$TECH_TEMPLATE" "$WORKSPACE/specs/tech-spec.md"
copy_template_if_needed "$TASK_TEMPLATE" "$WORKSPACE/tasks/task.template.md"
copy_template_if_needed "$DECISIONS_TEMPLATE" "$WORKSPACE/decisions.md"

if [[ "$ADVANCED_EXECUTION" == "true" ]]; then
  EXECUTION_PLAN_TEMPLATE="$(resolve_template "execution-plan.md.template")"
  CHECKPOINT_TEMPLATE="$(resolve_template "checkpoint.yaml.template")"
  copy_template_if_needed "$EXECUTION_PLAN_TEMPLATE" "$WORKSPACE/logs/execution-plan.md"
  copy_template_if_needed "$CHECKPOINT_TEMPLATE" "$WORKSPACE/logs/checkpoint.yaml"
fi

DECISIONS_TITLE="${FEATURE_TITLE:-$FEATURE_ID}"
if [[ ! -f "$WORKSPACE/decisions.md" || "$FORCE" == "true" || "$(grep -c '{{' "$WORKSPACE/decisions.md" 2>/dev/null || true)" != "0" ]]; then
  cat > "$WORKSPACE/decisions.md" <<DECISIONS
# Decisions Log: $DECISIONS_TITLE

> generated_at: $(date -Iseconds)
> feature_id: $FEATURE_ID
> Этот файл хранит важные решения, отклонения и проверки после выполнения задач.

## Как пользоваться

- Записывайте только решения, которые помогут будущему участнику понять, почему работа сделана именно так.
- Если задача отклонилась от user-spec, укажите связанный \`DEV-*\` и \`US-*\`.
- Если решение стало устойчивым правилом проекта, перенесите вывод в \`project-knowledge/\`.
- Для feature-execution-lite фиксируйте wave, review rounds и boundary: internal work, external user action или runtime backlog.

## Записи

- Пока записей нет.
DECISIONS
fi

if [[ "$ADVANCED_EXECUTION" == "true" ]]; then
  escape_sed_replacement() {
    printf '%s' "$1" | sed -e 's/[\/&]/\\&/g'
  }
  ADVANCED_TITLE="$(escape_sed_replacement "${FEATURE_TITLE:-$FEATURE_ID}")"
  ADVANCED_ID="$(escape_sed_replacement "$FEATURE_ID")"
  ADVANCED_TIME="$(escape_sed_replacement "$(date -Iseconds)")"
  sed -i \
    -e "s/{{FEATURE_ID}}/$ADVANCED_ID/g" \
    -e "s/{{FEATURE_TITLE}}/$ADVANCED_TITLE/g" \
    -e "s/{{GENERATED_AT}}/$ADVANCED_TIME/g" \
    "$WORKSPACE/logs/execution-plan.md" "$WORKSPACE/logs/checkpoint.yaml"
fi

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
Если нужен advanced feature execution, создайте workspace с --advanced-execution и ведите logs/checkpoint.yaml после каждой wave.
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
echo "- $WORKSPACE/decisions.md"
if [[ "$ADVANCED_EXECUTION" == "true" ]]; then
  echo "- $WORKSPACE/logs/execution-plan.md"
  echo "- $WORKSPACE/logs/checkpoint.yaml"
fi
echo "Следующий шаг:"
echo "python3 $RESUME_SCRIPT --workspace \"$WORKSPACE\""
echo "Или вернитесь в guided launcher:"
echo "python3 $ROOT/scripts/factory-launcher.py --continue"
