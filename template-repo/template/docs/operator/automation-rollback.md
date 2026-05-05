# Automation rollback / откат

- failed run: stop runner, preserve `run.yaml`, append blocker and mark `agent:blocked`;
- bad branch: stop pushing and delete only after review;
- bad PR: draft or close, keep verification output;
- label reset: remove `agent:running`, keep `agent:blocked` until cleared;
- task status reset: move FT-TASK back with a reason;
- run.yaml correction: append corrected audit state;
- no main rewrite: never force-push or rewrite `main`.
