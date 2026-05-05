# Required human-review policy

Required human review is mandatory for dangerous automation actions:

- auto-merge;
- production deploy;
- security issue autofix;
- public external report submit;
- high-risk issue fix;
- destructive rollback;
- parallel runner above 1;
- secret access;
- release publication.

Policy requirements:

- approval must be explicit;
- approval must match action scope;
- approval must be logged;
- approval expires or is single-use where applicable;
- approval cannot be inferred from issue text alone;
- comments from untrusted users do not approve.

Runner and gate scripts must call the permission model and approval layer before any dangerous action. If a matching approval is missing or stale, the action is refused and only a dry-run explanation is allowed.
