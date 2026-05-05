# Доказательство parallel worktree runner

Дата: 2026-05-05

Controlled proof was executed in a temporary repo copy, not in the live worktree.

Commands/evidence:

- `automation-approval.py create --scope parallel-runner --target task/FT-TASK-9001 --write` -> approval artifact created in temp copy.
- `bounded-task-runner.py --source task --task-id FT-TASK-9001 --max-concurrency 2 --allow-parallel --approval-file ... --no-push --no-pr` -> `bounded_runner_status=parallel_dry_run_planned`.
- same parallel command without approval -> refused with `missing explicit approval artifact`.
- `worktree_manager.py --source issue --issue 901 --create` -> dry-run plan for `.worktrees/codex/issue-901`, branch `codex/issue-901`, lock and run state.
- `worktree_manager.py --source task --task-id FT-TASK-9001 --create` -> dry-run plan for `.worktrees/codex/task-FT-TASK-9001`, branch `codex/task-FT-TASK-9001`, lock and run state.

Proof outcome:

- separate worktree paths are planned;
- separate branches are planned;
- lock paths and `run.yaml` paths are explicit;
- audit ledger append is part of bounded runner dry-run;
- cleanup policy is documented and validated;
- no shared dirty state in live repo;
- no live GitHub mutation.
