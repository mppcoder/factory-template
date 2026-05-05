# Production deploy gate

Production deploy is default disabled.

It requires:

- approval scope `production-deploy`;
- deploy target explicitly configured;
- environment approval if GitHub environments are used;
- secrets available through safe environment, not issue body;
- rollback plan;
- health check plan;
- audit ledger;
- no security issue unless `security-fix` scope is also approved.

The gate supports dry-run deployment plans. It must never print secrets and never performs actual deploy during verification.
