# Smoke promotion flow куратора

Дата: 2026-05-05

Path:

curator proposal -> FT-TASK draft -> review -> handoff -> implementation -> validator -> release note.

Smoke fixture:
- `tests/factory-curator/proposal.md`

Commands:

```bash
python3 template-repo/scripts/curator-proposal-to-task.py --proposal tests/factory-curator/proposal.md --output /tmp/curator-task.yaml --write
python3 template-repo/scripts/validate-curator-promotion-flow.py .
```

Outcome: curator output can become a draft task only with explicit write; it is not auto-applied and no hidden self-learning is allowed.
