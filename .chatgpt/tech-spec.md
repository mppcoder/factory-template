# Техническая спецификация

## Архитектура
- Verified sync и release executor остаются двумя независимыми скриптами.
- Оба контура используют общий helper layer в `template-repo/scripts/factory_automation_common.py`.
- Runtime lock-файлы и отчеты живут в `.factory-runtime/`, который исключен из git и release bundle.

## Verified Sync
- Для полного change path сохранить текущую проверку `verification_complete` и `.chatgpt/task-index.yaml` / `.chatgpt/verification-report.md`.
- Для lightweight follow-up path разрешать только low-risk `.gitignore` и docs/closeout allowlist paths.
- Lightweight follow-up требовать уже существующий green verify baseline и прогон `git diff --check`.
- Для lightweight follow-up собирать отдельный commit message, а не наследовать старый task title.
- Отфильтровать runtime и verify noise через denylist.
- Выполнить `git add` -> `git commit` -> `git push` строго последовательно.
- При нестабильном `origin push` использовать fallback на прямой SSH URL.

## Release Decision
- Канонический artifact: `.chatgpt/release-decision.yaml`.
- Валидировать `decision`, `version`, `channel`, `notes_source`, `approved_by`, `timestamp`.
- Для `release` требовать успешный verified sync и clean repo.
- Для `release` создавать и pushить tag, собирать notes artifact и публиковать GitHub Release через `gh` при возможности.
- При невозможности publish записывать deterministic fallback report без silent fail.
