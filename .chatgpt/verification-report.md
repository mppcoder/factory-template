# Отчет о проверке результата

## Что проверяли

- Historical red GitHub Actions CI #1-#5 from `2026-04-23`.
- Current GitHub Issues / PR backlog.
- PR #4 supersession state for Dependabot PRs #1, #2, #3.
- Current workflow baseline and current-main verification behavior.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-29-historical-actions-rerun-regression.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-2026-04-29-historical-actions-rerun-regression.md`.
- Слой: verification scripts / release audit portability.
- Статус remediation: fixed in scope.

## Что подтверждено

- Open GitHub Issues: `0`.
- Open GitHub PRs: `0`.
- PR #4 is `MERGED` and supersedes PRs #1, #2, #3.
- Current CI workflow uses `actions/checkout@v6`, `actions/setup-python@v6`, `actions/upload-artifact@v7`.
- Latest pre-fix CI on `main` was green: run `25101111513`, commit `7e6b63c350c4cfff1a8ebe113a722ef46fd40d3f`.
- CI #1 `24839250094` rerun reproduced old bug-024 snapshot: `EXAMPLES_TEST` / `validate-versioning-layer.py`.
- CI #2 `24839291045`, CI #3 `24839294182`, CI #4 `24839297068` reruns reproduced stale Dependabot PR failures on superseded merge bases.
- CI #5 `24839481282` rerun reproduced old fixed bug snapshot on commit `02fb8b7dfb5a74be13e1ba0211f24ac0fc1e0a82`.
- No hosted-runner acquisition blocker occurred in these five reruns.
- Current verification gap found separately: GitHub runner lacked `rg`, masking pre-release audit scan behavior; fixed by removing `rg` dependency and normalizing scan paths.

## Команды проверки

- `gh issue list --repo mppcoder/factory-template --state open --limit 50`: PASS, no open issues.
- `gh pr list --repo mppcoder/factory-template --state open --limit 50`: PASS, no open PRs.
- `gh pr view 4 --repo mppcoder/factory-template --json ...`: PASS, PR #4 `MERGED`.
- `gh run list --repo mppcoder/factory-template --limit 100 --json ...`: PASS, target runs identified.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --json ...`: PASS for CI #1-#5.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --verbose`: PASS for CI #1-#5.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --log-failed`: PASS where logs were available; job-log API used for PR run excerpts.
- `gh run rerun <RUN_ID> --repo mppcoder/factory-template --failed`: attempted for CI #1-#5.
- `gh run watch <RUN_ID> --repo mppcoder/factory-template --exit-status`: all five reruns completed red on old snapshot/stale PR verify step.
- `bash template-repo/scripts/verify-all.sh ci` from clean worktree with the fix-set applied: PASS.
- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.

## Итоговый вывод

The historical red CI runs are not new current-main regressions. They remain red because they rerun old snapshots or superseded Dependabot PR merge bases that predate the bug-024 fix. A separate current verification portability defect was found and fixed in scope.
