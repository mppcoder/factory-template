# Worktree manager / менеджер worktree

Dry-run-first isolation substrate for future bounded parallel execution.

- issue worktree path: `.worktrees/codex/issue-<N>`;
- task worktree path: `.worktrees/codex/task-<ID>`;
- branch: `codex/issue-<N>` or `codex/task-<ID>`;
- lock path: `.chatgpt/automation-runs/locks/<id>.lock`;
- issue run state: `.chatgpt/issue-runs/issue-<N>/run.yaml`;
- task run state: `.chatgpt/task-runs/<TASK-ID>/run.yaml`;
- default mode is dry-run;
- mutation requires `--write`;
- no secrets copied into worktree;
- no `.env` capture;
- no main rewrite;
- stale lock refuses create unless explicit cleanup command is used.
