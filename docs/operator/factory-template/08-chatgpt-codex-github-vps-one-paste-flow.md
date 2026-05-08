# One-paste flow: ChatGPT -> Codex -> GitHub -> VPS

## Для кого

Этот guide для пользователя, который хочет делать вайбкод-проект на VPS с ChatGPT, Codex app и GitHub. Не нужно сразу понимать все внутренние файлы шаблона. Достаточно идти по шагам и не вставлять секреты в публичные места.

## Что получится

В результате у вас будет repo с понятной задачей, handoff для Codex, выполненные изменения, verification evidence, PR или closeout, а также dashboard/card со статусом проекта.

## Минимальная схема

ChatGPT формирует задачу и handoff.

Codex читает repo router, выполняет изменения, запускает проверки.

GitHub хранит repo, issues, PR и историю решений.

VPS дает среду выполнения для проекта.

Dashboard показывает статус, blockers и следующий безопасный шаг.

## Сценарий 1. Новичок: задача начинается в ChatGPT

### 1. Сформулировать идею

Что делаем: пишем простыми словами, что хотим получить.
Если начинаете с `goal`, `goal:`, `/goal`, `цель` или `цель:`, ChatGPT Project сначала оформит `goal_contract`: результат, DoD, evidence, scope/non-goals, safety/budget boundaries и proxy-signal denylist.
Это goal-first contract, а не гарантия Codex CLI `/goal`.

Где выполняем: ChatGPT.

Что вставить или какую команду выполнить:

```text
Хочу сделать в проекте <что именно>. Пользователь должен уметь <результат>. Помоги оформить задачу repo-first и подготовить Codex handoff.
```

Ожидаемый результат: ChatGPT уточняет задачу и готовит route-aware handoff.
Если цель достаточно ясна, лишний вопрос не нужен: ChatGPT фиксирует safe defaults и продолжает route.

Если не получилось: добавьте пример желаемого поведения и что сейчас мешает.

### 2. Получить handoff

Что делаем: просим ChatGPT выдать один цельный handoff block.

Где выполняем: ChatGPT.

Что вставить или какую команду выполнить:

```text
Сделай один copy-paste Codex handoff. Обязательно укажи, что Codex должен сначала прочитать template-repo/scenario-pack/00-master-router.md.
```

Ожидаемый результат: один блок текста, который можно вставить в Codex.

Если не получилось: проверьте, что handoff не разбит на несколько отдельных блоков.

### 3. Открыть Codex app или VS Code Remote SSH Codex extension

Что делаем: открываем новую Codex session для этой задачи.

Где выполняем: Codex app или VS Code на VPS через Remote SSH.

Что вставить или какую команду выполнить: вручную выберите нужный model/reasoning в picker, затем откройте новый chat.

Ожидаемый результат: новая чистая Codex session готова принять handoff.

Если не получилось: не используйте старый чат как надежный способ переключения профиля. Откройте новый chat.

Если вы сознательно хотите использовать experimental `goals`, сначала проверьте в Codex terminal:

```bash
codex --version
codex features list
```

Если `goals` есть как experimental/off by default, считайте это рабочим runtime candidate только после явного выбора. Handoff все равно вставляется одним цельным блоком.

### 4. Вставить handoff

Что делаем: вставляем handoff целиком.

Где выполняем: Codex.

Что вставить или какую команду выполнить: вставьте block, который начинается примерно так:

```text
Ты Codex. launch_source=...
```

Ожидаемый результат: Codex читает repo router и отвечает route receipt.

Если не получилось: проверьте, что в handoff есть путь `template-repo/scenario-pack/00-master-router.md`.

### 5. Codex выводит route receipt

Что делаем: смотрим, что Codex понял маршрут.

Где выполняем: Codex.

Что вставить или какую команду выполнить: ничего, дождитесь route receipt.

Ожидаемый результат: видны `selected_project_profile`, `selected_scenario`, `pipeline_stage`, `artifacts_to_update`, `handoff_allowed`, `handoff_shape`.

