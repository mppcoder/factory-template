# Release ZIP GUI format compatibility issue

status: fixed
date: 2026-04-29
affected_layer: release packaging / install-from-scratch archive

## Title

Published release archive can be reported as invalid by user-side archive tools.

## Observed Behavior

User reported that the install-from-scratch archive "имеет не верный формат" and does not open.

Local reproduction with Linux tools did not show compressed-data corruption:

- `file _incoming/factory-v2.5.1.zip` reports `Zip archive data`.
- `unzip -t _incoming/factory-v2.5.1.zip` reports no compressed-data errors.
- `gh release download v2.5.1 --pattern 'factory-v2.5.1.zip'` downloads an asset with the same SHA256.

However, archive inspection found non-ASCII/mojibake paths under `bootstrap/`.

## Expected Behavior

The release archive intended for manual upload and install-from-scratch should open in ordinary archive tools, including GUI tools, and should avoid filename encoding ambiguity.

## Evidence

- `python3` zip inspection found 20 archive entries with non-ASCII paths.
- The affected paths are under `factory-v2.5.1/bootstrap/`.
- Several source filenames are mojibake-like names such as `bootstrap/01-╤ç╤é...factory-core.md`.

## Remediation Plan

1. Keep source files intact unless a separate content migration is approved.
2. Normalize `bootstrap/*.md` filenames to ASCII-only names inside the release staging tree.
3. Extend release package validation to fail on non-ASCII archive paths.
4. Rebuild the release package and checksum.
5. Re-upload corrected release assets or publish the corrected archive path, according to release decision.

## Status

fixed

Fix evidence:

- `RELEASE_BUILD.sh` normalizes `bootstrap/*.md` filenames inside the release staging tree to ASCII-only names.
- `template-repo/scripts/validate-release-package.py` now rejects non-ASCII paths in release archives.
- Rebuilt package evidence:
  - `python3` zip inspection: `NON_ASCII_COUNT=0`
  - `unzip -t _incoming/factory-v2.5.1.zip`: no compressed-data errors
  - `template-repo/scripts/validate-release-package.py`: release package valid
