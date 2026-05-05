# Bounded runner / ограниченный runner

`template-repo/scripts/bounded-task-runner.py` is the safe skeleton for one-task execution.

## Current capability / текущая возможность

- default dry-run;
- default `--max-concurrency 1`;
- supports GitHub issue (`--issue`), FT-TASK (`--task-id`) and existing handoff (`--handoff`);
- writes run state under `.chatgpt/issue-runs/issue-<N>/run.yaml` or `.chatgpt/task-runs/<TASK-ID>/run.yaml`;
- records exact `launcher_command`;
- supports `--dry-run`, `--one`, `--max-concurrency`, `--no-push`, `--no-pr`;
- appends audit state to `.chatgpt/automation-runs/ledger.jsonl` where safe.

## Refusals / отказы

- no auto-merge;
- no production deploy;
- no public report publication;
- no security/external-secret/blocked tasks;
- `--max-concurrency` above `1` is refused unless future worktree isolation is implemented and tested;
- parallel execution is refused without worktree isolation.

Related policies:
- `docs/operator/factory-template/worktree-isolation-policy.md`;
- `docs/operator/factory-template/automation-audit-log.md`;
- `docs/operator/factory-template/automation-rollback.md`.

This runner is a bounded substrate, not a daemon.
