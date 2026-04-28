# Отчет о дефекте

## Заголовок
GitHub Actions CI run #64 для `feat: Закрепить project-root boundary для intermediate repos` завершился failure до запуска шагов job из-за недоступности hosted runner.

## Failing GitHub run / job / step
- Repository: `mppcoder/factory-template`
- Workflow: `CI`
- Run ID: `25054700529`
- Display title: `feat: Закрепить project-root boundary для intermediate repos`
- Commit: `750ce6a787cf304d24af14ab856da34bb63221e0`
- Branch/event: `main` / `push`
- Job: `verify-baseline`
- Job ID: `73391634384`
- Step: runner acquisition before checkout; workflow steps were not started.
- Dependent job: `release-bundle-dry-run` skipped because it needs `verify-baseline`.

## Exact failing command
The intended workflow command was:

```bash
bash template-repo/scripts/verify-all.sh ci
```

GitHub Actions did not reach that command in run `25054700529`; the hosted runner was not acquired.

## Expected behavior
- GitHub-hosted runner starts `verify-baseline`.
- `verify-baseline` checks out the repo, installs Python dependencies and runs `bash template-repo/scripts/verify-all.sh ci`.
- `release-bundle-dry-run` runs after successful baseline verification.

## Actual behavior
- Run conclusion: `failure`.
- `verify-baseline` conclusion: `cancelled`, duration about 15 minutes.
- `release-bundle-dry-run` conclusion: `skipped`.
- No failed step log was available because the job did not start execution.

## Evidence from GitHub log
Commands run:

```bash
gh run list --repo mppcoder/factory-template --limit 20
gh run view 25054700529 --repo mppcoder/factory-template --log-failed
gh run view 25054700529 --repo mppcoder/factory-template --json name,event,status,conclusion,headSha,headBranch,displayTitle,createdAt,updatedAt,jobs
gh run view 25054700529 --repo mppcoder/factory-template --verbose
gh api repos/mppcoder/factory-template/actions/jobs/73391634384/logs --include
```

Observed evidence:

```text
completed failure feat: Закрепить project-root boundary для intermediate repos CI main push 25054700529 15m3s 2026-04-28T13:08:58Z
```

```json
{
  "conclusion": "failure",
  "displayTitle": "feat: Закрепить project-root boundary для intermediate repos",
  "headSha": "750ce6a787cf304d24af14ab856da34bb63221e0",
  "jobs": [
    {
      "conclusion": "cancelled",
      "name": "verify-baseline",
      "databaseId": 73391634384
    },
    {
      "conclusion": "skipped",
      "name": "release-bundle-dry-run",
      "databaseId": 73394348560
    }
  ]
}
```

`gh run view --verbose` annotation:

```text
The job was not acquired by Runner of type hosted even after multiple attempts
verify-baseline: .github#1
```

`gh run view --log-failed` returned no failed step output. Direct job log retrieval returned:

```text
HTTP/1.1 404 The specified blob does not exist.
```

This is consistent with the job never reaching step execution.

## Local reproduction result
Current checkout is the failed commit:

```text
750ce6a787cf304d24af14ab856da34bb63221e0
feat: Закрепить project-root boundary для intermediate repos
```

Local command requested by the handoff:

```bash
python3 -m pip install -r requirements.txt
```

Result in this local environment:

```text
error: externally-managed-environment
```

Because this host blocks system-wide pip installs under PEP 668, reproduction continued in a temporary venv outside the repo:

```bash
python3 -m venv /tmp/factory-template-ci-venv
. /tmp/factory-template-ci-venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash template-repo/scripts/verify-all.sh ci
```

Result:

```text
VERIFY-ALL ПРОЙДЕН (ci)
```

Local reproduction did not reproduce a repo-level CI regression.

## Layer classification
- Primary layer: CI workflow / GitHub-hosted runner acquisition.
- Verify pipeline: not reached in the failed GitHub run; locally passed.
- Validator: not implicated.
- Artifact eval: not implicated.
- Docs contract: not implicated.
- Task-pack: not implicated.
- Closeout artifact: updated to record evidence and resolution.

## Reusable factory feedback required
No. The failure was caused by GitHub Actions hosted runner acquisition, not by a reusable factory/template/process defect. No validator gate was weakened.

## Remediation / status
- No repo code remediation required.
- Failed job rerun requested with:

```bash
gh run rerun 25054700529 --repo mppcoder/factory-template --failed
```

- Rerun attempt used new `verify-baseline` job ID `73397267282` and again failed before checkout:

```text
The job was not acquired by Runner of type hosted even after multiple attempts
```

- Local CI baseline passes on commit `750ce6a787cf304d24af14ab856da34bb63221e0`.
- External blocker remains: GitHub-hosted runner acquisition for this repository/run.
