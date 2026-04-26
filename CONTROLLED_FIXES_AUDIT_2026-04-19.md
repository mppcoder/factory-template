# Controlled Fixes Audit — 2026-04-19

## Scope

- Repo under audit: `/projects/factory-template`
- Source pack unpacked from: `/projects/factory-template/_incoming/docs/operator/factory-template.zip`  (historical path normalized to current canonical VPS layout)
- Boundary mode: repo-only, no external actions
- Git status: not available, because `/projects/factory-template` is currently not initialized as a git repository

## Repo Structure Snapshot

- `template-repo/`: canonical project template, launcher, validators, scenario-pack
- `factory/producer/reference/examples/`: golden and scaffold examples
- `project-knowledge/factory/template-evolution/`: meta layer for factory evolution and release notes
- `factory/producer/extensions/workspace-packs/`: optional operational packs
- `domain-packs/`: optional domain overlays
- `bootstrap/`: operator guides and workflow notes
- `factory/producer/registry/`: release and project registry
- `docs/operator/factory-template/`: unpacked runbooks and operator materials from incoming zip

### Directory Counts

- `template-repo/scripts`: 21 files
- `template-repo/scenario-pack`: 31 files, 2 directories
- `factory/producer/reference/examples`: 228 files, 69 directories
- `bootstrap`: 22 files
- `project-knowledge/factory/template-evolution`: 26 files, 10 directories
- `factory/producer/extensions/workspace-packs`: 19 files, 7 directories
- `domain-packs`: 4 files, 4 directories
- `registry`: 5 files
- `docs/operator/factory-template`: 8 files

## Self-Tests And Audits

- `bash POST_UNZIP_SETUP.sh`: PASS
- `bash SMOKE_TEST.sh`: PASS
- `bash EXAMPLES_TEST.sh`: PASS
- `bash MATRIX_TEST.sh`: PASS
- `bash PRE_RELEASE_AUDIT.sh`: FAIL

## Progress Update After Controlled Fixes

Closed in this iteration:

- release identity aligned to `2.4.0` in `FACTORY_MANIFEST.yaml`
- root and template changelogs moved from pseudo-version `2.4.0-codex-dogfood-p1` to `Unreleased`
- canonical state filename unified to `CURRENT_FUNCTIONAL_STATE.md` across scripts, scenario-pack, template README, and ops tooling
- runbooks updated to point at actual repo topology
- repo-first guidance rewritten to reference real files from the repo
- `CLEAN_VERIFY_ARTIFACTS.sh` added to make self-test -> cleanup -> pre-release audit reproducible

Current validation state after fixes:

- `bash VERSION_SYNC_CHECK.sh`: PASS
- `bash SMOKE_TEST.sh`: PASS
- `bash EXAMPLES_TEST.sh`: PASS
- `bash MATRIX_TEST.sh`: PASS
- `bash CLEAN_VERIFY_ARTIFACTS.sh && bash PRE_RELEASE_AUDIT.sh`: PASS

### PRE_RELEASE_AUDIT Failure Breakdown

Operational failures caused by test artifacts left in repo root:

- forbidden `.smoke-test`
- forbidden `audit-smoke-project`
- forbidden `*.log`
- forbidden `_sources-export`
- forbidden `_factory-sync-export`
- forbidden `.matrix-test`

Content failure caused by release metadata drift:

- `FACTORY_MANIFEST.yaml` has `name: factory-v2.4.0-codex-dogfood-p1`
- `VERSION.md` and `VERSION_SYNC_CHECK.sh` expect `factory-v2.4.0`

## Fixed-State Snapshot Anchors

Reference hashes for key files before any controlled fixes:

