# Plan №5 orchestration runner write-before-fail

Date: 2026-04-28

## Summary

Plan №5 orchestration runner returned non-zero for an invalid secret-like parent plan, but created child session artifacts before exiting. This breaks the integrity/security boundary for Codex handoff orchestration.

## Severity

- High: write-before-fail/session leak in runner can create child session files from invalid or secret-like plans.
- Medium: `verify-all.sh` covered negative fixtures through the validator, but did not run runner-level negative smoke for write-before-fail behavior.
- Medium/Low: release-facing Plan №5 closeout text was stale and still made Plan №5 look like current implementation or next repo-local work after implementation evidence existed.

## Reproduction commands

```bash
tmp_dir="$(mktemp -d)"
python3 template-repo/scripts/orchestrate-codex-handoff.py \
  --root . \
  --plan tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml \
  --report "$tmp_dir/parent-orchestration-report.md"
echo "$?"
find "$tmp_dir" -maxdepth 3 -type f -printf '%P\n' | sort
```

Observed during defect capture:

- return code: `1`
- files created before failure: `parent-orchestration-report.md`, `sessions/secret-child.md`

## Expected behavior

Invalid orchestration plans fail before any output directory, child session file, prompt artifact or partial report containing invalid prompt content is created.

## Actual behavior

The runner creates `sessions_dir`, writes the child session file, writes the parent report and only then returns non-zero after validation errors are printed.

## Evidence files/paths

- Runner: `template-repo/scripts/orchestrate-codex-handoff.py`
- Verify script: `template-repo/scripts/verify-all.sh`
- Secret-like negative fixture: `tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml`
- Release-facing roadmap: `docs/releases/plan-5-internal-hardening-roadmap.md`
- Current state: `CURRENT_FUNCTIONAL_STATE.md`
- Test report: `TEST_REPORT.md`
- Gap register: `docs/releases/post-2.5-gap-register.md`

## Layer classification

- executable runner layer: `orchestrate-codex-handoff.py` must validate before creating sessions or reports.
- validator/verify layer: `verify-all.sh` must include runner-level negative smoke, not only validator negative fixtures.
- release-facing closeout layer: roadmap/current state/test report/gap register must describe Plan №5 status after the integrity follow-up honestly.

## Security/integrity boundary

- Invalid or secret-like plans must fail before creating `sessions_dir` or child session files.
- No secrets or private prompts from invalid plans may be written to repo, report or session artifacts.
- Failure output may include sanitized validation error summaries, but must not serialize invalid prompt content.

## Remediation plan

1. Move orchestration plan validation before output directory creation and before any session/report writes.
2. On validation errors, print a sanitized error summary and return non-zero immediately.
3. Preserve valid dry-run and optional `--execute` behavior after the validation gate.
4. Add runner-level negative smoke to `verify-all.sh`.
5. Update release-facing Plan №5 closeout docs and evidence.

## Verification plan

1. `python3 -m py_compile template-repo/scripts/orchestrate-codex-handoff.py`
2. Direct runner negative smoke against `tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml` in a temp output directory.
3. Existing orchestration validator positive/negative fixtures.
4. Curated pack quality validator.
5. Verified sync fallback evidence validator.
6. Artifact Eval for `vps-remote-ssh-orchestration`.
7. `bash template-repo/scripts/verify-all.sh quick`
8. `bash template-repo/scripts/verify-all.sh full`

## Factory feedback

Required. This is a reusable template runner/verify contract defect, not a one-off project-local issue.

Factory feedback report: `reports/factory-feedback/feedback-040-plan-5-orchestration-runner-write-before-fail.md`
