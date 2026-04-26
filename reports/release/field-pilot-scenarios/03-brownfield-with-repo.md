# FP-03: Battle brownfield with repo / реальный brownfield с repo

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `passed-on-existing-github-backed-brownfield-repo`
- Execution date: `2026-04-26`
- Repo: `https://github.com/mppcoder/openclaw-brownfield`
- Local checkout: `/projects/openclaw-brownfield`
- Latest pushed commit: `3c026fd`

## Route / маршрут

- Selected profile: `brownfield-with-repo-audit`
- Selected scenario: `brownfield/02-repo-audit.md` + `brownfield/03-as-is-architecture-map.md`
- Pipeline stage: `fp-03-brownfield-with-repo-evidence`
- Handoff allowed: `no`, continuation performed in current Codex session

## Входные условия

- Доступен real existing repo.
- В repo есть хотя бы одна meaningful project-owned area, которую нельзя overwrite.
- Operator может выполнить audit/verify commands или предоставить sanitized command results.

Observed input:

- Existing repo is the reconstructed OpenClaw brownfield repo created during FP-02 and then reused as FP-03 existing repo.
- GitHub repo exists, private, non-empty, default branch `main`.
- Project-owned areas: `src/openclaw-plus/`, `brownfield/`, `runtime-evidence/`, `work/`.
- Template-owned tooling areas: `template-repo/`, `scripts/`, `.chatgpt/`, project shell metadata.

## Ожидаемый результат

- Repo audit summary.
- Change map and risk register.
- Protected project-owned zones identified.
- Conversion path to `greenfield-product` или documented blocker.

## Фактический результат

- Repo audit summary updated in `/projects/openclaw-brownfield/brownfield/repo-audit.md`.
- System inventory updated in `/projects/openclaw-brownfield/brownfield/system-inventory.md`.
- As-is architecture map updated in `/projects/openclaw-brownfield/brownfield/as-is-architecture.md`.
- Change map updated in `/projects/openclaw-brownfield/brownfield/change-map.md`.
- Risk register updated in `/projects/openclaw-brownfield/brownfield/risks-and-constraints.md`.
- Conversion blocker was documented during FP-03; later repo-local readiness remediation converted the project lifecycle to `greenfield-product` / `greenfield-converted` without live runtime mutation.
- Runtime OpenClaw roots were not modified.

## Измеряемые KPI

| KPI | Pass threshold | Result |
|---|---:|---:|
| Project-owned protected zones identified | `100%` known live zones | pass: `src/openclaw-plus/`, `brownfield/`, `runtime-evidence/`, `work/` |
| Audit findings classified | `100%` | pass |
| Template-owned sync candidates separated from manual/advisory changes | yes | pass |
| Critical defects open at closeout | `0` | pass |

## Команды / шаги

1. Прочитать `template-repo/scenario-pack/00-master-router.md`.
2. Запустить guided brownfield-with-repo path:
   `python3 template-repo/scripts/factory-launcher.py --mode brownfield --brownfield-kind modernize --guided --project-name "<real repo>" --project-slug "<slug>" --yes`
3. В pilot repo выполнить project tests и:
   `bash template-repo/scripts/verify-all.sh quick`
4. Создать или обновить audit artifacts: system inventory, repo audit, change map, risks/constraints.
5. Если conversion возможен, записать `greenfield-product` conversion evidence. Если нет, записать blocker.

Executed commands:

```bash
git -C /projects/openclaw-brownfield status --short --branch
git -C /projects/openclaw-brownfield remote -v
gh repo view mppcoder/openclaw-brownfield --json nameWithOwner,url,defaultBranchRef,isEmpty,updatedAt,visibility,description
bash scripts/verify-all.sh
git add brownfield/repo-audit.md brownfield/system-inventory.md brownfield/as-is-architecture.md brownfield/change-map.md brownfield/risks-and-constraints.md
git commit -m "Add FP-03 brownfield repo audit evidence"
git push origin main
```

Command results:

- `bash scripts/verify-all.sh` in `/projects/openclaw-brownfield`: `VERIFY-ALL ПРОЙДЕН (full)`.
- `git status --short --branch`: clean on `main...origin/main`.
- GitHub repo: private, non-empty, default branch `main`.
- Latest pushed audit commit: `3c026fd Add FP-03 brownfield repo audit evidence`.
- Later conversion closeout commit: `1f8fb6d chore: sync post-done follow-up`.

## Pass criteria / критерии прохождения

- Existing repo можно audit без destructive template overwrite.
- Project-owned и template-owned zones разделены.
- Transition завершается conversion evidence или blocker, который можно review.

Status: passed.

## Fail criteria / критерии провала

- Template sync overwrites project-owned files.
- Project не может выполнить meaningful audit/verify step и blocker не записан.
- Critical risk найден без defect capture.

Status: no fail criteria observed.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized repo audit summary.
- Change map и risk register.
- Protected-zone inventory.
- Conversion или blocker summary.

Retained in:

- `https://github.com/mppcoder/openclaw-brownfield` commit `3c026fd`.
- Greenfield conversion closeout retained in `https://github.com/mppcoder/openclaw-brownfield` commit `1f8fb6d`.
- `/projects/openclaw-brownfield/brownfield/repo-audit.md`.
- `/projects/openclaw-brownfield/brownfield/change-map.md`.
- `/projects/openclaw-brownfield/brownfield/risks-and-constraints.md`.
- `/projects/openclaw-brownfield/brownfield/as-is-architecture.md`.
- `/projects/openclaw-brownfield/brownfield/system-inventory.md`.
- `/projects/openclaw-brownfield/greenfield/conversion-readiness.md`.
- `/projects/openclaw-brownfield/.chatgpt/project-owned-zones.yaml`.
