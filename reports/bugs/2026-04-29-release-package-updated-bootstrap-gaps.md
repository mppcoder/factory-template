# Release package updated bootstrap gaps

## Title

Release package for install-from-scratch lacked explicit manifest, checksum, package validator and fallback wording.

## Observed behavior

- `RELEASE_BUILD.sh` built `factory-v<VERSION>.zip`, but did not generate a sidecar manifest or SHA256 checksum.
- Install-from-scratch runbooks described `_incoming` and repo/bootstrap work, but did not give a complete fallback archive path with checksum verification, single-root validation and expected evidence.
- `package.json` is absent, so npm is not a supported canonical install/download path for this repo.
- Release checklist said the release bundle could be assembled, but did not explicitly require archive checksum/manifest validation on a freshly unpacked package.

## Expected behavior

- Release package assembly must produce:
  - canonical archive `factory-v<VERSION>.zip`;
  - one archive root `factory-v<VERSION>/`;
  - manifest with version, source commit, build timestamp, included/excluded paths, first-run commands, verification status and npm support status;
  - SHA256 checksum file usable with `sha256sum -c <file>.sha256`;
  - deterministic validator for the already-built zip.
- User and Codex runbooks must distinguish canonical GitHub clone/download or release artifact from manual fallback archive upload.
- Docs must not claim npm install/download support when no `package.json` or npm packaging contract exists.

## Affected layer

- release packaging
- install-from-scratch runbooks
- Codex package verification
- release checklist / release notes

## Evidence

- `find . -name package.json` returned no files.
- `RELEASE_BUILD.sh` only staged files, ran `VERSION_SYNC_CHECK.sh` / `PRE_RELEASE_AUDIT.sh`, zipped the stage and printed the archive path.
- `.releaseignore` excluded common transient paths, but release package verification did not have its own manifest/checksum gate.

## Remediation plan

1. Treat this as release-facing installation contract change and prepare patch release `2.5.1`.
2. Extend `RELEASE_BUILD.sh` instead of creating a competing release builder.
3. Add a zip validator for archive root, required files, forbidden paths, manifest and checksum.
4. Update user and Codex runbooks with canonical and fallback install-from-scratch flows.
5. Update release checklist, release notes, changelog and handoff implementation register.
6. Build, unpack and verify the package.

## Status

closed

## Remediation evidence

- `VERSION.md` and version-linked manifests updated to `2.5.1`.
- `RELEASE_BUILD.sh` now produces archive, sidecar manifest and SHA256 checksum.
- `template-repo/scripts/validate-release-package.py` validates zip root, forbidden paths, manifest, checksum and required files.
- User and Codex runbooks document GitHub/release artifact canonical path, manual archive upload fallback and unsupported npm path.
- `bash RELEASE_BUILD.sh` passed.
- `sha256sum -c factory-v2.5.1.zip.sha256` passed.
- Unpacked archive quick verify passed from temp root.
