# Security Policy

## Supported Versions

| Version line | Status |
| --- | --- |
| 2.5.x | Supported |
| 2.4.x | Security fixes only |
| < 2.4 | Not supported |

## Reporting a Vulnerability

1. Use GitHub Private Vulnerability Reporting for this repository.
2. Include reproducible steps, affected paths, and impact.
3. Do not publish exploit details in public issues before triage.

If private reporting is unavailable, open a minimal public issue without sensitive details and request a secure follow-up channel.

## Response Targets

- Initial triage: within 3 business days.
- Status update after triage: within 7 business days.
- Critical/high severity fixes: prioritized for nearest patch window.

## Secret Handling Baseline

- Never commit real credentials, tokens, keys, or session artifacts.
- Keep local secrets in non-committed `.env` files; use `.env.example` as the only committed template.
- Never paste secrets into `.chatgpt/*`, bug reports, release notes, or handoff artifacts.
- For CI, store secrets only in GitHub Actions Secrets and avoid printing them in logs.
- Rotate credentials immediately if accidental exposure is suspected.

## Coordinated Disclosure

Security fixes should include:

- clear impact statement,
- verification evidence,
- release notes entry when applicable,
- follow-up hardening tasks for reusable defects.
