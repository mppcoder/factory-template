# Локальный end-to-end dry-run issue-autofix

Дата: 2026-05-05

Local path:

fixture issue -> gate -> `codex-input.md` -> `run.yaml` -> bounded runner dry-run -> branch/PR plan -> verification plan.

Command:

```bash
python3 template-repo/scripts/issue-autofix-smoke.py .
```

The smoke uses a temporary directory and does not create a real PR, mutate live GitHub labels/issues, push a branch or auto-merge.

`verify-all quick` includes this smoke.
