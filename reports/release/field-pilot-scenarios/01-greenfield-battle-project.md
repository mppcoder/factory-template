# FP-01: Battle greenfield project / реальный greenfield

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `field-proven-sanitized`
- Run date: `2026-04-26`
- Real project id: `greenfield-test`
- GitHub remote: `https://github.com/mppcoder/greenfield-test`
- Latest pushed commit: `cca68d5 Remove generated Python cache from field pilot repo`
- Operator: Codex field run inside `/projects/factory-template`

## Фактический field run

Создан реальный greenfield project:

- local path: `/projects/greenfield-test`
- project preset: `greenfield-product`
- execution mode: `codex-led`
- first feature workspace: `/projects/greenfield-test/work/features/first-feature`
- remote repo: `mppcoder/greenfield-test`

## Фактические команды и evidence

- `sed -n '1,260p' template-repo/scenario-pack/00-master-router.md`
- `python /projects/factory-template/template-repo/scripts/factory-launcher.py --template-repo-root /projects/factory-template/template-repo --mode greenfield --guided --project-name 'Greenfield Test' --project-slug greenfield-test --yes --skip-preflight`
- `bash /projects/greenfield-test/scripts/init-feature-workspace.sh --feature-id first-feature` через guided launcher.
- `python scripts/bootstrap-codex-task.py . --launch-source direct-task --task-class build ...`
- `python scripts/create-codex-task-pack.py .`
- `bash scripts/verify-all.sh` in `/projects/greenfield-test` -> passed.
- `git push -u origin main` -> latest pushed commit `cca68d5`.

## Сохраненные артефакты

- `/projects/greenfield-test/.chatgpt/project-profile.yaml`
- `/projects/greenfield-test/.chatgpt/evidence-register.md`
- `/projects/greenfield-test/.chatgpt/reality-check.md`
- `/projects/greenfield-test/.chatgpt/verification-report.md`
- `/projects/greenfield-test/.chatgpt/done-report.md`
- `/projects/greenfield-test/work/features/first-feature`
- `https://github.com/mppcoder/greenfield-test`

## Измеренные KPI

| KPI | Target | Result |
|---|---:|---:|
| Time to first successful route | `<= 25` minutes target | passed: completed within current field run |
| Manual undocumented interventions | `0` | passed: planned launcher inputs only |
| Required repo-first artifacts present | `100%` | passed: generated repo contains `.chatgpt`, `template-repo`, `AGENTS.md`, routing and task pack |
| Critical defects open at closeout | `0` | passed: no critical FP-01 defect left open |

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

Status: passed.

## Решение по переходу

FP-01 закрыт как greenfield launch-path proof. Следующая работа в `greenfield-test` должна начинаться с реального product scope в `work/features/first-feature`; это не блокирует field-pilot evidence.

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
