# Рабочий проект

Этот шаблон создается launcher'ом и становится вашей рабочей папкой проекта.

## Что обязательно заполнять в первую очередь
- `.chatgpt/intake.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/task-index.yaml`
- `PROJECT_BRIEF.md`
- `CURRENT_FUNCTIONAL_STATE.md`

Для ChatGPT Project используйте repo-first инструкцию: её нужно внести в поле `Instructions`, а сценарии должны читаться из GitHub repo проекта, а не храниться внутри самого проекта как source of truth.

Для Codex используйте named profiles `quick / build / deep / review` через task launcher.
Не ожидайте, что один static profile в `.codex/config.toml` будет сам переключаться по типу задачи внутри старой сессии.
Если handoff уже готов, сначала выполняйте launcher-команду нового task launch, а не просто вставляйте handoff в случайный старый чат.
