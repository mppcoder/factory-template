# Bounded runner / ограниченный runner

Generated project receives `scripts/bounded-task-runner.py` as a dry-run / one-task automation skeleton.

Current boundary: default max concurrency is `1`, no auto-merge, no production deploy, no public report publication, no security/external-secret/blocked tasks. The runner records `launcher_command`, appends audit state where safe and keeps run state under `.chatgpt/issue-runs/` or `.chatgpt/task-runs/`.

Parallel execution is refused without worktree isolation. `--max-concurrency` above `1` stays disabled until worktree isolation, audit log, rollback and cleanup policy are implemented and tested.
