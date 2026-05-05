# Downstream-материализация

Дата: 2026-05-05

Downstream-facing docs added under `template-repo/template/docs/operator/`:

- `worktree-manager.md`
- `required-human-review-policy.md`
- `automation-approval.md`
- `automation-audit-log.md`
- `automation-rollback.md`
- `auto-merge-gate.md`
- `production-deploy-gate.md`
- `security-issue-gate.md`
- `public-submit-gate.md`

Template `SECURITY.md` now states that public security issue autofix is refused and security work requires a private report channel.

Smoke result:

- file existence check -> pass;
- downstream docs say dangerous actions are default disabled/refused;
- no generated project auto-enables auto-merge, production deploy, security issue autofix, public submit or unbounded parallel execution.

Scripts remain factory-side tooling; generated projects receive operator policy docs and safe boundaries.
