# FP-02: Battle brownfield without repo / реальный brownfield без repo

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `field-proven-sanitized`
- Run date: `2026-04-26`
- Real system id: `openclaw-plus-local-vps-sanitized`
- Operator: Codex field run inside `/projects/factory-template`

## Фактический field run

Проверен реальный brownfield без repo с двумя корнями:
- `/root/.openclaw` — live runtime / настроенный дистрибутив.
- `/root/openclaw-plus` — package / overlay / тонкий слой кастомных доработок.

Sanitizing policy:
- значения `/etc/openclaw-plus.env` не переносились;
- `/root/.openclaw/credentials`, `/root/.openclaw/identity`, `/root/.openclaw/telegram`, session logs, sqlite и jsonl state исключены из source reconstruction;
- в repo сохранены только sanitized summaries, allowlist/denylist и evidence notes.

## Фактические команды и evidence

- `sed -n '1,260p' template-repo/scenario-pack/00-master-router.md`
- `git -C /root/.openclaw rev-parse --show-toplevel` -> not a git repo.
- `git -C /root/openclaw-plus rev-parse --show-toplevel` -> not a git repo.
- `systemctl is-active/is-enabled` для `openclaw-gateway`, `openclaw-retrieval`, `openclaw-vectorizer`, `gpt2giga`, `postgresql`, `nginx` -> active/enabled.
- `bash validators/run-final-acceptance.sh` в `/root/openclaw-plus` -> acceptance passed, с warning `duplicated content detected (context bloat)`.
- `find` / `du` inventory для source/generated/runtime/secret-bearing zones.
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
- `brownfield/change-map.md`
- `.chatgpt/evidence-register.md`
- `.chatgpt/reality-check.md`
- `reports/bugs/bug-035-closeout-stopped-before-internal-followup-and-user-instruction.md`
- `reports/factory-feedback/feedback-035-closeout-stopped-before-internal-followup-and-user-instruction.md`

## Измеренные KPI

| KPI | Target | Result |
|---|---:|---:|
| Evidence items inventoried | `>= 1` | passed: roots, services, env inventory, validators, source/generated/runtime zones |
| Unknowns classified | `100% discovered gaps have owner/status` | passed: `brownfield/gap-register.md` |
| Path to repo or blocker | present | passed: create reconstruction workspace under `/projects/<project-root>/...` |
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

Следующий безопасный transition step:
- создать dedicated reconstruction workspace внутри project root, например `/projects/openclaw-brownfield/reconstruction/`;
- собрать redacted source pack по `brownfield/reconstruction-allowlist.md`;
- применить `brownfield/reconstruction-denylist.md`;
- не создавать git repo внутри `/root/.openclaw` или `/root/openclaw-plus`;
- не выполнять runtime remediation до review reconstructed source boundary.

## Остаточные gap / defects

- `GAP-005`: live validator warning `duplicated content detected (context bloat)` требует отдельного runtime quality defect, если scope расширяется до OpenClaw remediation.
- `GAP-006`: secret/runtime state вне repo boundary остается постоянным ограничением reconstruction.
- `GAP-008`: process closeout bug исправлен in factory-template scope.

## Fail criteria / критерии провала

- Scenario не может retain sanitized evidence.
- Process требует unverifiable memory-only reconstruction.
- Gaps найдены, но не captured в `reports/bugs/` или gap register.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized evidence inventory.
- Gap register summary.
- Repo creation/identification plan или blocker.
- Verify result summary, когда repo exists.
