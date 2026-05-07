#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template"

read -rp "Название проекта: " PROJECT_NAME
read -rp "Slug проекта: " PROJECT_SLUG
ALLOW_RESERVED_SLUG="${FACTORY_ALLOW_RESERVED_SLUG:-false}"
RESERVED_SLUG_OVERRIDE="${FACTORY_RESERVED_SLUG_OVERRIDE:-false}"
if python3 "$SCRIPT_DIR/scripts/project_naming.py" is-reserved "$PROJECT_SLUG"; then
  if [ "$ALLOW_RESERVED_SLUG" != "true" ] && [ "$RESERVED_SLUG_OVERRIDE" != "true" ]; then
    read -rp "Slug '$PROJECT_SLUG' reserved/generic. Подтверждаете намеренное использование? [y/N]: " RESERVED_CONFIRM
    case "${RESERVED_CONFIRM,,}" in
      y|yes|д|да)
        RESERVED_SLUG_OVERRIDE="true"
        ALLOW_RESERVED_SLUG="true"
        ;;
      *)
        echo "Остановлено: выберите содержательный project_slug."
        exit 1
        ;;
    esac
  fi
fi
VALIDATE_SLUG_ARGS=("$SCRIPT_DIR/scripts/project_naming.py" validate "$PROJECT_SLUG")
if [ "$ALLOW_RESERVED_SLUG" = "true" ] || [ "$RESERVED_SLUG_OVERRIDE" = "true" ]; then
  VALIDATE_SLUG_ARGS+=("--allow-reserved")
fi
python3 "${VALIDATE_SLUG_ARGS[@]}"
DEFAULT_PROJECT_CODE="$(python3 "$SCRIPT_DIR/scripts/project_naming.py" code-from-slug "$PROJECT_SLUG")"
if [ -n "${FACTORY_PROJECT_CODE:-}" ]; then
  PROJECT_CODE="$FACTORY_PROJECT_CODE"
elif [ -t 0 ]; then
  read -rp "PROJECT_CODE проекта (uppercase, один раз при создании) [$DEFAULT_PROJECT_CODE]: " PROJECT_CODE
  PROJECT_CODE="${PROJECT_CODE:-$DEFAULT_PROJECT_CODE}"
else
  PROJECT_CODE="$DEFAULT_PROJECT_CODE"
fi
python3 "$SCRIPT_DIR/scripts/project_naming.py" validate-code "$PROJECT_CODE"
read -rp "Профиль проекта (greenfield-product/brownfield-with-repo-modernization/brownfield-with-repo-integration/brownfield-with-repo-audit/brownfield-without-repo) [greenfield-product]: " PROJECT_PRESET
PROJECT_PRESET="${PROJECT_PRESET:-greenfield-product}"

PROJECT_PRESET_FILE="$SCRIPT_DIR/project-presets.yaml"
COMPATIBILITY_ALIASES_FILE="$SCRIPT_DIR/compatibility-aliases.yaml"
readarray -t PRESET_VALUES < <(PROJECT_PRESET="$PROJECT_PRESET" PROJECT_PRESET_FILE="$PROJECT_PRESET_FILE" COMPATIBILITY_ALIASES_FILE="$COMPATIBILITY_ALIASES_FILE" python3 - <<'PY'
import os, yaml
from pathlib import Path
preset_file = Path(os.environ['PROJECT_PRESET_FILE'])
data = yaml.safe_load(preset_file.read_text(encoding='utf-8')) or {}
presets = data.get('project_presets', {})
aliases = {}
aliases_file = Path(os.environ['COMPATIBILITY_ALIASES_FILE'])
if aliases_file.exists():
    aliases_data = yaml.safe_load(aliases_file.read_text(encoding='utf-8')) or {}
    for alias, value in (aliases_data.get('preset_aliases', {}) or {}).items():
        aliases[alias] = value.get('target') if isinstance(value, dict) else value
else:
    aliases = data.get('preset_aliases', {})
resolved = aliases.get(os.environ['PROJECT_PRESET'], os.environ['PROJECT_PRESET'])
preset = presets.get(resolved, {})
print(resolved)
print(preset.get('default_mode', 'greenfield'))
print(preset.get('recommended_change_class', 'feature'))
print(preset.get('recommended_execution_mode', 'codex-led'))
print(preset.get('lifecycle_state', 'greenfield-active'))
conversion_required = bool(preset.get('conversion_required', False))
print(preset.get('target_lifecycle_state', 'greenfield-converted' if conversion_required else preset.get('lifecycle_state', 'greenfield-active')))
print(str(conversion_required).lower())
PY
)
PROJECT_PRESET="${PRESET_VALUES[0]:-greenfield-product}"
DEFAULT_MODE="${PRESET_VALUES[1]:-greenfield}"
DEFAULT_CLASS="${PRESET_VALUES[2]:-feature}"
DEFAULT_EXEC="${PRESET_VALUES[3]:-codex-led}"
LIFECYCLE_STATE="${PRESET_VALUES[4]:-greenfield-active}"
TARGET_LIFECYCLE_STATE="${PRESET_VALUES[5]:-greenfield-active}"
CONVERSION_REQUIRED="${PRESET_VALUES[6]:-false}"

