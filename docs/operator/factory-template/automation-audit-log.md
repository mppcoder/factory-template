# Automation audit log

Automation runs write an append-only JSONL ledger at `.chatgpt/automation-runs/ledger.jsonl`.

Required schema fields:

- `run_id`
- `parent_run_id`
- `issue_or_task_id`
- `actor`
- `trigger`
- `permission_decision`
- `approvals`
- `worktree`
- `branch`
- `commands`
- `launcher_command`
- `handoff_path`
- `verification`
- `pr_url`
- `deploy_status`
- `public_submit_status`
- `rollback_plan`
- `blockers`
- `final_status`
- `timestamp_utc`

Rules:

- append-only;
- no secrets;
- no raw `.env` values;
- no raw issue body by default; store sanitized hash/summary where needed;
- no untrusted issue text as executable command;
- dry-run and real runs use the same ledger shape;
- optional hash chain fields `previous_entry_hash` and `current_entry_hash` make local tampering visible enough for repo use.

Validation:

```bash
python3 template-repo/scripts/automation_run_ledger.py --ledger .chatgpt/automation-runs/ledger.jsonl validate
python3 template-repo/scripts/validate-automation-run-ledger.py .
```
