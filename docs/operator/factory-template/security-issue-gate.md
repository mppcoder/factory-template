# Security issue gate

Public security issue autofix refused.

Security work requires:

- private report channel;
- approval scope `security-fix`;
- maintainer/admin actor;
- no public logs;
- no public issue body in handoff;
- sanitized private handoff;
- audit ledger with no sensitive details;
- human review required;
- no auto-merge unless separate auto-merge approval and policy allows.

If the private channel cannot be implemented safely, the automation stops at docs, refusal validator and private placeholder. Public security autofix is not implemented.