read -rp "Режим старта (greenfield/brownfield) [${DEFAULT_MODE}]: " PROJECT_MODE
PROJECT_MODE="${PROJECT_MODE:-$DEFAULT_MODE}"
read -rp "Класс изменения (small-fix/feature/refactor/migration/brownfield-audit/brownfield-stabilization) [${DEFAULT_CLASS}]: " CHANGE_CLASS
CHANGE_CLASS="${CHANGE_CLASS:-$DEFAULT_CLASS}"
read -rp "Режим выполнения (manual/hybrid/codex-led) [${DEFAULT_EXEC}]: " EXEC_MODE
EXEC_MODE="${EXEC_MODE:-$DEFAULT_EXEC}"

DEST_DIR="./${PROJECT_SLUG}"
cp -R "$TEMPLATE_DIR" "$DEST_DIR"
PROJECT_NAME="$PROJECT_NAME" PROJECT_SLUG="$PROJECT_SLUG" PROJECT_CODE="$PROJECT_CODE" PROJECT_MODE="$PROJECT_MODE" LIFECYCLE_STATE="$LIFECYCLE_STATE" TARGET_LIFECYCLE_STATE="$TARGET_LIFECYCLE_STATE" DEST_DIR="$DEST_DIR" python3 - <<'PY'
import os
from pathlib import Path
repl = {
    "{{PROJECT_NAME}}": os.environ['PROJECT_NAME'],
    "{{PROJECT_SLUG}}": os.environ['PROJECT_SLUG'],
    "{{PROJECT_CODE}}": os.environ.get('PROJECT_CODE', ''),
    "{{PROJECT_MODE}}": os.environ['PROJECT_MODE'],
    "{{LIFECYCLE_STATE}}": os.environ['LIFECYCLE_STATE'],
    "{{TARGET_LIFECYCLE_STATE}}": os.environ['TARGET_LIFECYCLE_STATE'],
    "{{CURRENT_DATE}}": __import__("datetime").date.today().isoformat(),
}
for p in Path(os.environ['DEST_DIR']).rglob("*"):
    if p.is_file():
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for k, v in repl.items():
            txt = txt.replace(k, v)
        p.write_text(txt, encoding="utf-8")
