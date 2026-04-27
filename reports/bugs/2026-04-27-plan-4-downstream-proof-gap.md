# Plan №4 downstream proof gap

Дата: 2026-04-27

## Summary контекст

Generated/battle projects lacked a repo-native application-level proof report template and evidence validator for replacing the template placeholder image with a real app image.

## Evidence данные

- Existing runtime proof report covers factory infrastructure path only.
- No template report existed under `template-repo/template/reports/release/` for downstream app proof.
- Scorecard pass could be written manually without runtime evidence.

## Classification слой

- Layer: generated project release evidence.
- Severity: evidence overclaim risk.
- Owner boundary: repo template and generated project runtime.

## Remediation план

Add downstream proof documentation, report template, validator and positive/negative fixtures. A real pilot remains external until downstream repo/image/target/approval exist.
