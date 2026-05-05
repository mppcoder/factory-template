# Automation rollback

Rollback is a recovery policy for branches, PRs, labels, task state and run files. It never rewrites `main`.

- failed run: stop the runner, preserve `run.yaml`, append a ledger blocker and mark `agent:blocked`;
- bad branch: stop pushing, close or abandon the branch after review, then delete the branch if safe;
- bad PR: convert to draft or close it, keep verification output and link the ledger entry;
- label reset: remove `agent:running`, keep `agent:blocked` until a human clears the state;
- task status reset: move FT-TASK back to `blocked` or `ready_for_handoff` with a reason;
- run.yaml correction: write corrected state and append a new ledger entry rather than overwriting history silently;
- no main rewrite: no force-push and no history rewrite on `main`.

Dry-run helper:

```bash
python3 template-repo/scripts/automation-rollback-plan.py --issue 101 --branch codex/issue-101 --output /tmp/rollback.md
```
