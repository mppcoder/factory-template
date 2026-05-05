# Rollback proof / доказательство отката

Дата: 2026-05-05

`template-repo/scripts/automation-rollback-plan.py` now generates dry-run rollback plans for:

- failed run;
- bad branch;
- bad PR;
- wrong labels;
- wrong task status;
- failed deploy;
- bad public submit;
- security false positive.

Safety proof:

- destructive cleanup requires explicit `destructive-rollback` approval;
- generated plans contain no `git push --force`;
- no force push to main;
- no history rewrite;
- ledger append is supported through `--ledger`;
- validator: `python3 template-repo/scripts/validate-automation-rollback.py .` -> pass.

No destructive action was executed.
