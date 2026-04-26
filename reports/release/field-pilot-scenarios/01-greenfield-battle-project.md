# FP-01: Battle greenfield project / реальный greenfield

## Статус

- Current status: `pending`
- Evidence class: field pilot
- Result: `no-field-evidence`

## Входные условия

- Выбран реальный новый product/project.
- Operator может сохранить прямые repo evidence или sanitized evidence.
- Run начинается с чтения `template-repo/scenario-pack/00-master-router.md`.
- Synthetic fixture не используется как field project.

## Ожидаемый результат

- Generated или initialized greenfield project с repo-first instructions.
- Active profile equivalent to `greenfield-product`.
- First task workspace или documented reason, почему first task не стартовал.
- Verify summary для generated project.

## Измеряемые KPI

| KPI | Pass threshold |
|---|---:|
| Time to first successful route | target `<= 25` minutes, measured honestly even if exceeded |
| Manual undocumented interventions | `0` |
| Required repo-first artifacts present | `100%` |
| Critical defects open at closeout | `0` |

## Команды / шаги

1. Прочитать `template-repo/scenario-pack/00-master-router.md`.
2. Запустить guided greenfield path:
   `python3 template-repo/scripts/factory-launcher.py --mode greenfield --guided --project-name "<real project>" --project-slug "<slug>" --yes`
3. В generated project выполнить:
   `bash template-repo/scripts/verify-all.sh quick`
4. Зафиксировать timing, manual interventions, verify result и retained artifacts.
5. Если найден defect, создать `reports/bugs/YYYY-MM-DD-field-pilot-greenfield-<slug>.md` до remediation.

## Pass criteria / критерии прохождения

- Project может продолжать работу по repo-first rules без operator guessing.
- Required project knowledge и `.chatgpt`/scenario-pack artifacts существуют.
- Quick verify проходит или каждый failure имеет linked accepted blocker.
- Synthetic smoke artifact не цитируется как field result.

## Fail criteria / критерии провала

- Field project нельзя создать или initialized.
- First task route требует undocumented manual recovery.
- Repo-first instructions отсутствуют или не materialized.
- Critical defect остаётся open.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized project profile и route summary.
- Timing and intervention notes.
- Verify command/result summary.
- Defect links, если есть.
