# Full advanced automation gates / ворота полной автоматизации

Full automation is not enabled in generated projects.

Allowed now: dry-run issue dispatch, gated issue-autofix, PR creation, human review and task queue/runner one-task mode.

Prohibited now: auto-merge default, production deploy, secrets, security issue autofix, public external report auto-submit, unbounded parallel agents and pull_request_target.

Future unlock conditions: sandboxed runner, worktree isolation, permission model, audit log, rollback, required human review policy and cost/rate guard where applicable.

Emergency stop: add label `agent:blocked`, disable workflow, remove `agent:ready`, or run runner `--dry-run`.

Supporting hardening docs: `docs/operator/issue-autofix-permission-model.md`, `docs/operator/worktree-isolation-policy.md`, `docs/operator/worktree-manager.md`, `docs/operator/automation-audit-log.md`, `docs/operator/automation-rollback.md`, `docs/operator/required-human-review-policy.md`, `docs/operator/automation-approval.md`, `docs/operator/auto-merge-gate.md`, `docs/operator/production-deploy-gate.md`, `docs/operator/security-issue-gate.md`, `docs/operator/public-submit-gate.md` and `docs/operator/curator-promotion-flow.md`.
