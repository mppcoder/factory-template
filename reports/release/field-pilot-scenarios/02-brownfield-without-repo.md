# FP-02: Battle brownfield without repo / реальный brownfield без repo

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `field-proven-sanitized`
- Run date: `2026-04-26`
- Real system id: `openclaw-plus-local-vps-sanitized`
- Operator: Codex field run inside `/projects/factory-template`
- Created project repo: `/projects/openclaw-brownfield`
- Project repo commit: `4a58c8d Initial sanitized OpenClaw brownfield repo`
- GitHub remote: `https://github.com/mppcoder/openclaw-brownfield`
- Latest pushed commit: `7b3d1a4 Publish OpenClaw brownfield repo and fix generated verify`

## Фактический field run

Проверен реальный brownfield без repo с двумя корнями:
- `/root/.openclaw` — live runtime / настроенный дистрибутив.
- `/root/openclaw-plus` — package / overlay / тонкий слой кастомных доработок.

Sanitizing policy:
- значения `/etc/openclaw-plus.env` не переносились;
- `/root/.openclaw/credentials`, `/root/.openclaw/identity`, `/root/.openclaw/telegram`, session logs, sqlite и jsonl state исключены из source reconstruction;
- в repo сохранены только sanitized summaries, allowlist/denylist и evidence notes.

Фактический repo boundary:
- `/projects/openclaw-brownfield` создан через factory launcher как project root.
- `/projects/openclaw-brownfield/src/openclaw-plus` содержит sanitized source layer из `/root/openclaw-plus`.
- `/projects/openclaw-brownfield/runtime-evidence/openclaw-plus-env.inventory.md` содержит только redacted inventory имен переменных.
- `/projects/openclaw-brownfield` запушен в `https://github.com/mppcoder/openclaw-brownfield`.
- raw `/root/.openclaw` не копировался.

## Фактические команды и evidence

- `sed -n '1,260p' template-repo/scenario-pack/00-master-router.md`
- `git -C /root/.openclaw rev-parse --show-toplevel` -> not a git repo.
- `git -C /root/openclaw-plus rev-parse --show-toplevel` -> not a git repo.
- `systemctl is-active/is-enabled` для `openclaw-gateway`, `openclaw-retrieval`, `openclaw-vectorizer`, `gpt2giga`, `postgresql`, `nginx` -> active/enabled.
- `bash validators/run-final-acceptance.sh` в `/root/openclaw-plus` -> acceptance passed, с warning `duplicated content detected (context bloat)`.
- `find` / `du` inventory для source/generated/runtime/secret-bearing zones.
- `python /projects/factory-template/template-repo/scripts/factory-launcher.py --template-repo-root /projects/factory-template/template-repo --mode brownfield --brownfield-kind no-repo --guided --project-name 'OpenClaw Brownfield' --project-slug openclaw-brownfield --yes --skip-preflight` -> created `/projects/openclaw-brownfield`.
- `rsync` source reconstruction из `/root/openclaw-plus` в `/projects/openclaw-brownfield/src/openclaw-plus` с denylist для `.venvs`, `venv`, `node_modules`, `__pycache__`, `var`, logs, backups и `wrappers/docs/*.txt`.
- `git -C /projects/openclaw-brownfield commit -m 'Initial sanitized OpenClaw brownfield repo'` -> `4a58c8d`.
- `gh repo create mppcoder/openclaw-brownfield --private --source=. --remote=origin --push` -> created `https://github.com/mppcoder/openclaw-brownfield`.
- `git -C /projects/openclaw-brownfield push origin main` -> latest pushed commit `7b3d1a4`.
- Targeted project validators in `/projects/openclaw-brownfield`: `validate-brownfield-transition.py`, `validate-evidence.py`, `validate-codex-task-pack.py` -> passed.
- `bash scripts/verify-all.sh` in `/projects/openclaw-brownfield` -> passed after `bug-038` remediation.
- `bash template-repo/scripts/verify-all.sh` в `factory-template` -> full pass после сохранения evidence.

## Сохраненные артефакты

- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `brownfield/reverse-engineering-plan.md`
- `brownfield/reverse-engineering-summary.md`
- `brownfield/source-candidate-map.md`
- `brownfield/reconstruction-allowlist.md`
- `brownfield/reconstruction-denylist.md`
- `brownfield/reconstruction-repo-report.md`
- `brownfield/change-map.md`
- `.chatgpt/evidence-register.md`
- `.chatgpt/reality-check.md`
- `reports/bugs/bug-035-closeout-stopped-before-internal-followup-and-user-instruction.md`
- `reports/factory-feedback/feedback-035-closeout-stopped-before-internal-followup-and-user-instruction.md`
- `reports/bugs/bug-036-fp02-marked-passed-before-repo-creation.md`
- `reports/factory-feedback/feedback-036-fp02-marked-passed-before-repo-creation.md`
- `reports/bugs/bug-037-github-repo-creation-misclassified-as-user-step.md`
- `reports/factory-feedback/feedback-037-github-repo-creation-misclassified-as-user-step.md`
- `reports/bugs/bug-038-generated-project-root-script-verify-all-wrong-root.md`
- `reports/factory-feedback/feedback-038-generated-project-root-script-verify-all-wrong-root.md`
- `/projects/openclaw-brownfield` GitHub-backed repo, latest pushed commit `7b3d1a4`

## Измеренные KPI

| KPI | Target | Result |
|---|---:|---:|
| Evidence items inventoried | `>= 1` | passed: roots, services, env inventory, validators, source/generated/runtime zones |
| Unknowns classified | `100% discovered gaps have owner/status` | passed: `brownfield/gap-register.md` |
| Path to repo or blocker | present | passed: created and pushed `https://github.com/mppcoder/openclaw-brownfield`, commit `7b3d1a4` |
| Critical defects open at closeout | `0` | passed: no open critical; reusable closeout defect fixed as `bug-035` |

## Входные условия

- Есть реальная existing system, но canonical repo на старте пилота отсутствует.
- Evidence может включать файлы, notes, screenshots, deployment details или operator descriptions.
- Sensitive details sanitizing выполняется до commit evidence.

## Ожидаемый результат

- Brownfield-without-repo intake/reconstruction package.
- Evidence inventory и gap register.
- Documented path к созданию/поиску canonical repo или blocker, почему это пока невозможно.
- Transition plan toward `greenfield-product`.

## Измеряемые KPI

| KPI | Pass threshold |
|---|---:|
| Evidence items inventoried | `>= 1` real evidence source |
| Unknowns classified | `100%` discovered gaps have owner/status |
| Path to repo or blocker | present |
| Critical defects open at closeout | `0` |

## Команды / шаги

1. Прочитать `template-repo/scenario-pack/00-master-router.md`.
2. Запустить guided brownfield no-repo path:
   `python3 template-repo/scripts/factory-launcher.py --mode brownfield --brownfield-kind no-repo --guided --project-name "<real system>" --project-slug "<slug>" --yes`
3. Заполнить или summary-зафиксировать `brownfield/system-inventory.md`, `brownfield/gap-register.md` и reconstruction notes в field evidence package.
4. Когда repo доступен, выполнить:
   `bash template-repo/scripts/verify-all.sh quick`
5. Для каждого tool/process gap создать defect report до remediation.

## Pass criteria / критерии прохождения

- No-repo system представлен repo-controlled evidence без притворства, что repo уже существовал.
- Следующий transition step explicit: create repo, identify repo или accept blocker.
- Brownfield evidence защищён и не overwritten template sync.

Status: passed.

## Решение по переходу

Безопасный transition step выполнен:
- dedicated project repo создан в `/projects/openclaw-brownfield`;
- GitHub repo создан и подключен как `origin`;
- redacted source pack собран в `src/openclaw-plus`;
- denylist применен;
- git repo внутри `/root/.openclaw` или `/root/openclaw-plus` не создавался;
- runtime remediation не выполнялась.

## Остаточные gap / defects

- `GAP-005`: live validator warning `duplicated content detected (context bloat)` требует отдельного runtime quality defect, если scope расширяется до OpenClaw remediation.
- `GAP-006`: secret/runtime state вне repo boundary остается постоянным ограничением reconstruction.
- `GAP-008`: process closeout bug исправлен in factory-template scope.
- `GAP-009`: FP-02 был преждевременно помечен `passed` до repo creation; исправлено созданием `/projects/openclaw-brownfield`, commit `4a58c8d`.
- `GAP-010`: GitHub repo creation был ошибочно оставлен пользователю; исправлено созданием remote `mppcoder/openclaw-brownfield`.
- `GAP-011`: generated `scripts/verify-all.sh` неверно вычислял root; исправлено, verify проходит в project repo.

## Fail criteria / критерии провала

- Scenario не может retain sanitized evidence.
- Process требует unverifiable memory-only reconstruction.
- Gaps найдены, но не captured в `reports/bugs/` или gap register.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized evidence inventory.
- Gap register summary.
- Created project repo path и commit hash.
- Verify result summary, когда repo exists.
