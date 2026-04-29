# Отчет о проверке результата

## Что проверяли

- GitHub Actions backlog после hosted runner acquisition failures.
- Open GitHub Issues / PRs.
- Historical red runs in the recent Actions window.
- Whether reruns reach repo steps or expose a real repo-side CI regression.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-28-ci-run-64-project-root-boundary-regression.md`.
- Factory feedback не требуется: reusable factory/process defect не подтвержден.
- Слой: CI workflow / GitHub-hosted runner acquisition.
- Статус remediation: repo code changes not required; affected runs rerun successfully after GitHub-hosted runner acquisition recovered.

## Что подтверждено

- Open GitHub Issues: `0`.
- Open GitHub PRs: `0`.
- Closed PR check: PR #4 is `MERGED`; Dependabot PRs #1, #2, #3 are `CLOSED`.
- Historical red runs inspected: `25054700529`, `25057090187`, `25058477360`, `25059862780`.
- Each red run originally had `verify-baseline` cancelled before steps with annotation `The job was not acquired by Runner of type hosted even after multiple attempts`.
- Each inspected red run was rerun and is now green; both `verify-baseline` and `release-bundle-dry-run` passed.
- No checkout/setup-python/pip/verify-all/release-bundle repo-side failure appeared.

## Команды проверки

- `gh issue list --repo mppcoder/factory-template --state open --limit 50`: PASS, no open issues.
- `gh pr list --repo mppcoder/factory-template --state open --limit 50`: PASS, no open PRs.
- `gh pr list --repo mppcoder/factory-template --state closed --limit 10`: PASS, PR #4 merged and PRs #1-#3 closed.
- `gh run list --repo mppcoder/factory-template --limit 30`: PASS, four historical red runs identified.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --json name,event,status,conclusion,headSha,headBranch,displayTitle,createdAt,updatedAt,jobs`: PASS for `25054700529`, `25057090187`, `25058477360`, `25059862780`.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --verbose`: PASS for all four red runs; runner acquisition annotation captured.
- `gh run view <RUN_ID> --repo mppcoder/factory-template --log-failed`: PASS as evidence collection for all four red runs; no failed step logs existed before rerun.
- `gh run rerun <RUN_ID> --repo mppcoder/factory-template --failed`: PASS for all four red runs.
- `gh run watch <RUN_ID> --repo mppcoder/factory-template --exit-status`: PASS for all four reruns.
- `gh run list --repo mppcoder/factory-template --limit 12`: PASS, recent window shows inspected red runs now `completed success`.

## Итоговый вывод

The red Actions were external GitHub-hosted runner acquisition failures. After rerun, all inspected runs reached repo steps and passed. No repo-side CI regression was found, and no remediation or new defect report is required.
