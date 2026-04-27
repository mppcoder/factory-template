# Легкий task-state слой

`task-state-lite` добавляет один компактный YAML-файл для ответа на вопрос: где сейчас задача, кто владеет следующим шагом и что блокирует движение.

Это не Kanban UI, не daemon и не runtime service. Beginner path остается прежним: маленькая задача может идти через обычные `.chatgpt` artifacts и handoff. `task-state-lite` нужен, когда важно быстро восстановить состояние между сессиями или не смешать internal work, external user action, downstream sync и runtime backlog.

## Артефакт

Канонический путь в generated/battle project:

```text
.chatgpt/task-state.yaml
```

Source-of-truth в `factory-template`:

```text
template-repo/template/.chatgpt/task-state.yaml
```

Не добавляйте root-level `.chatgpt/task-state.yaml` в `factory-template` для этой feature: root `.chatgpt/` в factory repo используется для factory-level task artifacts, а template source живет под `template-repo/template/`.

Минимальные поля:

- `schema`: `task-state-lite/v1`;
- `current_state`: `intake`, `planning`, `ready_for_handoff`, `in_progress`, `blocked`, `external_wait`, `verify` или `done`;
- `owner_boundary`: `internal_repo`, `external_user`, `external_runtime`, `downstream_sync` или `mixed`;
- `next_action.type`: `internal`, `external`, `blocked`, `verify` или `none`;
- `next_action.summary`: конкретный следующий шаг;
- `blocked.status`: `true` или `false`;
- `blocked.reason`: причина блокировки или `not_required`;
- `boundaries`: отдельные списки для internal work, external user actions, external runtime и downstream sync.

## Границы

- `internal_work` — то, что Codex может сделать внутри repo.
- `external_user_actions` — ручные решения, approvals, UI-действия или ввод секретов.
- `external_runtime` — VPS, production deploy, restore, rollback и runtime transcript.
- `downstream_sync` — controlled sync в downstream/battle repo.

Если `current_state: done`, `next_action.type` должен быть `none` или `verify`, а `blocked.status` должен быть `false`.

Если `current_state: blocked`, `blocked.status` должен быть `true` и `blocked.reason` должен быть заполнен.

## Проверка

```bash
python3 template-repo/scripts/validate-task-state-lite.py .
```

Quick verify запускает этот validator для factory root и для generated projects. Validator проверяет только структуру и честность boundary-разделения; он не требует advanced execution для маленьких задач.

## Почему отдельный файл

`task-index.yaml` остается графом изменения и задач. `task-state.yaml` хранит текущий operational state: владелец следующего шага, блокеры и boundary-разделение. Это снижает риск stale commit metadata и не перегружает task graph дополнительной runtime-семантикой.
