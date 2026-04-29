# Factory Feedback: make verification scans portable without optional tools

- Date: `2026-04-29`
- Source bug: `reports/bugs/2026-04-29-historical-actions-rerun-regression.md`
- Layer: `factory-template verification / release audit`
- Reusable defect: yes

## Observation

Historical GitHub Actions rerun work surfaced that current verification scripts could give different results across environments:

- GitHub-hosted CI did not have `rg`, so a legacy scan in `PRE_RELEASE_AUDIT.sh` silently became a non-match.
- A repo-wide `rg -g` scan in `VERSION_SYNC_CHECK.sh` behaved differently when the script was invoked by absolute path from outside the repo root.

## Factory Learning

Release and CI gate scripts should not depend on optional developer tools unless the tool is installed by the workflow or the script fails explicitly with a clear missing-tool error. Path-sensitive scans should anchor themselves at the repo root before applying allowlists.

## Recommended Factory Rule

- Prefer POSIX/Bash baseline tools for release-blocking scans.
- If a release-blocking script uses `rg`, `jq`, or another optional tool, add a preflight `command -v` check that fails loudly.
- For allowlisted scans, search from `ROOT` and compare normalized repo-relative paths.

## Applied In This Task

- `PRE_RELEASE_AUDIT.sh` now uses `grep -Eq` for the single-file legacy check.
- `VERSION_SYNC_CHECK.sh` now uses `find` + `grep` with repo-relative allowlist matching.
- Active template `project-origin.md` now carries the current `2.5.0` factory identity instead of the old versioning-layer label.
