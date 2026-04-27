# Downstream application proof сценарий

## Назначение

Этот сценарий нужен generated/battle repo, когда placeholder runtime уже недостаточен и нужно доказать deploy настоящего приложения.

`factory-template-placeholder-app:local` остается template-owned reference app для first install, smoke и recovery. Application-level proof начинается только после замены `APP_IMAGE` на реальный image downstream проекта.

## Входные условия

Обязательные внешние inputs:

- downstream repo path;
- real application image;
- approved VPS or staging target;
- secrets entered outside repo;
- approval for deploy, restore and rollback;
- sanitized transcript without secrets.

Если этих inputs нет, stage остается `blocked_external_inputs`, а repo может подготовить только docs/template/checklist evidence.

## Путь от placeholder к real app image

1. Убедиться, что template/runtime path уже healthy с `factory-template-placeholder-app:local`.
2. В downstream repo заменить `APP_IMAGE` на image приложения.
3. Настроить app-specific healthcheck.
4. Выполнить pre-deploy QA и migrations policy.
5. Выполнить approved deploy.
6. Проверить healthcheck.
7. Выполнить backup.
8. Выполнить restore test на disposable/staging target.
9. Выполнить rollback drill.
10. Сохранить sanitized transcript и заполнить report.

## Proof report артефакт

Generated projects use:

```text
reports/release/downstream-application-proof-report.md
```

Template source lives at:

```text
template-repo/template/reports/release/downstream-application-proof-report.md.template
```

Report должен фиксировать:

- app image;
- healthcheck;
- migrations if any;
- backup;
- restore;
- rollback;
- sanitized transcript;
- secrets boundary.

## Novice-to-deploy scorecard проверка

Scorecard answers whether a new operator reached a real deploy without hidden help:

- time-to-first-handoff;
- handoff rework loops;
- manual interventions;
- external blockers;
- deploy result.

`pass` нельзя заявлять без evidence for every runtime gate and every scorecard field.

## Проверка

```bash
python3 template-repo/scripts/validate-downstream-application-proof.py reports/release/downstream-application-proof-report.md
```

Validator accepts blocked/not-run reports only when they do not claim pass and include a blocker reason. A passed report must use a real app image, not `factory-template-placeholder-app:local`, and must include evidence for healthcheck, migrations policy, backup, restore, rollback, sanitized transcript and secrets boundary.

## Boundary правило

This scenario is outside the completed `factory-template` template/runtime proof. It becomes actionable only in a selected downstream/battle project with a real workload.
