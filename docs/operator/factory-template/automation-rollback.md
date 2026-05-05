# Automation rollback

Rollback is a dry-run-first recovery policy for branches, PRs, labels, task state, deploys, public submits and security false positives. It never rewrites `main`.

- failed run: stop the runner, preserve `run.yaml`, append a ledger blocker and mark `agent:blocked`;
- bad branch: stop pushing, close or abandon the branch after review, then delete the branch only after approval;
- bad PR: convert to draft or close it, keep verification output and link the ledger entry;
- wrong labels: plan label correction in dry-run; live label mutation requires explicit approval;
- wrong task status: append a correction state and reason, never erase history;
- failed deploy: stop rollout, run health check, follow environment rollback procedure after human deploy approval;
- bad public submit: prepare correction/close/update plan; no public mutation without `public-submit` approval;
- security false positive: close private security workflow with sanitized audit entry and no public disclosure;
- run.yaml correction: write corrected state and append a new ledger entry rather than overwriting history silently;
- destructive cleanup requires explicit `destructive-rollback` approval;
- no main rewrite: no force-push and no history rewrite on `main`.

Dry-run helper:

```bash
python3 template-repo/scripts/automation-rollback-plan.py --issue 101 --branch codex/issue-101 --output /tmp/rollback.md
```
