# Отчет о создании repo проекта OpenClaw Brownfield

Дата: 2026-04-26

## Итог

Создан локальный Git repo проекта:

```text
/projects/openclaw-brownfield
```

Первый commit:

```text
4a58c8d Initial sanitized OpenClaw brownfield repo
```

GitHub remote:

```text
https://github.com/mppcoder/openclaw-brownfield
```

Latest pushed commit:

```text
7b3d1a4 Publish OpenClaw brownfield repo and fix generated verify
```

## Что перенесено

- Factory project shell из `factory-template`.
- Sanitized source reconstruction из `/root/openclaw-plus` в `/projects/openclaw-brownfield/src/openclaw-plus`.
- Redacted env inventory из `/etc/openclaw-plus.env` в `/projects/openclaw-brownfield/runtime-evidence/openclaw-plus-env.inventory.md`.
- Runtime copy policy в `/projects/openclaw-brownfield/runtime-evidence/README.md`.
- GitHub remote `origin` на `https://github.com/mppcoder/openclaw-brownfield.git`.

## Что не перенесено

- Raw `/root/.openclaw`.
- Raw `/etc/openclaw-plus.env`.
- Credentials, identity, devices, telegram state, media, cache, sqlite, jsonl.
- `.venvs`, `venv`, `node_modules`, `__pycache__`, pyc, logs, `var`.
- Backup/deleted/disabled historical files.
- `wrappers/docs/*.txt`, потому что scan показал transcript/runtime fragments из `/root/.openclaw`.

## Проверки нового repo

- `python scripts/validate-brownfield-transition.py .`: passed.
- `python scripts/validate-evidence.py .`: passed.
- `python scripts/validate-codex-task-pack.py .`: passed.
- Denylist scan по project repo: prohibited runtime/generated paths not found.
- `bash scripts/verify-all.sh` в `/projects/openclaw-brownfield`: passed.
- `git status --short --branch`: clean on `main...origin/main`.

## Ограничение

Первичный запуск `bash scripts/verify-all.sh` в freshly generated downstream repo выявил bug root detection; он исправлен в `bug-038`, и verify теперь проходит.

## Статус FP-02

FP-02 теперь закрыт не только audit/evidence stage, но и фактическим созданием локального project repo.
