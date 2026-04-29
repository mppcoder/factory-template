# Bug Report: historical Actions rerun exposed pre-release audit portability gap

- Date: `2026-04-29`
- Type: current verification defect found during historical GitHub Actions rerun closeout
- Layer: `factory-template / verification scripts`
- Scope decision: `fixed-in-scope`

## Reproduce

1. Confirm current GitHub CI run `25091820360` is green on `main` commit `7c52550b4f1426daeeb5fb1fbdeeb8de788c2ac3`.
2. Run current baseline from a clean detached worktree while invoking the script by absolute path:
   - `bash /tmp/factory-template-clean-verify-*/template-repo/scripts/verify-all.sh ci`
3. Observe `PRE_RELEASE_AUDIT` fail in local environments where `rg` exists.

## Evidence

- GitHub run: `25091820360`, job `73519351170`, step `Run consolidated verification`.
- GitHub log excerpt: `PRE_RELEASE_AUDIT` reached `VERSION SYNC CHECK ПРОЙДЕН (2.5.0)` and then printed `/PRE_RELEASE_AUDIT.sh: line 20: rg: command not found`, but the run still concluded green.
- Local clean worktree excerpt before the fix:
  - `ОШИБКА: найдены неожиданные legacy/versioning-layer ссылки вне разрешенной истории:`
  - `factory/producer/registry/projects-created.md:83:  версия_фабрики: 2.4.0-versioning-layer`
  - `factory/producer/registry/projects-created.md:93:  версия_фабрики: 2.4.0-versioning-layer`
  - `VERSION SYNC CHECK НЕ ПРОЙДЕН`
- After making the scan portable, the same gate also exposed active template leftovers:
  - `template-repo/template/.chatgpt/project-origin.md:13:factory-2.4.0-versioning-layer`
  - `template-repo/template/.chatgpt/project-origin.md:16:2.4.0-versioning-layer`
- Post-fix GitHub CI run `25101530394` failed because the stricter scan also matched the legacy evidence quoted inside this bug report. Defect-capture reports are historical evidence and must be allowed history for this scan.

## Expected

Verification scripts should behave consistently in GitHub Actions and local clean worktrees, without requiring `rg` and without changing legacy-reference allowlist behavior based on the caller working directory.

## Actual

- GitHub-hosted CI did not have `rg`; `PRE_RELEASE_AUDIT.sh` treated that missing command as a non-match inside an `if` condition and stayed green.
- `VERSION_SYNC_CHECK.sh` used `rg -g` excludes while searching an absolute root path. When invoked from outside the repo root, allowed historical files were not excluded consistently.

## Classification

- Current repo-side regression: yes, verification portability gap.
- Historical CI #1-#5 regression: no; those reruns reproduce old bug-024 `EXAMPLES_TEST` / `validate-versioning-layer.py` failures on old commits and stale PR merge bases.
- External runner blocker: no hosted-runner acquisition blocker observed.

## Fix

- Replaced the `PRE_RELEASE_AUDIT.sh` single-file `rg` check with `grep -Eq`.
- Replaced the repo-wide legacy scan in `VERSION_SYNC_CHECK.sh` with a Bash/find/grep implementation that:
  - has no `rg` dependency;
  - searches from `ROOT`;
  - preserves the existing allowed historical files.
- Updated active template `project-origin.md` to `factory-v2.5.0` / `2.5.0`; historical registry entries remain allowed history.
- Added `reports/bugs/*` to the legacy-reference allowed history so defect-capture evidence can quote old IDs without breaking release audit.

## Verification

- GitHub CI run `25101530394`: FAIL, scan matched this bug report's quoted historical evidence.
- `bash template-repo/scripts/verify-all.sh ci` from a clean worktree with the follow-up allowlist fix applied: PASS.
- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.
