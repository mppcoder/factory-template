# Universal Task Control: downstream sync для существующих проектов

## Назначение

Этот документ описывает, как переносить обновления Universal Task Control в уже существующий downstream project, который был создан из `factory-template` раньше.

Главное правило: `.chatgpt/task-registry.yaml` нельзя слепо перезаписывать. В нем могут жить реальные пользовательские задачи, evidence, статусы, blockers и external-action boundaries.

## Что можно обновлять напрямую

При sync можно заменять или добавлять эти файлы, если downstream repo не менял их локально:

- `scripts/validate-task-registry.py`
- `scripts/allocate-task-id.py`
- `scripts/issue-to-task-registry.py`
- `scripts/preview-task-handoff.py`
- `scripts/prepare-task-pack.py`
- `scripts/render-task-queue.py`
- `scripts/task-to-codex-handoff.py`
- `scripts/update-task-status.py`
- `scripts/validate-codex-task-handoff.py`
- `scripts/task_control_paths.py`
- `.github/ISSUE_TEMPLATE/*.yml`
- `docs/operator/universal-task-control.md`

Если downstream repo менял эти файлы, делайте обычный review diff и сохраняйте локальные project-specific изменения.

## Что нельзя перезаписывать blind-copy

Нельзя blind-copy:

- `.chatgpt/task-registry.yaml`
- `.chatgpt/project-lifecycle-dashboard.yaml`, если в нем уже есть реальные counters/evidence
- `reports/handoffs/*`
- `reports/task-queue.md`, если он используется как локальный evidence snapshot

## Safe sync порядок

1. Создать clean branch в downstream repo.
2. Скопировать новые scripts/docs/Issue Forms.
3. Запустить:

```bash
python3 scripts/validate-task-registry.py .chatgpt/task-registry.yaml
python3 scripts/render-task-queue.py --registry .chatgpt/task-registry.yaml --output reports/task-queue.md
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
```

4. Если dashboard не содержит Universal Task Control, добавить section migration-style:

```yaml
universal_task_control:
  status: pending
  registry_path: .chatgpt/task-registry.yaml
  open_tasks: 0
  ready_for_handoff: 0
  ready_for_codex: 0
  codex_running: 0
  human_review: 0
  blocked: 0
  verified: 0
  next_action: Generate or update Codex handoff for the next ready task.
  fallback_next_action: Keep task in triage until route, evidence and human boundary are clear.
  evidence:
    - .chatgpt/task-registry.yaml
    - scripts/validate-task-registry.py
    - scripts/allocate-task-id.py
    - scripts/issue-to-task-registry.py
    - scripts/preview-task-handoff.py
    - scripts/update-task-status.py
    - scripts/prepare-task-pack.py
    - scripts/render-task-queue.py
    - reports/task-queue.md
```

5. Если registry schema lacks a new allowed class/status, add only the missing enum values and keep:

- `tasks`
- `next_task_number`
- `evidence`
- `last_status_change`
- `human_boundary`
- `dependencies`

6. Запустить generated smoke на временной копии downstream repo или temporary generated project.
7. Записать sync report в `reports/`, если менялись `.chatgpt/*` semantics.

## Registry merge rule

Допустимый registry migration:

- preserve all existing tasks as-is;
- preserve `next_task_number` unless recomputing upward is required because existing task ids exceed it;
- add new `allowed_classes` or `allowed_statuses` only append-style;
- do not rewrite task ids;
- do not erase evidence, accepted reasons, blockers or status history;
- do not change `human_boundary.external_user_action` from `true` to `false` automatically.

Если merge tool не может уверенно сохранить эти поля, остановитесь и создайте manual migration report.

## Verification evidence

Минимальный green contour после sync:

```bash
python3 scripts/validate-task-registry.py .chatgpt/task-registry.yaml
python3 scripts/allocate-task-id.py --registry .chatgpt/task-registry.yaml
python3 scripts/render-task-queue.py --registry .chatgpt/task-registry.yaml --output reports/task-queue.md
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
```

Для полной проверки используйте downstream temporary smoke: append draft -> `ready_for_handoff` -> preview -> prepare pack -> `ready_for_codex` -> validate generated handoff -> render queue -> dashboard validation.
