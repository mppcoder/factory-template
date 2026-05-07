# Рабочий проект

Этот шаблон создается launcher'ом и становится вашей рабочей папкой проекта.

## Что обязательно заполнять в первую очередь
- `.chatgpt/intake.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/task-index.yaml`
- `.chatgpt/task-state.yaml`
- `.chatgpt/project-lifecycle-dashboard.yaml`
- `PROJECT_BRIEF.md`
- `CURRENT_FUNCTIONAL_STATE.md`

Для ChatGPT Project используйте repo-first инструкцию: её нужно внести в поле `Instructions`, а сценарии должны читаться из GitHub repo проекта через GitHub connector / repo tool / authenticated `gh`, а не храниться внутри самого проекта как source of truth.
Public `github.com` / raw URL fallback допустим только при named blocker: connector unavailable, no permission, repo not installed in connector, authenticated repo tool unavailable или explicit user request for public URL.

Для Codex используйте named profiles `quick / build / deep / review`.
Здесь важно различать advisory layer (инструкции и сценарии) и executable routing layer (named profiles + launcher).
Не ожидайте, что один static profile в `.codex/config.toml` будет сам переключаться по типу задачи внутри старой сессии.
Для интерактивной работы в VS Code Codex extension основной путь `manual-ui (default)`: откройте новый чат/окно Codex, вручную выберите model/reasoning в picker и только потом вставьте handoff.
Launcher-команда `./scripts/launch-codex-task.sh` для нового task launch остается optional strict mode для automation, reproducibility и shell-first запуска.
Не считайте уже открытую live session надежным auto-switch механизмом. Новый чат + вставка handoff и executable launch path — не одно и то же.

Model availability auto-check хранится в `codex-model-routing.yaml` и выполняется командой `./scripts/check-codex-model-catalog.py .`, если доступен `codex debug models`.
Repo-configured mapping, live Codex catalog, manual UI picker selection и strict launcher profile selection — разные контуры.
Если новый model ID появился в live catalog, сначала создайте proposal через `--write-proposal`; существующие profiles не продвигаются автоматически без ручного review.

## Панель жизненного цикла проекта

`.chatgpt/project-lifecycle-dashboard.yaml` — единый lightweight state artifact, который связывает идею, текущую доработку, stage gates, multi-step execution, handoff/orchestration, release readiness, deploy/runtime state и post-release improvement queue.

Он не заменяет task/stage files, orchestration cockpit или operator dashboard. Он агрегирует их в один beginner-readable Markdown/CLI readout:

```bash
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
python3 scripts/render-project-lifecycle-dashboard.py --output reports/project-lifecycle-dashboard.md
```

Completed/passed gates требуют evidence или accepted reason. Advisory route text не переключает model/profile/reasoning внутри уже открытой Codex-сессии.
