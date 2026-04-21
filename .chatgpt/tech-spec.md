# Техническая спецификация

## Архитектура
- Verified sync и release executor разделяются на два независимых скрипта.
- Оба контура используют общий helper layer в `template-repo/scripts/factory_automation_common.py`.
- Runtime lock-файлы и отчеты живут в `.factory-runtime/`, который исключен из git и release bundle.

## Verified Sync
- Проверить `verification_complete` в `.chatgpt/stage-state.yaml`.
- Проверить наличие и достаточность `.chatgpt/task-index.yaml` и `.chatgpt/verification-report.md`.
- Собрать commit message из change metadata.
- Отфильтровать runtime и verify noise через denylist.
- Выполнить `git add` -> `git commit` -> `git push` строго последовательно.
- При нестабильном `origin push` использовать fallback на прямой SSH URL.

## Release Decision
- Канонический artifact: `.chatgpt/release-decision.yaml`.
- Валидировать `decision`, `version`, `channel`, `notes_source`, `approved_by`, `timestamp`.
- Для `release` требовать успешный verified sync и clean repo.
- Для `release` создавать и pushить tag, собирать notes artifact и публиковать GitHub Release через `gh` при возможности.
- При невозможности publish записывать deterministic fallback report без silent fail.
