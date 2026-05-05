# Full advanced automation gates / ворота полной автоматизации

Full automation is not enabled. This document defines the gates and refusal boundaries.

## Allowed now / разрешено сейчас

- dry-run issue dispatch;
- gated issue-autofix;
- PR creation;
- human review;
- task queue/runner one-task mode.

## Prohibited now / запрещено сейчас

- auto-merge default;
- production deploy;
- secrets;
- security issue autofix;
- public external report auto-submit;
- unbounded parallel agents;
- pull_request_target.

## Future unlock conditions / условия будущего открытия

- sandboxed runner;
- worktree isolation;
- permission model;
- audit log;
- rollback;
- required human review policy;
- cost/rate guard where applicable.

## Emergency stop / аварийная остановка

- add label `agent:blocked`;
- disable workflow;
- remove `agent:ready`;
- run runner `--dry-run`.
