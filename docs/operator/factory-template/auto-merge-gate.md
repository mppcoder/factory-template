# Auto-merge gate

Auto-merge is default disabled.

It requires:

- approval scope `auto-merge`;
- PR from automation branch;
- checks green;
- no security labels;
- no `external-secret`;
- no unresolved human-review;
- no merge conflicts;
- branch protection compatible;
- rollback plan available;
- audit ledger entry.

Real merge is allowed only with explicit `--write --approval-id` after policy validation. Verification runs only dry-run fixtures and performs no real merge. Production deploy and security fixes require separate scopes and are never merged by this gate alone.
