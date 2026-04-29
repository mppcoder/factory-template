# CLEAN_VERIFY_ARTIFACTS misses ignored `_artifacts`

Дата: 2026-04-29
Статус: fixed in current scope
Слой: `CLEAN_VERIFY_ARTIFACTS.sh`, `PRE_RELEASE_AUDIT.sh`, release verify cleanup

## Summary

Полный `template-repo/scripts/verify-all.sh` может падать на `PRE_RELEASE_AUDIT`, если в ignored `_artifacts/` остались старые release/source packs. `CLEAN_VERIFY_ARTIFACTS.sh` очищал `.release-stage`, `_sources-export`, `_factory-sync-export` и другие временные директории, но не `_artifacts`, тогда как version sync audit сканировал эти файлы и видел legacy release/versioning строки.

## Route

- `launch_source`: `chatgpt-handoff`
- `task_class`: `build`
- `selected_profile`: `build`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `medium`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> incidental defect capture -> cleanup remediation -> verification`
- `pipeline_stage`: `verification -> incidental cleanup remediation`
- `defect_capture_path`: `fixed-in-current-scope`

## Evidence

- `bash template-repo/scripts/verify-all.sh` прошел quick, onboarding smoke, smoke, examples и matrix, затем упал на `PRE_RELEASE_AUDIT`.
- Failure source: `_artifacts/release-2.4.3/.../CHANGELOG.md` и `_artifacts/release-followup-3a2963a/files/CHANGELOG.md` содержали historical legacy ids.
- `git status --short --untracked-files=all` не показывал `_artifacts`, то есть это ignored/generated release output, а не tracked source.
- `CLEAN_VERIFY_ARTIFACTS.sh` не содержал `_artifacts` в `TARGETS`.

## Expected behavior

Repo verify cleanup должен удалять ignored/generated `_artifacts` перед release audit, чтобы pre-release checks валидировали active source, а не stale generated archives.

## Remediation

- Добавить `_artifacts` в `CLEAN_VERIFY_ARTIFACTS.sh`.
- Добавить `_artifacts` в explicit `PRE_RELEASE_AUDIT.sh` forbidden artifact check, чтобы будущая ошибка была понятной до version sync scan.

