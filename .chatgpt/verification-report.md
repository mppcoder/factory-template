# Отчет о проверке результата

## Что проверяли

- GitHub Actions failure для run `25054700529` / run #64.
- Реальный failing layer по GitHub logs и job metadata.
- Локальное воспроизведение на commit `750ce6a787cf304d24af14ab856da34bb63221e0`.
- Минимальные проверки project-root boundary и repo baseline после defect capture.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-28-ci-run-64-project-root-boundary-regression.md`.
- Factory feedback не требуется: reusable factory/process defect не подтвержден.
- Слой: CI workflow / GitHub-hosted runner acquisition.
- Статус remediation: repo code changes not required; failed GitHub job rerun attempted and hit the same hosted runner acquisition blocker.

## Что подтверждено

- `gh run view 25054700529 --verbose` сообщает: `The job was not acquired by Runner of type hosted even after multiple attempts`.
- `verify-baseline` был `cancelled` до запуска workflow steps; `release-bundle-dry-run` был `skipped`.
- `gh run view 25054700529 --repo mppcoder/factory-template --log-failed` не вернул step log, а direct job log API вернул `404 The specified blob does not exist`.
- Локальный `bash template-repo/scripts/verify-all.sh ci` на том же commit прошел успешно.
- Rerun failed job created job ID `73397267282`, which also ended as `cancelled` after 15m1s with the same hosted runner acquisition annotation.

## Команды проверки

- `gh run list --repo mppcoder/factory-template --limit 20`: PASS, failed run найден.
- `gh run view 25054700529 --repo mppcoder/factory-template --json name,event,status,conclusion,headSha,headBranch,displayTitle,createdAt,updatedAt,jobs`: PASS.
- `gh run view 25054700529 --repo mppcoder/factory-template --verbose`: PASS, runner acquisition annotation captured.
- `gh run view 25054700529 --repo mppcoder/factory-template --log-failed`: PASS as evidence collection, no failed step log available.
- `python3 -m pip install -r requirements.txt`: BLOCKED locally by PEP 668 `externally-managed-environment`.
- `python3 -m venv /tmp/factory-template-ci-venv && . /tmp/factory-template-ci-venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt && bash template-repo/scripts/verify-all.sh ci`: PASS, `VERIFY-ALL ПРОЙДЕН (ci)`.
- `python3 template-repo/scripts/validate-tree-contract.py .`: PASS.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/project-root-boundary.yaml --output tests/artifact-eval/reports/project-root-boundary.md`: PASS.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/project-root-boundary.md`: PASS.
- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick`: PASS, `VERIFY-ALL ПРОЙДЕН (quick)`.
- `bash template-repo/scripts/verify-all.sh ci`: PASS, `VERIFY-ALL ПРОЙДЕН (ci)`.
- `gh run rerun 25054700529 --repo mppcoder/factory-template --failed`: accepted by GitHub.
- `gh run watch 25054700529 --repo mppcoder/factory-template --exit-status`: FAIL due to hosted runner acquisition, no repository step execution.

## Итоговый вывод

Run #64 failed before repository commands were executed because GitHub Actions could not acquire a hosted runner. A rerun reproduced the same external CI acquisition blocker. The repository baseline and project-root boundary checks pass locally; no validator/spec remediation is required.
