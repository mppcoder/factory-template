# Advanced automation downstream sync

This package tells an existing downstream/battle repo how to receive the advanced automation layer.

## Safe overwrite

- `docs/operator/bounded-runner.md`
- `docs/operator/factory-curator.md`
- `docs/operator/full-advanced-automation-gates.md`
- `docs/operator/issue-autofix-permission-model.md`
- `docs/operator/worktree-isolation-policy.md`
- `docs/operator/automation-rollback.md`
- `docs/operator/curator-promotion-flow.md`
- `WORKFLOW.md`

## Merge required

- `.chatgpt/task-registry.yaml`: never blindly overwrite user tasks or evidence;
- existing issue templates;
- `SECURITY.md`;
- existing workflows;
- local project docs and release notes.

## Verification in generated repo

```bash
python3 scripts/validate-task-registry.py
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```

No downstream sync is required for the current factory repo closeout.
