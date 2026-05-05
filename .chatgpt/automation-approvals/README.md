# Подтверждения automation

Approval artifacts live in this directory as JSON files with schema `automation-approval/v1`.

Required fields:

- `schema: automation-approval/v1`
- `approval_id`
- `action_scope`
- `actor`
- `actor_permission`
- `target`
- `expires_at`
- `single_use`
- `reason`
- `created_at`
- `consumed_at`
- `status: active/consumed/expired/revoked`
- `evidence`

Rules:

- dry-run by default;
- no approval from untrusted issue body;
- approval cannot be created for read/unknown actor;
- approval for `security-fix`, `production-deploy`, `public-submit`, `auto-merge` and `parallel-runner` must use the exact explicit scope;
- consumed and expired approvals are refused;
- approval consumption is recorded in the audit ledger.
