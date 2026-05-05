# Политика worktree isolation

Current MVP:
- branch per issue/task;
- one task at a time;
- run state in `.chatgpt/issue-runs/` or `.chatgpt/task-runs/`;
- lock file convention: `.chatgpt/automation-runs/locks/<issue-or-task>.lock`;
- cleanup policy keeps run state and audit ledger entries.

Future parallel mode requires worktree per issue/task. parallel execution is refused when `--max-concurrency > 1` until worktree isolation is implemented and tested.

Never rewrite `main`.
