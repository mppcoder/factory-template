# chg-20260426-handoff-codex-language-contract

## Статус

completed

## Дата

2026-04-26

## Defect capture

- `reports/bugs/2026-04-26-handoff-codex-language-leak.md`

## Что исправлено

- Generated Codex handoff теперь явно содержит `Язык ответа Codex: русский`.
- Copy-paste handoff больше не использует англоязычные labels `Repo:`, `Goal:`, `Entry point:`, `Scope:`.
- `validate-handoff-response-format.py` и `validate-handoff-language.py` блокируют регрессию.
- `validate-codex-task-pack.py` требует language contract в task pack, boundary actions и handoff response.
- Matrix добавляет negative-case `reject-english-handoff-labels`.

## Проверка

- `python3 template-repo/scripts/validate-handoff-response-format.py .chatgpt/handoff-response.md` — pass.
- `python3 template-repo/scripts/validate-handoff-language.py .chatgpt/handoff-response.md` — pass.
- `python3 template-repo/scripts/validate-codex-task-pack.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash MATRIX_TEST.sh` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
