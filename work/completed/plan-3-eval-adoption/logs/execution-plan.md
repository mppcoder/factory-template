# План выполнения Lite: Plan 3 Artifact Eval Adoption

> generated_at: 2026-04-27T12:21:06+03:00
> feature_id: plan-3-eval-adoption
> mode: optional-advanced
> max_review_rounds: 3

Этот план нужен только для advanced feature execution. Для beginner path достаточно `tech-spec.md`, task files и обычной проверки traceability.

## Граница роли dispatcher

- dispatcher ведёт план, checkpoint, decisions и handoff;
- implementation work выполняется внутри task scope;
- dispatcher не закрывает feature без final verification;
- internal work, external user action и runtime backlog фиксируются отдельно.

## Волны

<!--
### Wave 1 — независимые задачи

- tasks: [T-001, T-002]
- depends_on: []
- goal: что должна дать волна
- verify_smoke: команды или validator checks
- verify_user: что показать пользователю или `Не требуется`
- reviewer_hints: code/security/test/docs или `Не требуется`
-->

### Wave 1 — Artifact Eval expansion

- tasks: [T-001]
- depends_on: []
- goal: расширить specs/reports на routing-critical артефакты и negative fixtures.
- verify_smoke: `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/*.md`
- verify_user: Не требуется
- reviewer_hints: docs/eval boundary, source hygiene, overclaim checks

### Wave 2 — Feature adoption closeout evidence

- tasks: [T-002]
- depends_on: [T-001]
- goal: закрыть изменение через advanced feature-execution-lite workspace и release-facing status.
- verify_smoke: `python3 template-repo/scripts/validate-feature-execution-lite.py --workspace work/features/plan-3-eval-adoption --require-advanced`
- verify_user: Не требуется
- reviewer_hints: closeout docs, Project Knowledge proposal, downstream-impact

## Проверки пользователя

Не требуются для repo-local P3-S3/P3-S4. Внешний runtime approval относится только к P3-S5.

## Audit и final wave

Перед closeout:

- убедиться, что final verification passed в checkpoint;
- провести closeout через `close-feature-workspace.py`;
- проверить closed workspace через Project Knowledge validator;
- запустить quick verify и sync.

## Правило эскалации

- max_review_rounds: 3
- after_max_rounds: остановить закрытие задачи, записать escalation в `decisions.md`, обновить `logs/checkpoint.yaml`, запросить решение пользователя.
- blocker_policy: не смешивать internal work, external user action и runtime backlog.

## Чеклист закрытия

- [x] Все wave dependencies выполнены в правильном порядке.
- [x] `decisions.md` содержит записи по важным решениям, deviations и verification.
- [x] `logs/checkpoint.yaml` обновлён после последней волны.
- [x] `final_verification.status` равен `passed`.
- [x] Runtime backlog, если есть, явно отделён от выполненной repo-local работы.