PY
rm -f "$DEST_DIR/AGENT.md"
python3 "$SCRIPT_DIR/scripts/sync-agents.py" "$SCRIPT_DIR/AGENTS.md" "$DEST_DIR/AGENTS.md"
mkdir -p "$DEST_DIR/scripts"
cp -R "$SCRIPT_DIR/scripts/." "$DEST_DIR/scripts/"
find "$DEST_DIR/scripts" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$DEST_DIR/scripts" -type f -name "*.pyc" -delete
rm -f "$DEST_DIR/scripts/install-codex-dogfood-pack.sh"
cp "$SCRIPT_DIR/change-classes.yaml" "$DEST_DIR/change-classes.yaml"
cp "$SCRIPT_DIR/policy-presets.yaml" "$DEST_DIR/policy-presets.yaml"
cp "$SCRIPT_DIR/project-presets.yaml" "$DEST_DIR/project-presets.yaml"
cp "$SCRIPT_DIR/compatibility-aliases.yaml" "$DEST_DIR/compatibility-aliases.yaml"
cp "$SCRIPT_DIR/codex-routing.yaml" "$DEST_DIR/codex-routing.yaml"
cp "$SCRIPT_DIR/codex-model-routing.yaml" "$DEST_DIR/codex-model-routing.yaml"
if [ -d "$SCRIPT_DIR/../.github/ISSUE_TEMPLATE" ]; then
  mkdir -p "$DEST_DIR/.github/ISSUE_TEMPLATE"
  cp "$SCRIPT_DIR/../.github/ISSUE_TEMPLATE/"*.yml "$DEST_DIR/.github/ISSUE_TEMPLATE/"
fi
mkdir -p "$DEST_DIR/template-repo"
cp -R "$SCRIPT_DIR/scenario-pack" "$DEST_DIR/template-repo/scenario-pack"
cp "$SCRIPT_DIR/tree-contract.yaml" "$DEST_DIR/template-repo/tree-contract.yaml"
cp "$SCRIPT_DIR/mode-parity.yaml" "$DEST_DIR/template-repo/mode-parity.yaml"
mkdir -p "$DEST_DIR/reports/bugs" "$DEST_DIR/reports/factory-feedback" "$DEST_DIR/reports/handoffs" "$DEST_DIR/reports/release" "$DEST_DIR/tasks/chatgpt" "$DEST_DIR/tasks/codex"

CHANGE_ID="$($DEST_DIR/scripts/new-change-id.sh "$DEST_DIR")"
PROJECT_NAME="$PROJECT_NAME" CHANGE_CLASS="$CHANGE_CLASS" EXEC_MODE="$EXEC_MODE" CHANGE_ID="$CHANGE_ID" DEST_DIR="$DEST_DIR" PROJECT_MODE="$PROJECT_MODE" PROJECT_PRESET="$PROJECT_PRESET" LIFECYCLE_STATE="$LIFECYCLE_STATE" TARGET_LIFECYCLE_STATE="$TARGET_LIFECYCLE_STATE" CONVERSION_REQUIRED="$CONVERSION_REQUIRED" python3 - <<'PY'
import os, yaml
from pathlib import Path
root = Path(os.environ['DEST_DIR'])
task_index = yaml.safe_load((root/'.chatgpt/task-index.yaml').read_text(encoding='utf-8'))
task_index['change']['id'] = os.environ['CHANGE_ID']
task_index['change']['class'] = os.environ['CHANGE_CLASS']
task_index['change']['execution_mode'] = os.environ['EXEC_MODE']
task_index['change']['title'] = f"{os.environ['PROJECT_NAME']}: {os.environ['CHANGE_CLASS']}"
(root/'.chatgpt/task-index.yaml').write_text(yaml.safe_dump(task_index, allow_unicode=True, sort_keys=False), encoding='utf-8')
stage = yaml.safe_load((root/'.chatgpt/stage-state.yaml').read_text(encoding='utf-8'))
stage['project']['mode'] = os.environ['PROJECT_MODE']
stage.setdefault('lifecycle', {})
stage['lifecycle']['lifecycle_state'] = os.environ['LIFECYCLE_STATE']
stage['lifecycle']['target_lifecycle_state'] = os.environ['TARGET_LIFECYCLE_STATE']
stage['lifecycle']['conversion_required'] = os.environ['CONVERSION_REQUIRED'] == 'true'
stage['lifecycle']['conversion_gate_status'] = 'pending' if os.environ['CONVERSION_REQUIRED'] == 'true' else 'not_applicable'
(root/'.chatgpt/stage-state.yaml').write_text(yaml.safe_dump(stage, allow_unicode=True, sort_keys=False), encoding='utf-8')
active = yaml.safe_load((root/'.chatgpt/active-scenarios.yaml').read_text(encoding='utf-8'))
active['project_preset'] = os.environ['PROJECT_PRESET']
(root/'.chatgpt/active-scenarios.yaml').write_text(yaml.safe_dump(active, allow_unicode=True, sort_keys=False), encoding='utf-8')
PY
(
  cd "$DEST_DIR"
  ./scripts/apply-project-preset.py "$PROJECT_PRESET" project-presets.yaml .chatgpt/project-profile.yaml .chatgpt/active-scenarios.yaml
  ./scripts/apply-policy-preset.py .chatgpt/task-index.yaml policy-presets.yaml .chatgpt/policy-status.yaml
)

