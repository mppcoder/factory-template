# Рабочий проект

Этот шаблон создается launcher'ом и становится вашей рабочей папкой проекта.

## Что обязательно заполнять в первую очередь
- `.chatgpt/intake.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/task-index.yaml`
- `PROJECT_BRIEF.md`
- `CURRENT_FUNCTIONAL_STATE.md`

Для ChatGPT Project используйте repo-first инструкцию: её нужно внести в поле `Instructions`, а сценарии должны читаться из GitHub repo проекта, а не храниться внутри самого проекта как source of truth.

Для Codex используйте named profiles `quick / build / deep / review`.
Не ожидайте, что один static profile в `.codex/config.toml` будет сам переключаться по типу задачи внутри старой сессии.
Для интерактивной работы в VS Code Codex extension основной путь такой: откройте новый чат/окно Codex, вручную выберите model/reasoning в picker и только потом вставьте handoff.
Launcher-команда нового task launch остается optional strict mode для automation, reproducibility и shell-first запуска.
Не считайте уже открытую live session надежным auto-switch механизмом. Новый чат + вставка handoff и executable launch path — не одно и то же.
