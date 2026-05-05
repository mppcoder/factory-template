# Bounded runner / ограниченный runner

`template-repo/scripts/bounded-task-runner.py` is the safe substrate for one-task execution and approved parallel dry-run planning.

## Current capability / текущая возможность

- default dry-run;
- default `--max-concurrency 1`;
- supports `--source issue`, `--source task`, `--queue`, GitHub issue (`--issue`), FT-TASK (`--task-id`) and existing handoff (`--handoff`);
- writes run state under `.chatgpt/issue-runs/issue-<N>/run.yaml` or `.chatgpt/task-runs/<TASK-ID>/run.yaml`;
- records exact `launcher_command`;
- supports `--dry-run`, `--write`, `--one`, `--max-concurrency`, `--allow-parallel`, `--no-push`, `--no-pr`;
- appends audit state to `.chatgpt/automation-runs/ledger.jsonl` where safe.

## Refusals / отказы

- no auto-merge;
- no production deploy;
- no public report publication;
- no security/external-secret/blocked tasks;
- `--max-concurrency` above `1` requires `--allow-parallel`, approval scope `parallel-runner`, worktree manager validator, audit ledger and rollback plan;
- parallel tasks must use separate worktrees;
- refused task markers: `security`, `external-secret`, `needs-human`, `blocked`, high risk without approval and missing acceptance criteria;
- records claim, exact command, worktree path, branch, commit hash, PR plan/URL, verification result and rollback_plan.

Related policies:
- `docs/operator/factory-template/worktree-isolation-policy.md`;
- `docs/operator/factory-template/automation-audit-log.md`;
- `docs/operator/factory-template/automation-rollback.md`.

This runner is a bounded substrate, not a daemon.
