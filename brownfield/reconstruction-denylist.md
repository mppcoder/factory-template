# Denylist реконструкции: OpenClaw+

Дата: 2026-04-26

## Абсолютный denylist

```text
/etc/openclaw-plus.env
/root/.openclaw/credentials/**
/root/.openclaw/identity/**
/root/.openclaw/devices/**
/root/.openclaw/telegram/**
/root/.openclaw/media/**
/root/.openclaw/cache/**
/root/.openclaw/delivery-queue/**
/root/.openclaw/flows/*.sqlite*
/root/.openclaw/memory/*.sqlite*
/root/.openclaw/tasks/*.sqlite*
/root/.openclaw/**/*.jsonl
/root/openclaw-plus/.venvs/**
/root/openclaw-plus/**/node_modules/**
/root/openclaw-plus/**/__pycache__/**
/root/openclaw-plus/**/*.pyc
/root/openclaw-plus/var/**
/root/openclaw-plus/sidecars/gpt2giga/logs/**
/root/openclaw-plus/**/*.log
```

## Условный denylist

Не включать в active source без отдельного triage:

```text
*.bak
*.bak.*
*.old
*.orig
*.deleted.*
*.disabled.*
```

## Причина

- secret leakage risk;
- runtime state drift;
- generated dependency noise;
- oversized reconstructed repo;
- невозможность отличить active source от historical backup без triage.