Если не получилось: остановите задачу и попросите Codex сначала прочитать router.

### 6. Codex обновляет repo и запускает проверки

Что делаем: Codex меняет файлы, запускает validators и собирает evidence.

Где выполняем: Codex на repo/VPS.

Что вставить или какую команду выполнить: обычно Codex сам запускает команды. Минимальная проверка:

```bash
bash template-repo/scripts/verify-all.sh quick
```

Targeted validators для Universal Codex Handoff Factory:

```bash
python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
python3 template-repo/scripts/task-to-codex-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
```

Ожидаемый результат: проверки зеленые или есть понятный blocker.
Tests/validators green являются evidence, но не закрывают goal автоматически: closeout сравнивает evidence с DoD.

Если не получилось: сохраните точный command и первые значимые строки ошибки без секретов.

### 7. Codex готовит PR или closeout

Что делаем: Codex фиксирует результат, dashboard/card и sync status.

Где выполняем: Codex и GitHub.

Что вставить или какую команду выполнить: Codex перед финалом запускает:

```bash
git status --short --branch
```

Ожидаемый результат: финальный ответ содержит что сделано, проверки, actual execution mode, child/subagent count, commit/sync status.

Если не получилось: попросите Codex явно назвать blocker: verify red, нет remote, нет прав push, required human review или конфликт.

### 8. Пользователь делает review только если есть внешний boundary

Что делаем: проверяем только то, что требует человека.

Где выполняем: GitHub UI, VPS, provider UI или local secret manager.

Что вставить или какую команду выполнить: зависит от boundary. Codex должен назвать точное действие.

Ожидаемый результат: без внешнего boundary пользователю ничего делать не нужно.

Если не получилось: не делайте merge/deploy/secret action, пока не понятно, что именно подтверждается.

## Сценарий 1.5. Repo-native task lifecycle без GitHub Issue

Этот сценарий нужен, когда задача уже понятна и вы хотите вести ее через `.chatgpt/task-registry.yaml`, но пока не создаете GitHub Issue.

### 1. Посмотреть следующий номер

Что делаем: проверяем, какой `FT-TASK-NNNN` будет следующим.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/allocate-task-id.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml
```

Ожидаемый результат: команда печатает следующий id и `dry_run=true`.

Если не получилось: сначала проверьте, что registry валиден:

```bash
python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
```

### 2. Добавить draft task

Что делаем: создаем запись задачи в registry.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/allocate-task-id.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --append-draft \
  --title "Add deployment checklist" \
  --goal "Сделать короткий checklist перед deploy на VPS." \
  --task-class docs \
  --source-kind manual \
  --source-ref ""
```

Ожидаемый результат: появляется новый `FT-TASK-NNNN`, а `next_task_number` увеличивается.

Если не получилось: не правьте `FT-CH` или `FT-CX` counters. Для Codex task используется отдельный `FT-TASK`.

### 3. Посмотреть preview

Что делаем: смотрим будущий handoff path, route, dashboard counters и verification commands без запуска Codex.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/preview-task-handoff.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --task-id FT-TASK-0002 \
  --output reports/handoffs/FT-TASK-0002-preview.md
```

Ожидаемый результат: preview markdown создан, Codex не запускался.

Если не получилось: проверьте, что task id существует и route содержит `handoff_shape: codex-task-handoff`.

### 4. Подготовить handoff

Что делаем: генерируем Codex-ready handoff и валидируем его.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/prepare-task-pack.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --dashboard template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --task-id FT-TASK-0002 \
  --write
```

Ожидаемый результат: preview и handoff записаны, handoff прошел validator.

Если не получилось: запустите validator напрямую и сохраните sanitized ошибку:

```bash
python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0002-codex-handoff.md
```

### 5. Разрешить запуск в Codex

Что делаем: явно переводим задачу в `ready_for_codex` и пересчитываем dashboard.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/prepare-task-pack.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --dashboard template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --task-id FT-TASK-0002 \
  --mark-ready-for-codex \
  --sync-dashboard \
  --write
