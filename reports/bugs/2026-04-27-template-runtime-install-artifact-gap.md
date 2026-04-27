# Дефект: у template runtime не был явно описан install/reinstall artifact

Date: 2026-04-27

reusable: yes
learning_patch_status: not_required
learning_patch_reason: Remediation directly documents the reusable template runtime artifact and recovery contract; no separate learning proposal is needed.

## Summary

After separating `factory-template` template proof from downstream/battle app proof, the docs still did not clearly answer what artifact a new user installs on a VPS or uses to recover the VPS when no battle app exists yet.

## Evidence

User asked whether the template itself should have its own application image, npm install source or repo link for first install/reinstall after VPS failure.

The repo had a local placeholder app image builder, but it was described mostly as a placeholder workaround rather than the official template-owned reference runtime artifact.

## Layer Classification

- Layer: production runtime UX / template install and recovery docs.
- Defect class: missing template-owned runtime artifact contract.
- Owner boundary: repo docs and release-facing status.
- External boundary: publishing a public registry image or npm package is optional future packaging, not required for the current repo-first template proof.

## Remediation

Document `deploy/static-placeholder` plus `template-repo/scripts/build-placeholder-app-image.py` as the canonical `factory-template` reference runtime app:

- source lives in this repo;
- built locally as `factory-template-placeholder-app:local`;
- used for first install, smoke checks and VPS recovery when no downstream app exists;
- downstream/battle projects can later replace `APP_IMAGE` with their own real app image.

## Status

Captured and remediated in current scope.
