# Curator promotion flow

The curator is proposal-only by default.

Safe promotion path:

1. curator proposal
2. FT-TASK draft
3. review
4. handoff
5. implementation
6. validator
7. release note

Rules:
- do not auto-apply curator output;
- no hidden self-learning;
- all learning is repo-reviewed;
- the FT-TASK draft starts with `handoff_allowed: false`;
- implementation begins only after review makes the task explicit.

Command:

```bash
python3 template-repo/scripts/curator-proposal-to-task.py --proposal reports/curator/<file>.md --output /tmp/curator-task.yaml --write
```