PROJECT_NAME="$PROJECT_NAME" PROJECT_SLUG="$PROJECT_SLUG" PROJECT_MODE="$PROJECT_MODE" PROJECT_PRESET="$PROJECT_PRESET" CHANGE_CLASS="$CHANGE_CLASS" EXEC_MODE="$EXEC_MODE" CHANGE_ID="$CHANGE_ID" DEST_DIR="$DEST_DIR" RESERVED_SLUG_OVERRIDE="$RESERVED_SLUG_OVERRIDE" python3 - <<'PY'
import os, yaml, datetime
from pathlib import Path

root = Path(os.environ['DEST_DIR'])
chat = root / '.chatgpt'
policy = yaml.safe_load((chat / 'policy-status.yaml').read_text(encoding='utf-8')) or {}
handoff = policy.get('handoff_policy', 'forbidden')
needs_codex = {'required': 'да', 'optional': 'опционально', 'forbidden': 'нет'}.get(handoff, 'нет')

origin = f"""# Происхождение проекта

## Название проекта
{os.environ['PROJECT_NAME']}

## Slug
{os.environ['PROJECT_SLUG']}

## project_slug
{os.environ['PROJECT_SLUG']}

## Reserved slug override
{str(os.environ.get('RESERVED_SLUG_OVERRIDE') == 'true').lower()}

## Тип проекта
{os.environ['PROJECT_MODE']}

## Создан из фабрики
factory-v2.5.0

## Версия фабрики
2.5.0

## Дата создания
{datetime.date.today().isoformat()}

## Исходный профиль проекта
{os.environ['PROJECT_PRESET']}

## Исходный класс изменения
{os.environ['CHANGE_CLASS']}

## Исходный режим выполнения
{os.environ['EXEC_MODE']}

## Комментарий
Проект создан через launcher фабрики.
"""
(chat / 'project-origin.md').write_text(origin, encoding='utf-8')

classification = f"""# Классификация текущего цикла

## Тип проекта
{os.environ['PROJECT_MODE']}

## Тип работы
{os.environ['CHANGE_CLASS']}

## Требуется ли Codex
{needs_codex}

## Это проблема проекта или фабрики
project

## Обоснование
Классификация создана автоматически на основе выбранного режима, класса изменения и policy preset.

## Следующее действие
Проверить актуальность scenario-pack, затем заполнить reality-check и decision policy.

## Нужен ли feedback в фабрику
нет

## Нужен ли drift-check
нет

## Нужна ли обратная синхронизация
нет

## Есть ли обнаруженный дефект
нет

## Нужен ли bug report
нет

## Слой дефекта
project-only

## Нужен ли ChatGPT handoff bug note
нет

## Можно ли продолжать fix без bug report
нет

## Допустим ли controlled apply по safe-зонам
нет
"""
(chat / 'classification.md').write_text(classification, encoding='utf-8')

