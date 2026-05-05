# Issue-autofix permission model

Issue-autofix is gated before any runner or branch work starts.

## Actor checks

- accepted GitHub collaborator permissions: `admin`, `maintain`, `write`;
- unknown or lower permission is refused with `agent:blocked`;
- local dry-run fixtures may set `ISSUE_AUTOFIX_ACTOR_PERMISSION=write` to avoid live GitHub API calls;
- public or anonymous issue text is always untrusted data.

## Label gates

Required operator labels and states are documented in `.github/labels.yml`:

- start label: `agent:ready`;
- claimed/running labels: `agent:claimed`, `agent:running`;
- completion/review labels: `agent:pr-opened`, `agent:human-review`, `agent:done`;
- refusal/info labels: `agent:blocked`, `status:needs-info`;
- danger labels: `security`, `external-secret`, `needs-human`, `blocked`, `risk:high`.

`risk:high` requires `agent:approved-high-risk`. Labels `security`, `external-secret`, `needs-human` and `blocked` always refuse automation.

## Label sync

Label sync is dry-run by default. Verification must not mutate live GitHub labels/issues. Any command that creates or updates labels must have an explicit write flag and operator approval. The default verification contract is no live label mutation.

## Trust model

- never use `pull_request_target`;
- never run untrusted issue text as shell;
- never pass secrets into issue-derived runs;
- no auto-merge;
- no security issue autofix.
