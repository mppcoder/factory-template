# Карта архитектуры как есть: OpenClaw+

Дата: 2026-04-26

## Архитектурная модель по факту

Система разделена на два корня:

1. `/root/.openclaw`
   - live runtime
   - фактическая конфигурация OpenClaw
   - runtime DB/cache/log/state
   - credentials/device/telegram state

2. `/root/openclaw-plus`
   - package / overlay
   - docs/runbooks
   - validators
   - systemd unit templates
   - retrieval app
   - telemetry scripts
   - wrapper/plugin layer
   - policies/models/routing/templates

## Runtime-сервисы

Активные и enabled сервисы:
- `openclaw-gateway`
- `openclaw-retrieval`
- `openclaw-vectorizer`
- `gpt2giga`
- `postgresql`
- `nginx`

Systemd units из package layer:
- gateway запускается через `openclaw gateway run`
- retrieval API запускается из `/root/openclaw-plus/.venvs/retrieval`
- vectorizer watcher запускается как `python -m retrieval.app.watch`
- gpt2giga sidecar запускается через `/root/openclaw-plus/sidecars/gpt2giga/run.sh`

## Данные и состояние

Runtime state:
- SQLite registry: `/root/.openclaw/flows/registry.sqlite`
- SQLite task runs: `/root/.openclaw/tasks/runs.sqlite`
- SQLite memory: `/root/.openclaw/memory/makar.sqlite`
- Telegram state: `/root/.openclaw/telegram/`
- Device identity: `/root/.openclaw/identity/`
- Credentials: `/root/.openclaw/credentials/`

External service state:
- `/etc/openclaw-plus.env` содержит integration secrets и runtime env.
- PostgreSQL используется для retrieval/pgvector по package docs.

## Слой policy и routing

Runtime:
- `/root/.openclaw/policies/`
- `/root/.openclaw/routing/task-classifier.yaml`
- `/root/.openclaw/prompts/`

Package:
- `/root/openclaw-plus/models/*.yaml`
- `/root/openclaw-plus/policies/*.yaml`
- `/root/openclaw-plus/routing/*.yaml`
- `/root/openclaw-plus/prompts/*.system.md`
- `/root/openclaw-plus/facade/*.yaml`

## Инварианты из package docs

Из `/root/openclaw-plus/ARCHITECTURE.md`:
- live runtime exists only in `~/.openclaw`
- package tree is overlay only
- no duplicate runtime under `/root/openclaw-plus`
- flat layout is canonical source-of-truth
- destructive actions require confirmation
- private chat and `MAIN` route to `makar`
- topic-local responders: `arkasha`, `sonya`, `yana`, `goga`
- token economy uses PostgreSQL + pgvector, MiniLM embeddings, retrieval-first

## Проверенная работоспособность

`validators/run-final-acceptance.sh` прошел успешно, но live validator выдал warning:
- duplicated content detected / context bloat

Этот warning должен быть занесен в gap register до remediation planning.