bugflow = f'''defect_detected: false  # Обнаружен ли дефект
bug_report_required: false  # Требуется ли bug report
bug_report_created: false  # Создан ли bug report

defect_layer: "project-only"  # project-only / factory-template / shared-unknown

factory_feedback_required: false  # Требуется ли feedback в фабрику
factory_feedback_created: false  # Создан ли feedback в фабрику

chatgpt_bug_handoff_required: false  # Нужен ли отдельный ChatGPT handoff
chatgpt_bug_handoff_created: false  # Создан ли handoff

codex_bug_capture_required: true  # Должен ли Codex получить defect-capture block
silent_fix_forbidden: true  # Silent fix запрещен
'''
(chat / 'bugflow-status.yaml').write_text(bugflow, encoding='utf-8')

registry_path = chat / 'task-registry.yaml'
if registry_path.exists():
    registry = yaml.safe_load(registry_path.read_text(encoding='utf-8')) or {}
    if isinstance(registry, dict):
        policy = registry.setdefault('task_id_policy', {})
        if isinstance(policy, dict):
            policy['source_of_truth'] = '.chatgpt/task-registry.yaml'
        for task in registry.get('tasks', []) or []:
            if isinstance(task, dict) and task.get('status') == 'not_applicable':
                task['verification_commands'] = [
                    'python3 scripts/validate-task-registry.py .chatgpt/task-registry.yaml',
                    'bash scripts/verify-all.sh quick',
                ]
        registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding='utf-8')

dashboard_path = chat / 'project-lifecycle-dashboard.yaml'
if dashboard_path.exists():
    dashboard = yaml.safe_load(dashboard_path.read_text(encoding='utf-8')) or {}
    if isinstance(dashboard, dict):
        project = dashboard.setdefault('project', {})
        if isinstance(project, dict):
            project['name'] = os.environ['PROJECT_NAME']
            project['slug'] = os.environ['PROJECT_SLUG']
            project['profile'] = os.environ['PROJECT_PRESET']
            project['lifecycle_state'] = os.environ.get('LIFECYCLE_STATE', project.get('lifecycle_state', 'greenfield-active'))
            project['current_mode'] = os.environ['PROJECT_MODE']
            project['owner_boundary'] = 'project-owned'
        active_change = dashboard.setdefault('active_change', {})
        if isinstance(active_change, dict):
            active_change.update({
                'id': os.environ['CHANGE_ID'],
                'title': f"{os.environ['PROJECT_NAME']}: initial scaffold",
                'class': os.environ['CHANGE_CLASS'],
                'priority': 'medium',
                'status': 'draft',
                'owner_boundary': 'internal-repo-follow-up',
                'evidence': ['.chatgpt/task-index.yaml', '.chatgpt/project-origin.md'],
                'source_artifacts': ['.chatgpt/task-index.yaml', '.chatgpt/project-origin.md'],
            })
        execution = dashboard.setdefault('multi_step_execution', {})
        if isinstance(execution, dict):
            execution['current_wave'] = 1
            execution['waves'] = [{
                'id': 'wave-1',
                'title': 'Initial project scaffold materialization',
                'status': 'completed',
                'evidence': ['.chatgpt/task-index.yaml', '.chatgpt/project-origin.md'],
                'tasks': [{
                    'id': 'T-001',
                    'title': 'Materialize generated project scaffold',
                    'status': 'completed',
                    'owner_boundary': 'internal-repo-follow-up',
                    'evidence': ['.chatgpt/task-index.yaml', '.chatgpt/project-origin.md'],
                }],
            }]
            execution['completed_tasks'] = ['T-001']
            execution['blocked_tasks'] = []
            execution['next_task'] = {
                'id': 'T-PLAN',
                'owner_boundary': 'internal-repo-follow-up',
                'action': 'Run repo-first router and continue the project scenario from the generated project.',
            }
            execution['final_verification'] = {
                'status': 'pending',
                'evidence': [],
            }
            execution['archive_to_work_completed'] = {
                'allowed': False,
                'reason': 'Initial scaffold is not a completed product change yet.',
            }
        orchestration = dashboard.setdefault('handoff_orchestration', {})
        if isinstance(orchestration, dict):
            orchestration['parent_handoff'] = {
                'id': 'not_allocated',
                'title': 'No ChatGPT handoff allocated inside this generated repo yet',
                'status': 'not_started',
                'evidence': [],
            }
            orchestration['child_tasks'] = []
            orchestration['route_explanation_boundary'] = (
                'Advisory layer показывает маршрут и handoff-текст, но не переключает '
                'model/profile/reasoning внутри уже открытой Codex-сессии; надежная '
                'executable boundary — новый task launch или ручной picker в новом чате.'
            )
        dashboard['source_artifacts'] = [
            '.chatgpt/task-index.yaml',
            '.chatgpt/chat-handoff-index.yaml',
            '.chatgpt/handoff-implementation-register.yaml',
            '.chatgpt/project-origin.md',
        ]
        control = dashboard.setdefault('universal_task_control', {})
        if isinstance(control, dict):
            control['registry_path'] = '.chatgpt/task-registry.yaml'
            control['status'] = 'pending'
            control['evidence'] = [
                '.chatgpt/task-registry.yaml',
                'scripts/validate-task-registry.py',
                'scripts/allocate-task-id.py',
                'scripts/issue-to-task-registry.py',
                'scripts/preview-task-handoff.py',
                'scripts/update-task-status.py',
                'scripts/prepare-task-pack.py',
                'scripts/render-task-queue.py',
                'reports/task-queue.md',
            ]
        dashboard_path.write_text(yaml.safe_dump(dashboard, allow_unicode=True, sort_keys=False), encoding='utf-8')

