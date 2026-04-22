# Отчет о дефекте

## Идентификатор
bug-015-explicit-handoff-reasoning-overridden-by-keyword-routing

## Краткий заголовок
Executable router игнорировал explicit `selected_reasoning_effort` из structured handoff и пересчитывал route по keyword fallback, из-за чего `high` деградировал в `medium`.

## Где найдено
Repo: `factory-template`, routing / handoff artifact layer:

- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/bootstrap-codex-task.py`
- `template-repo/scripts/resolve-codex-task-route.py`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/normalized-codex-handoff.md`

## Шаги воспроизведения
1. Передать router'у structured handoff с явными полями:
   - `selected_model: GPT-5.4 Thinking`
   - `selected_reasoning_effort: high`
   - `selected_profile: repo-maintenance`
2. Запустить `python3 template-repo/scripts/resolve-codex-task-route.py . --launch-source chatgpt-handoff --task-text '<handoff>'`.
3. Наблюдать, что до исправления router смотрел только на keyword hits в тексте.
4. Проверить generated artifacts и увидеть `selected_reasoning_effort=medium`, хотя source handoff явно требовал `high`.

## Ожидаемое поведение
- Если handoff уже содержит explicit routing fields, router должен уважать их как входные данные для нового task launch.
- Если `selected_profile` из handoff не исполним напрямую, router должен выбрать совместимый executable profile по model/reasoning, а не silently откатываться к keyword fallback.
- Generated `.chatgpt/task-launch.yaml` и normalized handoff не должны терять explicit high-reasoning intent.

## Фактическое поведение
- `build_launch_record()` заново инферил `task_class/profile` только по keyword match.
- Explicit `selected_reasoning_effort: high` и `selected_model` из handoff игнорировались.
- В результате artifacts фиксировали `selected_profile=build`, `selected_reasoning_effort=medium`, хотя source handoff требовал high reasoning.

## Evidence
- [PROJECT] До исправления:
  - `python3 template-repo/scripts/resolve-codex-task-route.py . --launch-source chatgpt-handoff --task-text '<structured handoff>'`
  - выводил `selected_profile=build`
  - выводил `selected_reasoning_effort=medium`
- [PROJECT] Source handoff при этом содержал:
  - `selected_profile: repo-maintenance`
  - `selected_model: GPT-5.4 Thinking`
  - `selected_reasoning_effort: high`
- [PROJECT] После исправления тот же reproduce path выводит:
  - `selected_profile=deep`
  - `selected_reasoning_effort=high`
  - `launch_command=codex --profile deep`

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, потому что это reusable routing defect в source-of-truth repo: explicit handoff metadata терялась при bootstrap нового task launch.

## Статус
зафиксировано
