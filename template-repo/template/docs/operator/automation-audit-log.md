# Журнал audit log automation

Automation runs write an append-only JSONL ledger at `.chatgpt/automation-runs/ledger.jsonl`.

Required schema fields: `run_id`, `parent_run_id`, `issue_or_task_id`, `actor`, `trigger`, `permission_decision`, `approvals`, `worktree`, `branch`, `commands`, `launcher_command`, `handoff_path`, `verification`, `pr_url`, `deploy_status`, `public_submit_status`, `rollback_plan`, `blockers`, `final_status`, `timestamp_utc`.

Rules: append-only, no secrets, no raw `.env` values, no raw issue body by default, no untrusted issue text as executable command, optional hash chain with `previous_entry_hash` and `current_entry_hash`.
