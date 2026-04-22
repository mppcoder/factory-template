#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template"

read -rp "Название проекта: " PROJECT_NAME
read -rp "Slug проекта: " PROJECT_SLUG
read -rp "Профиль проекта (product-dev/legacy-modernization/integration-project/audit-only/brownfield-dogfood-codex-assisted) [product-dev]: " PROJECT_PRESET
PROJECT_PRESET="${PROJECT_PRESET:-product-dev}"

PROJECT_PRESET_FILE="$SCRIPT_DIR/project-presets.yaml"
readarray -t PRESET_VALUES < <(PROJECT_PRESET="$PROJECT_PRESET" PROJECT_PRESET_FILE="$PROJECT_PRESET_FILE" python3 - <<'PY'
import os, yaml
from pathlib import Path
preset_file = Path(os.environ['PROJECT_PRESET_FILE'])
presets = yaml.safe_load(preset_file.read_text(encoding='utf-8')).get('project_presets', {})
preset = presets.get(os.environ['PROJECT_PRESET'], {})
print(preset.get('default_mode', 'greenfield'))
print(preset.get('recommended_change_class', 'feature'))
print(preset.get('recommended_execution_mode', 'codex-led'))
PY
)
DEFAULT_MODE="${PRESET_VALUES[0]:-greenfield}"
DEFAULT_CLASS="${PRESET_VALUES[1]:-feature}"
DEFAULT_EXEC="${PRESET_VALUES[2]:-codex-led}"

read -rp "Режим старта (greenfield/brownfield) [${DEFAULT_MODE}]: " PROJECT_MODE
PROJECT_MODE="${PROJECT_MODE:-$DEFAULT_MODE}"
read -rp "Класс изменения (small-fix/feature/refactor/migration/brownfield-audit/brownfield-stabilization) [${DEFAULT_CLASS}]: " CHANGE_CLASS
CHANGE_CLASS="${CHANGE_CLASS:-$DEFAULT_CLASS}"
read -rp "Режим выполнения (manual/hybrid/codex-led) [${DEFAULT_EXEC}]: " EXEC_MODE
EXEC_MODE="${EXEC_MODE:-$DEFAULT_EXEC}"

DEST_DIR="./${PROJECT_SLUG}"
cp -R "$TEMPLATE_DIR" "$DEST_DIR"
PROJECT_NAME="$PROJECT_NAME" PROJECT_SLUG="$PROJECT_SLUG" PROJECT_MODE="$PROJECT_MODE" DEST_DIR="$DEST_DIR" python3 - <<'PY'
import os
from pathlib import Path
repl = {
    "{{PROJECT_NAME}}": os.environ['PROJECT_NAME'],
    "{{PROJECT_SLUG}}": os.environ['PROJECT_SLUG'],
    "{{PROJECT_MODE}}": os.environ['PROJECT_MODE'],
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
cp "$SCRIPT_DIR/change-classes.yaml" "$DEST_DIR/change-classes.yaml"
cp "$SCRIPT_DIR/policy-presets.yaml" "$DEST_DIR/policy-presets.yaml"
cp "$SCRIPT_DIR/project-presets.yaml" "$DEST_DIR/project-presets.yaml"
cp "$SCRIPT_DIR/codex-routing.yaml" "$DEST_DIR/codex-routing.yaml"
mkdir -p "$DEST_DIR/template-repo"
cp -R "$SCRIPT_DIR/scenario-pack" "$DEST_DIR/template-repo/scenario-pack"
mkdir -p "$DEST_DIR/reports/bugs" "$DEST_DIR/reports/factory-feedback" "$DEST_DIR/tasks/chatgpt" "$DEST_DIR/tasks/codex"

CHANGE_ID="$($DEST_DIR/scripts/new-change-id.sh "$DEST_DIR")"
PROJECT_NAME="$PROJECT_NAME" CHANGE_CLASS="$CHANGE_CLASS" EXEC_MODE="$EXEC_MODE" CHANGE_ID="$CHANGE_ID" DEST_DIR="$DEST_DIR" PROJECT_MODE="$PROJECT_MODE" PROJECT_PRESET="$PROJECT_PRESET" python3 - <<'PY'
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

PROJECT_NAME="$PROJECT_NAME" PROJECT_SLUG="$PROJECT_SLUG" PROJECT_MODE="$PROJECT_MODE" PROJECT_PRESET="$PROJECT_PRESET" CHANGE_CLASS="$CHANGE_CLASS" EXEC_MODE="$EXEC_MODE" CHANGE_ID="$CHANGE_ID" DEST_DIR="$DEST_DIR" python3 - <<'PY'
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

## Тип проекта
{os.environ['PROJECT_MODE']}

## Создан из фабрики
factory-v2.4.3

## Версия фабрики
2.4.3

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

today = datetime.date.today().isoformat()

version_md = f'''# Версия проекта

## Текущая версия проекта
0.1.0

## Статус
{os.environ['PROJECT_MODE']}-draft

## Дата последнего обновления
{today}

## Версия фабрики-источника
2.4.3

## Тип проекта
{os.environ['PROJECT_MODE']}
'''
(root / 'VERSION.md').write_text(version_md, encoding='utf-8')

changelog_md = f'''# Журнал изменений проекта

## [0.1.0] - {today}
### Добавлено
- первичная генерация проекта из фабрики 2.4.3

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

## Что работает стабильно
- launcher и базовые structural validators

## Что работает частично
- содержательное наполнение артефактов требует сценарного слоя

## Что еще не реализовано
- предметная реализация проекта

## Известные ограничения
- реальные процессы и модули должны быть дополнены вручную или через сценарии

## Следующий приоритетный шаг
- заполнить reality-check, user-spec и task-index
'''
(root / 'CURRENT_FUNCTIONAL_STATE.md').write_text(current_state_md, encoding='utf-8')
PY

REGISTRY_FILE="$(cd "$SCRIPT_DIR/.." && pwd)/registry/projects-created.md"
REGISTRY_MODE="${FACTORY_REGISTRY_MODE:-production}"
if [ "$REGISTRY_MODE" != "skip" ] && [ -f "$REGISTRY_FILE" ] && [ -w "$REGISTRY_FILE" ]; then
  {
    echo "- дата: $(date +%F)"
    echo "  проект: $PROJECT_NAME"
    echo "  slug: $PROJECT_SLUG"
    echo "  версия_фабрики: 2.4.3"
    echo "  режим: $PROJECT_MODE"
    echo "  статус_записи: $REGISTRY_MODE"
    echo "  project_preset: $PROJECT_PRESET"
    echo "  change_class: $CHANGE_CLASS"
    echo "  execution_mode: $EXEC_MODE"
    echo "  примечание: создан через launcher"
  } >> "$REGISTRY_FILE"
fi

echo
echo "Проект создан: $DEST_DIR"
echo "Change ID: $CHANGE_ID"
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
echo "6. Для новой задачи запускайте Codex через ./scripts/launch-codex-task.sh и новый profile launch."
