# Automation rollback / откат

- failed run: stop runner, preserve `run.yaml`, append blocker and mark `agent:blocked`;
- bad branch: stop pushing and delete only after review;
- bad PR: draft or close, keep verification output;
- wrong labels: dry-run correction plan only; live label mutation requires explicit approval;
- wrong task status: append correction state, never erase history;
- failed deploy: stop rollout, run health check and use approved rollback procedure;
- bad public submit: prepare correction/close/update plan without live public mutation;
- security false positive: close private workflow with sanitized audit entry;
- run.yaml correction: append corrected audit state;
- destructive cleanup requires explicit approval;
- no main rewrite: never force-push or rewrite `main`.