today = datetime.date.today().isoformat()

version_md = f'''# Версия проекта

## Текущая версия проекта
0.1.0

## Статус
{os.environ['PROJECT_MODE']}-draft

## Дата последнего обновления
{today}

## Версия фабрики-источника
2.5.0

## Тип проекта
{os.environ['PROJECT_MODE']}
'''
(root / 'VERSION.md').write_text(version_md, encoding='utf-8')

changelog_md = f'''# Журнал изменений проекта

## [0.1.0] - {today}
### Добавлено
- первичная генерация проекта из фабрики 2.5.0
- controlled software update governance artifacts: `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml`, `reports/software-updates/README.md`

### Изменено
- 

### Исправлено
- 
'''
(root / 'CHANGELOG.md').write_text(changelog_md, encoding='utf-8')

current_state_md = '''# Текущее функциональное состояние проекта

## Что уже реализовано
- базовый каркас проекта
- `.chatgpt` и presets
- defect-capture и versioning layer
- controlled software update governance artifacts: inventory, watchlist, readiness и reports/software-updates

## Что работает стабильно
- launcher и базовые structural validators
- software update governance validator после materialization scripts

## Что работает частично
- содержательное наполнение артефактов требует сценарного слоя

## Что еще не реализовано
- предметная реализация проекта

## Известные ограничения
- реальные процессы и модули должны быть дополнены вручную или через сценарии

## Следующий приоритетный шаг
- заполнить reality-check, user-spec и task-index
- заполнить `.chatgpt/software-inventory.yaml`, проверить `unattended-upgrades` и обновить watchlist/readiness перед deploy/operate
'''
(root / 'CURRENT_FUNCTIONAL_STATE.md').write_text(current_state_md, encoding='utf-8')
PY

python3 "$DEST_DIR/scripts/materialize-project-indexes.py" \
  --root "$DEST_DIR" \
  --project-code "$PROJECT_CODE"

python3 "$DEST_DIR/scripts/render-project-lifecycle-dashboard.py" \
  --input "$DEST_DIR/.chatgpt/project-lifecycle-dashboard.yaml" \
  --format markdown-full \
  --output "$DEST_DIR/reports/project-lifecycle-dashboard.md"
python3 "$DEST_DIR/scripts/render-project-lifecycle-dashboard.py" \
  --input "$DEST_DIR/.chatgpt/project-lifecycle-dashboard.yaml" \
  --format chatgpt-card \
  --output "$DEST_DIR/reports/project-status-card.md"

