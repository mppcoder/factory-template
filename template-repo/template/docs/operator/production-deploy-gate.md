# Ворота production deploy

Production deploy is default disabled.

Requires approval scope `production-deploy`, explicit target, environment approval, safe secrets environment rather than issue body, rollback plan, health check plan, audit ledger and separate `security-fix` approval if the deploy is for a security issue.

The gate supports dry-run plans and must never print secrets.
