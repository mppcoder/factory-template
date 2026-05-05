# Журнал automation runs

`ledger.jsonl` is an append-only local audit log for issue/task automation runs.

Required fields:
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

Policy:
- append-only; do not rewrite previous entries;
- no secrets, tokens, private keys or `.env` values;
- issue text is recorded only as sanitized metadata, not as executable shell;
- dry-run and real runs use the same schema where safe.
