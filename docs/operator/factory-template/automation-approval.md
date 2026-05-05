# Automation approval layer

`template-repo/scripts/automation-approval.py` creates, validates and consumes approval artifacts. It is dry-run by default and writes only with `--write`.

Approval record schema:

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

- approval cannot be created for read/unknown actor;
- approval for security/deploy/public-submit requires explicit scope;
- approval must be consumed and recorded in ledger;
- no approval from untrusted issue body;
- expired and consumed approvals are refused.

Examples:

```bash
python3 template-repo/scripts/automation-approval.py create --scope parallel-runner --target task/FT-TASK-0001 --actor maint --actor-permission maintain --reason fixture --write
python3 template-repo/scripts/automation-approval.py validate --scope parallel-runner --target task/FT-TASK-0001 --actor maint --actor-permission maintain --approval-id approval-parallel-runner-task-FT-TASK-0001
```
