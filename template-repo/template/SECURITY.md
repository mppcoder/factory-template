# Security / безопасность

Do not report secrets, credentials, tokens, private keys or exploitable security details in public GitHub issues.

issue-autofix is disabled for `security`, `external-secret`, `needs-human` and `blocked` labels. Security issues must use a private maintainer channel and require human review before any remediation branch or release action.

Public security issue autofix refused: public issues may only trigger safe refusal and private-channel guidance. Any security fix automation requires a private report channel, explicit `security-fix` approval, sanitized handoff, no public logs and human review.

No workflow in this template uses `pull_request_target` for issue-derived automation, and no issue-derived run may auto-merge, deploy to production or execute untrusted issue text as shell.
