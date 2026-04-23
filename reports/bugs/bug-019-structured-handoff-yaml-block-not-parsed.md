# Отчет о дефекте

## Идентификатор
bug-019-structured-handoff-yaml-block-not-parsed

## Краткий заголовок
Structured handoff parser не читал YAML routing block, если тот шел после markdown heading, из-за чего explicit overrides для `artifacts_to_update`, `handoff_allowed` и других полей silently терялись при bootstrap нового Codex task.

## Тип дефекта
incidental-side-bug

## Где найдено
Repo: `factory-template`, executable routing / bootstrap layer:

- `template-repo/scripts/codex_task_router.py`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/normalized-codex-handoff.md`

## Шаги воспроизведения
1. Подготовить structured handoff, в котором YAML routing block идет после markdown heading, например `# Входной пакет для Codex`.
2. Передать этот текст в `template-repo/scripts/bootstrap-codex-task.py` или `template-repo/scripts/resolve-codex-task-route.py`.
3. Проверить generated `.chatgpt/task-launch.yaml`.
4. Увидеть, что до исправления parser не вытаскивал часть explicit overrides из YAML block и откатывался к fallback metadata.

## Ожидаемое поведение
- Router должен уметь читать structured YAML block даже если перед ним есть markdown heading.
- Explicit handoff fields должны сохраняться в launch record без silent downgrade к fallback metadata.

## Фактическое поведение
- `parse_structured_handoff()` сначала пытался распарсить весь markdown как YAML, затем падал в line-by-line fallback.
- При наличии heading и list-структур line-by-line fallback терял часть structured data.
- В результате launch record мог сохранить stale/fallback значения вместо explicit overrides из handoff.

## Evidence
- [PROJECT] Во время текущей remediation `.chatgpt/task-launch.yaml` сначала не подхватил полный `artifacts_to_update` из обновленного `.chatgpt/codex-input.md`.
- [PROJECT] После исправления `template-repo/scripts/codex_task_router.py` launch record корректно фиксирует полный YAML block из handoff input.
- [PROJECT] Повторный bootstrap после fix корректно заполнил `artifacts_to_update`, `handoff_allowed` и другие explicit routing fields.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Route не требовал смены profile/model/reasoning; defect исправлялся в текущем `deep` scope как incidental parser fix внутри того же routing слоя.

## Временный обход
До исправления можно было писать чистый YAML без markdown heading, но это ломало нормальный user-facing handoff format и не было приемлемым canonical workaround.

## Решение / статус
fixed
