# Security / безопасность

Do not report secrets, credentials, tokens, private keys or exploitable security details in public GitHub issues.

issue-autofix is disabled for `security`, `external-secret`, `needs-human` and `blocked` labels. Security issues must use a private maintainer channel and require human review before any remediation branch or release action.

No workflow in this template uses `pull_request_target` for issue-derived automation, and no issue-derived run may auto-merge, deploy to production or execute untrusted issue text as shell.