```text
71188c0d33afdbb6  README.md
1c86b4d4c0255dca  VERSION.md
e43f45e62fe9ab4e  CHANGELOG.md
3ab6462900940983  CURRENT_FUNCTIONAL_STATE.md
480b07d0519d6343  FACTORY_MANIFEST.yaml
4005420e4e00c08c  template-repo/README.md
b81e6f68560695c9  template-repo/CHANGELOG.md
9d69ef183a586de2  template-repo/launcher.sh
087746eb358acd9a  template-repo/scripts/check-dod.py
336796ca3038b9e0  template-repo/scripts/validate-versioning-layer.py
e1e2211a7ac9f7f0  template-repo/scripts/create-codex-task-pack.py
8572c0fd6b7029c4  template-repo/scenario-pack/16-done-closeout.md
5376f2cf730353b3  template-repo/scenario-pack/brownfield/09-brownfield-closeout.md
774787a8d0969088  docs/operator/factory-template/01-runbook-dlya-polzovatelya-factory-template.md
85936eefca4368eb  docs/operator/factory-template/02-runbook-dlya-codex-factory-template.md
1aa98e3685cf9357  docs/operator/factory-template/04-chatgpt-project-sources-factory-template-20-cap.md
```

## Inconsistency Map

### A. Release Metadata Drift

1. `VERSION.md` declares current release `2.4.0`, but root metadata also carries a new patch line.
2. `CHANGELOG.md` and `template-repo/CHANGELOG.md` start with `2.4.0-codex-dogfood-p1`, while root version stays `2.4.0`.
3. `FACTORY_MANIFEST.yaml` uses `factory-v2.4.0-codex-dogfood-p1`, which breaks `VERSION_SYNC_CHECK.sh`.

Impact:

- release audit is red even on otherwise healthy content
- repo does not have one authoritative release identity

### B. Versioning Filename Drift

Current canonical validator expectation:

- `template-repo/scripts/validate-versioning-layer.py` requires `CURRENT_FUNCTIONAL_STATE.md`

Legacy references still active:

- `template-repo/scripts/check-dod.py` requires `CURRENT_STATE.md`
- `template-repo/scripts/create-codex-task-pack.py` tells user to update `CURRENT_STATE.md`
- `template-repo/scenario-pack/16-done-closeout.md` refers to `CURRENT_STATE.md`
- `template-repo/scenario-pack/brownfield/09-brownfield-closeout.md` refers to `CURRENT_STATE.md`
- `template-repo/template/README.md` lists `CURRENT_STATE.md`
- `docs/operator/factory-template/04-chatgpt-project-sources-factory-template-20-cap.md` lists `CURRENT_STATE.md`
- `factory/producer/extensions/workspace-packs/factory-ops/detect-factory-issues.py` looks for `CURRENT_STATE.md`

Impact:

- docs, validators, handoff checklist, and ops tooling disagree on the required project state file
- tests pass only because examples and generated projects currently carry compatibility overlap

### C. Runbook-To-Repo Topology Drift

`docs/operator/factory-template/02-runbook-dlya-codex-factory-template.md` tells Codex to inventory:

- `scripts/`
- `scenario-pack/`
- `.chatgpt/`
- `examples/`

Actual repo topology is:

- `template-repo/scripts/`
- `template-repo/scenario-pack/`
- no root `.chatgpt/`
- `factory/producer/reference/examples/`

Impact:

- runbook inventory instructions do not match the real repository layout
- a new operator can search the wrong paths first

### D. Repo-First / Reference Pack Policy Drift

`docs/operator/factory-template/04-chatgpt-project-sources-factory-template-20-cap.md` recommends permanent Sources files that are absent from repo:

- `factory-template-overview.md`
- `factory-release-policy.md`
- `scenario-pack-index.md`
- `launcher-behavior.md`
- `validators-policy.md`
- `source-pack-policy.md`
- `codex-task-pack-policy.md`
- `.chatgpt/codex-task-pack.md` at repo root
- `CURRENT_STATE.md`
- `RELEASE_NOTES.md` at repo root

Impact:

- the curated repo-first/reference guidance is not executable as written
- user cannot follow the documented 20-file pack literally

### E. Verify/Release Lifecycle Drift

`PRE_RELEASE_AUDIT.sh` forbids temporary test and export artifacts in repo root, while current self-tests create them in repo root and keep them after completion:

