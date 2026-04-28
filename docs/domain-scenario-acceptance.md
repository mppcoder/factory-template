# Domain scenario acceptance для novice flow

## Назначение

Этот template расширяет novice acceptance beyond parity smoke без требования real downstream app.

Parity smoke отвечает на вопрос: "может ли новичок пройти canonical launcher flow". Domain scenario acceptance отвечает на вопрос: "понятно ли новичку, как выразить предметную задачу и получить проверяемый результат в generated project".

## Граница

- Real downstream field pilot остается future external contour.
- Real `APP_IMAGE`, production deploy и real business workload proof не требуются для Plan №5.
- Domain examples ниже являются repo-local acceptance templates, а не evidence of a real downstream/battle system.

## Шаблон

```yaml
schema: domain-scenario-acceptance/v1
id: <domain-scenario-id>
domain: <crm|inventory|support|analytics|other>
persona: novice operator
entry_mode: greenfield-product
user_goal: "<short domain goal>"
expected_artifacts:
  - PROJECT_BRIEF.md
  - .chatgpt/user-spec.md
  - .chatgpt/tech-spec.md
  - work/features/<feature-id>/tasks/
acceptance:
  - user intent is preserved in user-spec
  - technical plan maps domain terms to implementation tasks
  - external/runtime/downstream boundaries are explicit
  - no secrets or real customer data in fixtures
field_pilot_boundary: future_external
```

## Пример CRM follow-up queue

```yaml
schema: domain-scenario-acceptance/v1
id: crm-follow-up-queue
domain: crm
persona: novice operator
entry_mode: greenfield-product
user_goal: "Создать backlog для follow-up очереди клиентов с due dates and priority."
expected_artifacts:
  - PROJECT_BRIEF.md
  - .chatgpt/user-spec.md
  - .chatgpt/tech-spec.md
  - work/features/crm-follow-up-queue/tasks/
acceptance:
  - user-spec names customer, due date, owner and priority terms
  - tech-spec separates data model, UI list and notification boundary
  - runtime/email integration is marked external until credentials exist
  - fixtures contain synthetic customer names only
field_pilot_boundary: future_external
```

## Пример inventory reorder review

```yaml
schema: domain-scenario-acceptance/v1
id: inventory-reorder-review
domain: inventory
persona: novice operator
entry_mode: greenfield-product
user_goal: "Собрать сценарий контроля товаров ниже reorder point."
expected_artifacts:
  - PROJECT_BRIEF.md
  - .chatgpt/user-spec.md
  - .chatgpt/tech-spec.md
  - work/features/inventory-reorder-review/tasks/
acceptance:
  - user-spec explains SKU, current stock, reorder point and supplier boundary
  - tech-spec creates validation tasks without real supplier credentials
  - acceptance distinguishes repo-local fixture and future external ERP integration
  - no real inventory export or customer data is committed
field_pilot_boundary: future_external
```
