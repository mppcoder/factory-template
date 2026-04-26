# Allowlist реконструкции: OpenClaw+

Дата: 2026-04-26

## Разрешенный набор package root

Base: `/root/openclaw-plus`

```text
.env.example
.env.example.patch
ARCHITECTURE.md
KNOWN-BUGS.md
MEMORY-TOKEN-CONTROL.md
README.md
RUNBOOK-FULL.md
RUNBOOK-RETRIEVAL-BLOCK.md
RUNBOOK-TOOLS-BLOCK.md
VERSIONS_SNAPSHOT.txt
accounts/**/*.yaml
docs/**/*.md
env/*.append
facade/**/*.py
facade/**/*.yaml
facade/**/*.sh
hooks/**/*.py
hooks/**/*.md
infra/**/*.conf
infra/**/*.md
infra/**/*.service
infra/**/*.sh
infra/**/*.sql
infra/**/*.txt
memory/**/*.yaml
models/**/*.yaml
policies/**/*.yaml
prompts/**/*.md
requirements-*.txt
retrieval/**/*.py
routing/**/*.yaml
scripts/**/*.py
scripts/**/*.sh
sidecars/gpt2giga/config.yaml
sidecars/gpt2giga/healthcheck.sh
sidecars/gpt2giga/run.sh
sidecars/gpt2giga/security.md
skills/**/*.md
snippets/**/*
telemetry/**/*.py
templates/**/*
tools/**/*.py
tools/**/*.yaml
validators/**/*.md
validators/**/*.sh
wrappers/delegate-specialist-plugin/index.js
wrappers/delegate-specialist-plugin/openclaw.plugin.json
wrappers/delegate-specialist-plugin/package.json
wrappers/delegate-specialist-plugin/package-lock.json
wrappers/docs/**/*
wrappers/scripts/**/*.py
wrappers/snippets/**/*
wrappers/tools/**/*
wrappers/validators/**/*.sh
```

## Ограниченный allowlist runtime root

Base: `/root/.openclaw`

Только после redaction/review:

```text
openclaw.json
canvas/index.html
agents/*/agent/models.json
hooks/**/*.py
policies/**/*.yaml
prompts/**/*.md
routing/**/*.yaml
```

## Разрешенный набор inventory env

Base: `/etc/openclaw-plus.env`

Разрешено переносить только:
- список имен переменных;
- категорию переменной;
- факт наличия;
- redacted placeholder.

Значения не переносить.
