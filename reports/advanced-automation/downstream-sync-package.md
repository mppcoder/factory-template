# Пакет downstream sync

Дата: 2026-05-05

## Кандидаты copy/update

Safe overwrite:
- generated operator docs under `docs/operator/` for bounded runner, curator, gates, permission model, worktree isolation, rollback and promotion flow;
- `WORKFLOW.md` when downstream has no local workflow customizations.

Merge required:
- `.chatgpt/task-registry.yaml`;
- existing issue templates;
- `SECURITY.md`;
- existing workflows;
- local project docs and release notes.

## Проверка в downstream

```bash
python3 scripts/validate-task-registry.py
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```

This is a future/operator action only if real downstream sync is desired. It is not required for the current factory repo closeout.
