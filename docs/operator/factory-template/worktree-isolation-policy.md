# Worktree isolation policy

## Current MVP

- branch per issue/task;
- one runner task at a time;
- default `--max-concurrency 1`;
- run state under `.chatgpt/issue-runs/issue-<N>/run.yaml` or `.chatgpt/task-runs/<TASK-ID>/run.yaml`;
- lock file convention: `.chatgpt/automation-runs/locks/<issue-or-task>.lock`.

## Future parallel mode

Parallel execution requires worktree per issue/task before it can be enabled. Each worktree must have:

- isolated checkout path;
- unique branch;
- lock file;
- run state;
- audit ledger entry;
- cleanup policy for failed and completed runs.

## Refusal

The bounded runner refuses `--max-concurrency > 1` until worktree isolation is implemented and tested. parallel execution is refused without that isolation.

## Cleanup policy

- remove stale lock files only after confirming no runner process owns them;
- archive run state and ledger entries;
- delete abandoned automation branches only after review;
- never rewrite `main`.
