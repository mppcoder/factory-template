# Модель прав issue-autofix

Issue-autofix is gated before runner or branch work starts.

- accepted collaborator permissions: `admin`, `maintain`, `write`;
- dry-run fixtures may set `ISSUE_AUTOFIX_ACTOR_PERMISSION=write`;
- start label: `agent:ready`;
- state labels: `agent:claimed`, `agent:running`, `agent:pr-opened`, `agent:human-review`, `agent:done`;
- refusal/info labels: `agent:blocked`, `status:needs-info`;
- danger labels: `security`, `external-secret`, `needs-human`, `blocked`, `risk:high`;
- `risk:high` requires `agent:approved-high-risk`;
- label sync is dry-run by default and verification performs no live label mutation.

Trust model:
- no `pull_request_target`;
- no untrusted issue text as shell;
- no secrets in issue-derived runs;
- no auto-merge;
- no security issue autofix.
