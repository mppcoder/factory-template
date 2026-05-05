# Проверка audit ledger

Дата: 2026-05-05

`template-repo/scripts/automation_run_ledger.py` writes append-only JSONL entries for dry-run and real runs where safe.

Covered fields:
- issue/task id;
- trigger;
- actor;
- gate result;
- handoff path;
- branch;
- launcher command;
- verification commands/results;
- PR URL;
- blockers;
- final status;
- timestamps.

Validator:

```bash
python3 template-repo/scripts/validate-automation-run-ledger.py .
```

Safety: no secrets, append-only, no untrusted issue text execution.
