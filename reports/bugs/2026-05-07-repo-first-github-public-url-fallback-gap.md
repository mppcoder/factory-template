# Bug: repo-first-github-public-url-fallback-gap

Date: 2026-05-07
Status: fixed-in-current-scope

## Symptom

Repo-first guidance said "читать GitHub repo" or "сценарии читаются из GitHub repo" without saying that ChatGPT/Codex must prefer GitHub connector, repo tool or authenticated `gh` over public `github.com` / raw URLs.

## Impact

- ChatGPT/Codex could treat public GitHub/raw URLs as the default route for `mppcoder/factory-template`.
- Private or permission-sensitive repo access semantics could be bypassed.
- The first-answer/router contract could still be followed superficially while using the wrong repo access channel.

## Expected Behavior

For GitHub repo `mppcoder/factory-template`, ChatGPT/Codex repo reads and writes use GitHub connector / repo tool / authenticated `gh` when available.

Public `github.com` or `raw.githubusercontent.com` fallback is allowed only when a blocker is explicitly named:
- connector unavailable;
- no permission;
- repo not installed in connector;
- authenticated repo tool unavailable;
- user explicitly asks for public URL.

## Actual Evidence

- User rule: "запросы к гитхаб должны идти не через публичные url а через коннекторы".
- `template-repo/README.md`, generated `.chatgpt/boundary-actions.md`, `template-repo/template/README.md`, `template-repo/template/docs/integrations.md` and `template-repo/scripts/create-codex-task-pack.py` used broad "GitHub repo" wording.
- `docs/operator/runbook-packages/01-factory-template/02-codex-runbook.md` used public HTTPS clone before authenticated `gh repo clone`.

## Layer Classification

- defect class: `repo-first-github-access-contract`
- affected layer: scenario-pack / AGENTS / `.chatgpt` boundary docs / runbooks / validators
- reusable downstream issue: yes
- not in scope: user browser setup pages and release download URLs that are not ChatGPT/Codex repo reads

## Required Remediation

1. Add a scenario-pack contract that repo-first GitHub access means connector/tool/authenticated `gh` first.
2. Update generated/source `.chatgpt` and documentation wording so "read GitHub repo" does not imply browser/public URL by default.
3. Update Codex runbook clone flow to prefer `gh repo clone`.
4. Add validator coverage for the invariant.

## Verification Target

- `python3 template-repo/scripts/validate-repo-first-github-access.py .`
- `python3 template-repo/scripts/validate-codex-task-pack.py .`
- `python3 template-repo/scripts/validate-runbook-packages.py .`
- `bash template-repo/scripts/verify-all.sh quick`