REGISTRY_FILE="$(cd "$SCRIPT_DIR/.." && pwd)/factory/producer/registry/projects-created.md"
REGISTRY_MODE="${FACTORY_REGISTRY_MODE:-production}"
if [ "$REGISTRY_MODE" != "skip" ] && [ -f "$REGISTRY_FILE" ] && [ -w "$REGISTRY_FILE" ]; then
  {
    echo "- дата: $(date +%F)"
    echo "  проект: $PROJECT_NAME"
    echo "  slug: $PROJECT_SLUG"
    echo "  версия_фабрики: 2.5.0"
    echo "  режим: $PROJECT_MODE"
    echo "  статус_записи: $REGISTRY_MODE"
    echo "  project_preset: $PROJECT_PRESET"
    echo "  change_class: $CHANGE_CLASS"
    echo "  execution_mode: $EXEC_MODE"
    echo "  reserved_slug_override: $RESERVED_SLUG_OVERRIDE"
    echo "  примечание: создан через launcher"
  } >> "$REGISTRY_FILE"
fi

create_or_reuse_github_repo() {
  local project_dir="$1"
  local owner="${FACTORY_GITHUB_OWNER:-}"
  local visibility="${FACTORY_GITHUB_VISIBILITY:-private}"
  local reuse_existing="${FACTORY_GITHUB_REUSE_EXISTING:-false}"
  local repo_full
  local origin_url
  local origin_name
  if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub repo не создан: gh CLI не найден." >&2
    return 1
  fi
  if ! gh auth status >/dev/null 2>&1; then
    echo "GitHub repo не создан: gh CLI не авторизован." >&2
    return 1
  fi
  if [ -z "$owner" ]; then
    owner="$(gh api user --jq .login 2>/dev/null || true)"
  fi
  if [ -z "$owner" ]; then
    echo "GitHub repo не создан: owner неоднозначен. Передайте --github-owner/FACTORY_GITHUB_OWNER." >&2
    return 1
  fi
  if [ "$visibility" != "private" ] && [ "$visibility" != "public" ]; then
    echo "GitHub repo не создан: visibility должен быть private или public." >&2
    return 1
  fi
  repo_full="$owner/$PROJECT_SLUG"
  if [ ! -d "$project_dir/.git" ]; then
    git -C "$project_dir" init -b main
  fi
  ensure_project_git_identity "$project_dir"
  if git -C "$project_dir" remote get-url origin >/dev/null 2>&1; then
    origin_url="$(git -C "$project_dir" remote get-url origin)"
    origin_name="$(PYTHONPATH="$SCRIPT_DIR/scripts" python3 - "$origin_url" <<'PY'
import sys
from project_naming import remote_repo_name
print(remote_repo_name(sys.argv[1]))
PY
)"
    if [ "$origin_name" != "$PROJECT_SLUG" ]; then
      echo "GitHub repo не создан: origin repo '$origin_name' не совпадает с project_slug '$PROJECT_SLUG'." >&2
      return 1
    fi
  fi
  if gh repo view "$repo_full" >/dev/null 2>&1; then
    if [ "$reuse_existing" != "true" ]; then
      read -rp "GitHub repo '$repo_full' уже существует. Это тот же проект и его можно использовать? [y/N]: " REUSE_CONFIRM
      case "${REUSE_CONFIRM,,}" in
        y|yes|д|да) reuse_existing="true" ;;
        *) echo "Остановлено: repo exists but reuse is not confirmed." >&2; return 1 ;;
      esac
    fi
    if ! git -C "$project_dir" remote get-url origin >/dev/null 2>&1; then
      git -C "$project_dir" remote add origin "https://github.com/$repo_full.git"
    fi
  fi
  if ! git -C "$project_dir" rev-parse --verify HEAD >/dev/null 2>&1; then
    git -C "$project_dir" add .
    git -C "$project_dir" commit -m "Initial factory project scaffold"
  fi
  if gh repo view "$repo_full" >/dev/null 2>&1; then
    git -C "$project_dir" push -u origin HEAD
  else
    local visibility_arg="--private"
    if [ "$visibility" = "public" ]; then
      visibility_arg="--public"
    fi
    gh repo create "$repo_full" "$visibility_arg" --source="$project_dir" --remote=origin --push
  fi
}

