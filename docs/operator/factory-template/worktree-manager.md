# Worktree manager

`template-repo/scripts/worktree_manager.py` is the dry-run-first worktree isolation substrate for future bounded parallel execution.

Conventions:

- issue worktree path: `.worktrees/codex/issue-<N>`;
- task worktree path: `.worktrees/codex/task-<ID>`;
- issue branch: `codex/issue-<N>`;
- task branch: `codex/task-<ID>`;
- lock path: `.chatgpt/automation-runs/locks/<id>.lock`;
- issue run state: `.chatgpt/issue-runs/issue-<N>/run.yaml`;
- task run state: `.chatgpt/task-runs/<TASK-ID>/run.yaml`.

Safety:

- default mode is dry-run;
- mutation requires `--write`;
- no secrets copied into worktree;
- no `.env` capture;
- no main rewrite;
- stale lock refuses create unless an explicit cleanup command is used.

Cleanup policy:

- dry-run cleanup prints the cleanup plan;
- completed cleanup may remove the completed worktree with `--write`;
- failed runs are preserved for inspection;
- stale locks are not removed silently.
