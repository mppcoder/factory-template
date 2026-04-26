# FP-02: Battle brownfield without repo / реальный brownfield без repo

## Статус

- Current status: `pending`
- Evidence class: field pilot
- Result: `no-field-evidence`

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

## Fail criteria / критерии провала

- Scenario не может retain sanitized evidence.
- Process требует unverifiable memory-only reconstruction.
- Gaps найдены, но не captured в `reports/bugs/` или gap register.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized evidence inventory.
- Gap register summary.
- Repo creation/identification plan или blocker.
- Verify result summary, когда repo exists.
