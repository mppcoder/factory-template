# Release ZIP path length compatibility issue

status: fixed
date: 2026-04-29
affected_layer: release packaging / install-from-scratch archive

## Title

Release archive fails user-side extraction because some paths are too long.

## Observed Behavior

User reported that the archive extraction fails with a "too long paths" error.

Archive inspection found long paths caused by transient smoke output trees under `tests/onboarding-smoke/.tmp-run/`.

## Expected Behavior

Install-from-scratch release archives should be portable for ordinary user extraction tools and should not include transient test output trees.

## Evidence

- Current archive entries: `4483`.
- Max archive path length before fix: `200`.
- Entries over 160 characters before fix: `473`.
- `tests/onboarding-smoke/.tmp-run/` contains `2550` generated files and is a transient test output tree.
- Removing `.tmp-run` from the release payload drops the max archive path length to `161`.

## Remediation Plan

1. Exclude `.tmp-run/` from release archives.
2. Extend release package validator with a portable max archive path length gate.
3. Rebuild archive, checksum and manifest.
4. Re-upload corrected GitHub Release assets.

## Status

fixed

Fix evidence:

- `.releaseignore` excludes `.tmp-run/`.
- `RELEASE_BUILD.sh` manifest records `max_archive_path_length: 180`.
- `template-repo/scripts/validate-release-package.py` rejects archive paths longer than `180`.
- Rebuilt archive evidence:
  - entries: `1589`
  - `TMP_RUN_COUNT=0`
  - `NON_ASCII_COUNT=0`
  - `MAX_PATH_LEN=161`
  - `unzip -t`: no compressed-data errors
  - release package validator: passed