- `.smoke-test`
- `.matrix-test`
- `_sources-export`
- `_factory-sync-export`
- smoke project directory
- logs

Impact:

- a normal test run leaves the tree in a state that fails pre-release audit
- release hygiene depends on undocumented manual cleanup or fresh unpack

### F. Example Coverage Model Is Implicit

`EXAMPLES_TEST.sh` validates examples with canonical scripts from `template-repo/scripts`, while working examples intentionally do not contain local `scripts/`.

Impact:

- this may be correct by design, but it is not explicitly documented in the runbook set
- example validation currently tests content compatibility with canonical validators, not example-local automation bundles

## Controlled Fixes Plan

### Priority 0: Make Release Identity Single-Valued

1. Decide whether repo head is still final `2.4.0` or already `2.4.0-codex-dogfood-p1`.
2. Align `VERSION.md`, `CHANGELOG.md`, `template-repo/CHANGELOG.md`, `FACTORY_MANIFEST.yaml`, and any release-facing docs to that single answer.
3. Re-run `VERSION_SYNC_CHECK.sh` and `PRE_RELEASE_AUDIT.sh` on a clean tree.

### Priority 1: Unify State Filename Across Docs, Scripts, And Packs

1. Pick one canonical file name:
   `CURRENT_FUNCTIONAL_STATE.md` is already enforced by validators and root docs, so it is the safest candidate.
2. Update legacy references in:
   - `template-repo/scripts/check-dod.py`
   - `template-repo/scripts/create-codex-task-pack.py`
   - `template-repo/scenario-pack/16-done-closeout.md`
   - `template-repo/scenario-pack/brownfield/09-brownfield-closeout.md`
   - `template-repo/template/README.md`
   - `factory/producer/extensions/workspace-packs/factory-ops/detect-factory-issues.py`
   - operator docs in `docs/operator/factory-template/`
3. Re-run smoke, examples, matrix, and targeted validators.

### Priority 2: Fix Runbook Topology Language

1. Update Codex and user runbooks to name actual repo paths:
   - `template-repo/scripts`
   - `template-repo/scenario-pack`
   - `factory/producer/reference/examples`
   - clarify that project `.chatgpt/` lives inside generated/example projects, not repo root
2. Add one concise repo map section to reduce path ambiguity.

### Priority 3: Make Repo-First Guidance Executable

1. Replace non-existent file names in the 20-cap guide with real files, or create the missing policy/index docs intentionally.
2. Decide whether root-level `.chatgpt/codex-task-pack.md` is meant to exist; if not, remove it from the permanent Sources recommendation.
3. Align repo-first/reference guidance with the actual export flow from `template-repo/scripts/export-sources-pack.sh`.

### Priority 4: Clean Verify/Release Ergonomics

1. Decide whether self-tests should:
   - auto-clean after themselves, or
   - write under a single ignored temp root, or
   - be paired with a cleanup script
2. Document the expected order:
   clean tree -> pre-release audit -> self-tests -> cleanup -> pre-release audit / release build
3. Ensure release audit can be reproduced without relying on a freshly unpacked archive.

### Priority 5: Clarify Example Validation Contract

1. Document that working examples are content fixtures validated by canonical template validators.
2. If stronger guarantees are needed, add an explicit sync or fixture audit for example structure vs template expectations.

## Recommended Execution Order

1. Release identity alignment
2. `CURRENT_STATE.md` -> `CURRENT_FUNCTIONAL_STATE.md` convergence
3. runbook topology cleanup
4. sources-pack guide cleanup
5. verify/release cleanup strategy
6. optional example-contract hardening

## Exit Criteria For Controlled Fixes

- `VERSION_SYNC_CHECK.sh` passes
- `PRE_RELEASE_AUDIT.sh` passes on a clean working tree
- `SMOKE_TEST.sh`, `EXAMPLES_TEST.sh`, `MATRIX_TEST.sh` pass after fixes
- runbooks reference real paths and real files
- docs and validators agree on the canonical state file name
- Sources guidance can be followed literally without guesswork
