# Public submit gate

Public external report submission is default disabled.

It requires:

- approval scope `public-submit`;
- redaction validator green;
- consent artifact;
- no secrets;
- no private URLs;
- no raw logs unless explicitly allowed and sanitized;
- target repo configured;
- audit ledger entry;
- rollback/update plan if submission is wrong.

External user reports never auto-submit without consent. Dry-run creates a public issue body preview only; real submit requires explicit write approval and is outside verification.
