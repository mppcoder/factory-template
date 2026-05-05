# Слой approval automation

Approval artifacts use schema `automation-approval/v1` with `approval_id`, `action_scope`, `actor`, `actor_permission`, `target`, `expires_at`, `single_use`, `reason`, `created_at`, `consumed_at`, `status: active/consumed/expired/revoked` and `evidence`.

Rules: dry-run by default, no approval from untrusted issue body, read/unknown actors are refused, security/deploy/public-submit require explicit scope, consumed and expired approvals are refused, approval consumption is recorded in the audit ledger.
