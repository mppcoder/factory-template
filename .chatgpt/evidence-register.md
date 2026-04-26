# Реестр доказательств

- [PROJECT] В каталоге `template-repo/scenario-pack` подтверждено наличие сценарного слоя и файлов маршрутизации.
- [DOC] В `bootstrap/04-как-работает-stage-pipeline.md` зафиксировано требование закрывать этапные шлюзы до handoff.
- [REAL] Живой smoke-test подтвердил, что launcher создает проект, копирует скрипты и заполняет стартовые YAML-файлы.
- [BROWNFIELD] `template-repo/scenario-pack/00-master-router.md` прочитан перед стартом задачи; маршрут перевел задачу в direct-task self-handoff + brownfield entry.
- [BROWNFIELD] `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`, `01-system-inventory.md`, `02-repo-audit.md`, `03-as-is-architecture-map.md` прочитаны перед инвентаризацией.
- [ROUTING] `template-repo/scripts/bootstrap-codex-task.py` создал `.chatgpt/task-launch.yaml`, `.chatgpt/direct-task-source.md`, `.chatgpt/direct-task-self-handoff.md`, `.chatgpt/normalized-codex-handoff.md` для текущего direct task.
- [REAL] `/root/.openclaw` существует, является directory `drwx------ root:root`, размер `16M`, git repo отсутствует.
- [REAL] `/root/openclaw-plus` существует, является directory `drwxr-xr-x root:root`, размер `7.3G`, git repo отсутствует.
- [REAL] `systemctl is-active/is-enabled` подтвердил active+enabled для `openclaw-gateway`, `openclaw-retrieval`, `openclaw-vectorizer`, `gpt2giga`, `postgresql`, `nginx`.
- [REAL] `/etc/openclaw-plus.env` существует с mode `-rw-------`; значения секретов не выводились, ключи зафиксированы redacted.
- [VERIFY] `bash validators/run-final-acceptance.sh` из `/root/openclaw-plus` завершился `[OK] acceptance checks passed`; одновременно зафиксирован `[WARN] duplicated content detected (context bloat)`.
- [BUG] Пользовательский follow-up 2026-04-26 подтвердил reusable defect: closeout остановился перед internal `source-candidate-map` и не выдал `## Инструкция пользователю`.
- [FIX] `template-repo/scripts/codex_task_router.py` обновлен: generated direct-task response теперь содержит publishable handoff sections, continuation rule и closeout instruction rule.
- [FIX] `template-repo/scripts/validate-codex-routing.py` обновлен: direct-task response невалиден без continuation guardrail и `## Инструкция пользователю`/`Внешних действий не требуется.` guardrails.
- [REAL] Source-candidate scan подтвердил generated/dependency denylist zones: `/root/openclaw-plus/.venvs`, `node_modules`, `__pycache__`, `/root/openclaw-plus/var`.