```

Ожидаемый результат: task status стал `ready_for_codex`, dashboard counters обновлены.

Если не получилось: не ставьте зеленый статус вручную. Сначала исправьте validator или добавьте понятный blocker.

### 6. Показать очередь

Что делаем: рендерим read-only список задач для оператора.

Где выполняем: terminal в repo на VPS.

Что вставить или какую команду выполнить:

```bash
python3 template-repo/scripts/render-task-queue.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --output reports/task-queue.md
```

Ожидаемый результат: `reports/task-queue.md` показывает draft/ready/running/human-review задачи и команды подготовки.

Если не получилось: запустите `validate-task-registry.py`; очередь не должна скрывать невалидный registry.

## Сценарий 2. Задача начинается в GitHub Issue

Что делаем: создаем issue через подходящий template: bug, feature, docs, research, audit, release, downstream feedback или curator proposal.

Где выполняем: GitHub.

Что вставить или какую команду выполнить: заполните поля issue. Для логов используйте только sanitized excerpts.

Ожидаемый результат: issue получает label `needs-triage` и class label, например `task:feature`.

Если не получилось: не создавайте blank issue с приватными логами. Вернитесь к template и заполните минимум: цель, expected result, affected layer, context/evidence, Codex involvement.

Repo-native bridge может создать запись в `.chatgpt/task-registry.yaml`, после чего `task-to-codex-handoff.py` соберет handoff.

```bash
python3 template-repo/scripts/issue-to-task-registry.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --issue-file reports/handoffs/example-issue-draft.yaml
```

После этого:

```bash
python3 template-repo/scripts/preview-task-handoff.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --task-id FT-TASK-0002 \
  --output reports/handoffs/FT-TASK-0002-preview.md

python3 template-repo/scripts/prepare-task-pack.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --task-id FT-TASK-0002 \
  --write

python3 template-repo/scripts/render-task-queue.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --output reports/task-queue.md

python3 template-repo/scripts/task-to-codex-handoff.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --task-id FT-TASK-0002 \
  --output reports/handoffs/FT-TASK-0002-codex-handoff.md
```

## Сценарий 3. Задача начинается как maintenance/scheduled item

Что делаем: плановая задача попадает в registry как `maintenance`, `audit`, `release` или `curator`.

Где выполняем: repo script, future runner или ручной triage.

Что вставить или какую команду выполнить: пока MVP без daemon, поэтому scheduled item записывается вручную или через будущий allocator.

Ожидаемый результат: задача имеет `FT-TASK-NNNN`, статус, route и next_action.

Если не получилось: не называйте задачу зеленой. Оставьте `pending`, `draft` или `blocked` с объяснением.

Future automation может делать daily issue triage, release readiness scan и stale task scan, но только с явными boundaries.

## Что нельзя автоматизировать без подтверждения

- ввод или раскрытие secrets;
- public log submission;
- merge, если требуется human review;
- production deploy;
- paid/security-sensitive actions.

## Частые ошибки

- Вставили handoff в старую Codex session и ожидали auto-switch.
- Забыли прочитать `template-repo/scenario-pack/00-master-router.md`.
- Поставили green status без evidence.
- Отправили private logs в public issue.
- Dashboard показывает false green.

## Минимальная команда проверки

```bash
bash template-repo/scripts/verify-all.sh quick
```

Targeted check для handoff factory:

```bash
python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
python3 template-repo/scripts/allocate-task-id.py --registry template-repo/template/.chatgpt/task-registry.yaml
python3 template-repo/scripts/preview-task-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-preview.md
python3 template-repo/scripts/update-task-status.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --status ready_for_handoff --reason "Task route is clear." 
python3 template-repo/scripts/prepare-task-pack.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --write
python3 template-repo/scripts/render-task-queue.py --registry template-repo/template/.chatgpt/task-registry.yaml --output reports/task-queue.md
python3 template-repo/scripts/task-to-codex-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
```
