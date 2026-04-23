# Отчет о дефекте

## Идентификатор
bug-018-vscode-codex-manual-ui-default-gap

## Краткий заголовок
Handoff/completion layer выдавал launcher-first path как обязательный default даже для интерактивного VS Code Codex extension workflow, из-за чего шаблон перегружал пользователя лишним terminal step и путал manual UI apply со strict executable launch.

## Тип дефекта
reusable-process-defect

## Где найдено
Repo: `factory-template`, source-facing routing / handoff / completion layer:

- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/12-bug-analysis.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/codex-routing.yaml`
- `template-repo/scripts/bootstrap-codex-task.py`
- `template-repo/scripts/launch-codex-task.sh`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `template-repo/scripts/validate-handoff-response-format.py`
- `template-repo/scripts/validate-codex-routing.py`
- `template-repo/template/docs/codex-workflow.md`
- `template-repo/template/docs/integrations.md`
- `template-repo/template/README.md`

## Шаги воспроизведения
1. Подготовить handoff для задачи, которая исполняется через VS Code Codex extension.
2. Открыть generated/source-facing handoff guidance.
3. Увидеть, что canonical default path для пользователя подается как launcher-first: выполнить terminal command, затем вставить handoff.
4. Сравнить это с реальным interactive workflow, где пользователь обычно уже находится в окне extension и может вручную выбрать model/reasoning в picker.

## Ожидаемое поведение
- Для VS Code Codex extension default user-facing path должен быть `manual-ui (default)`.
- Handoff package должен прямо объяснять: открыть новый чат/окно Codex, вручную выбрать `selected_model` и `selected_reasoning_effort` в picker, затем вставить handoff.
- Launcher-first path должен оставаться доступным как optional strict mode для automation, reproducibility, shell-first и scripted launch.
- Должно быть явно сказано, что `новый чат + вставка handoff` и `new task launch через executable launcher` — не одно и то же.
- Уже открытая live session не должна подаваться как надежный auto-switch mechanism.

## Фактическое поведение
- Source-facing guidance и generated handoff/completion artifacts подавали launcher-first path как default.
- Пользователю для обычной interactive работы приходилось идти в терминал, хотя реальный UX VS Code Codex extension чаще начинается с ручного выбора model/reasoning в UI.
- Шаблон корректно различал advisory и executable routing на policy level, но user-facing слой не давал удобного manual-ui default.
- Из-за этого дефект выглядел как "неправильный шаг пользователя", хотя корневая проблема была в template UX contract.

## Evidence
- [PROJECT] До исправления `.chatgpt/handoff-response.md` начинался с обязательного `## Launch в Codex` и instruct-ил сначала выполнить launcher command.
- [PROJECT] До исправления `.chatgpt/boundary-actions.md` содержал формулировку `Перед передачей handoff сначала выполните явный launch command`, без manual-ui default path.
- [PROJECT] До исправления `template-repo/template/docs/codex-workflow.md`, `template-repo/template/docs/integrations.md` и `template-repo/template/README.md` учили launcher-first flow как основной.
- [PROJECT] Router contract уже предупреждал, что advisory layer не auto-switches live session, но не разводил достаточно явно interactive UI-first и strict executable launch.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Текущий route остается совместимым с `selected_profile=deep`, `selected_model=gpt-5.4`, `selected_reasoning_effort=high`; меняется не executable router logic как таковая, а default user-facing apply path и completion contract.

## Временный обход
До исправления пользователь мог вручную игнорировать launcher-first совет, открыть новый чат/окно Codex и сам выставить picker. Но шаблонный default при этом оставался misleading.

## Решение / статус
fixed