ensure_project_git_identity() {
  local project_dir="$1"
  local current_name
  local current_email
  local gh_login
  local gh_id
  local gh_name
  local gh_email
  current_name="$(git -C "$project_dir" config user.name || true)"
  current_email="$(git -C "$project_dir" config user.email || true)"
  if [ -n "$current_name" ] && [ -n "$current_email" ]; then
    return 0
  fi

  gh_login="$(gh api user --jq .login 2>/dev/null || true)"
  gh_id="$(gh api user --jq .id 2>/dev/null || true)"
  gh_name="$(gh api user --jq .name 2>/dev/null || true)"
  gh_email="$(gh api user --jq .email 2>/dev/null || true)"
  if [ "$gh_name" = "null" ] || [ -z "$gh_name" ]; then
    gh_name="$gh_login"
  fi
  if [ "$gh_email" = "null" ] || [ -z "$gh_email" ]; then
    if [ -n "$gh_id" ] && [ -n "$gh_login" ]; then
      gh_email="${gh_id}+${gh_login}@users.noreply.github.com"
    fi
  fi

  if [ -z "$gh_name" ] || [ -z "$gh_email" ]; then
    echo "GitHub repo не создан: git user.name/user.email не настроены, а gh не вернул login/id для локальной identity." >&2
    echo "Настройте git identity или повторите после восстановления gh auth." >&2
    return 1
  fi
  if [ -z "$current_name" ]; then
    git -C "$project_dir" config user.name "$gh_name"
  fi
  if [ -z "$current_email" ]; then
    git -C "$project_dir" config user.email "$gh_email"
  fi
}

if [ "${FACTORY_CREATE_GITHUB_REPO:-false}" = "true" ]; then
  create_or_reuse_github_repo "$DEST_DIR"
fi

echo
echo "Проект создан: $DEST_DIR"
echo "Change ID: $CHANGE_ID"
echo "PROJECT_CODE: $PROJECT_CODE"
echo "Профиль проекта: $PROJECT_PRESET"
echo "Дальше:"
echo "1. Создайте ChatGPT Project"
echo "2. Добавьте в инструкции проекта repo-first правило: сначала открыть GitHub repo и прочитать template-repo/scenario-pack/00-master-router.md"
echo "3. Начните с 00-master-router.md и затем выберите entry path по типу проекта:"
echo "   - greenfield: 04-discovery-new-project.md"
echo "   - brownfield без repo: brownfield/00-brownfield-entry.md"
echo "   - brownfield с repo: brownfield/00-brownfield-entry.md -> brownfield/01-system-inventory.md"
echo "4. Обновляйте .chatgpt/ по мере прохождения сценариев"
echo "5. Перед handoff запустите проверки:"
echo "   ./scripts/validate-task-graph.py"
echo "   ./scripts/validate-change-profile.py"
echo "   ./scripts/validate-project-preset.py"
echo "   ./scripts/validate-policy-preset.py"
echo "   ./scripts/validate-versioning-layer.py"
echo "6. Для интерактивной работы в VS Code Codex extension используйте manual-ui path по умолчанию: новый чат/окно Codex, ручной выбор model/reasoning в picker, затем вставка handoff."
echo "7. Launcher path ./scripts/launch-codex-task.sh --launch-source <chatgpt-handoff|direct-task> ... остается optional strict mode для automation, reproducibility и shell-first запуска."
echo "8. Не считайте уже открытую сессию, новый чат без проверки picker или простой текст handoff надежным auto-switch profile/model."
echo "9. Model availability auto-check: ./scripts/check-codex-model-catalog.py . проверяет live Codex catalog; новые model IDs сначала оформляются как proposal, без automatic profile promotion."
