# Automation audit log

Automation runs write an append-only ledger at `.chatgpt/automation-runs/ledger.jsonl` where safe.

Schema fields:
- `issue_or_task_id`
- `trigger`
- `actor`
- `gate_result`
- `handoff_path`
- `branch`
- `launcher_command`
- `verification_commands_results`
- `pr_url`
- `blockers`
- `final_status`
- `timestamp_utc`

Rules:
- append-only;
- no secrets;
- no raw `.env` values;
- no untrusted issue text as executable command;
- dry-run and real runs should use the same ledger shape.
