# Bug: runtime proof required a real app image when a generated placeholder was enough

Date: 2026-04-27

## Summary

After 2.6 runtime proof, the closeout told the operator to provide a real `APP_IMAGE` for application-level proof. For a template/runtime smoke path, Codex can provide a generated placeholder application image/page while keeping the boundary clear: placeholder proof is not business application proof.

## Evidence

The runtime proof passed with `APP_IMAGE=nginx:1.27-alpine`, but the user still had to ask for Codex to generate and install a placeholder app/image/page rather than pushing that work back to the operator. Follow-up clarification showed `APP_IMAGE` was ambiguous in Russian: it can read as "program image" that Codex should generate for this template stage, not as a logo/image URL.

## Layer Classification

- Layer: production runtime proof UX / placeholder app path.
- Defect class: excessive user burden and missing placeholder option.
- Owner boundary: repo/template for placeholder defaults and installer; user only supplies real app image when they want real application proof.

## Remediation

Add a repo-native static placeholder asset, local app image builder and installer:

- `deploy/static-placeholder/index.html`
- `deploy/static-placeholder/placeholder.svg`
- `template-repo/scripts/build-placeholder-app-image.py`
- `template-repo/scripts/install-static-placeholder.py`

Update production env preparation/docs so the default path can choose placeholder mode, generate `factory-template-placeholder-app:local`, set `APP_PULL_POLICY=never` for that local tag and optionally accept a custom image URL.

## Status

Captured and remediated in current scope.
