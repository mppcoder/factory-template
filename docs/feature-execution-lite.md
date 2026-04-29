# Лёгкое выполнение фичи

`feature-execution-lite` — это optional advanced path для больших фич, где одной линейной задачи уже мало. Beginner path остаётся прежним: `init-feature-workspace.sh` → интервью → `user-spec` → `tech-spec` → маленькие задачи → обычный handoff.

Продвинутый path включается только явно, когда нужны волны задач, checkpoint/resume и более строгий closeout.

## Когда использовать

Используйте этот режим, если:

- задач больше трёх и часть можно делать независимо;
- есть риск потерять состояние между сессиями;
- нужны audit/reviewer hints;
- есть внутренние проверки, внешние действия пользователя и runtime backlog, которые нельзя смешивать;
- feature нельзя закрывать без финальной verification evidence.

Не используйте режим по умолчанию для первой маленькой feature или простого bugfix.

## Принцип dispatcher-not-doer

Для Codex это не означает обязательную команду агентов. В этом repo правило звучит проще:

- dispatcher держит план, волны, checkpoint и decisions;
- исполнитель задачи работает только в scope конкретной задачи;
- после каждой волны обновляются task statuses, `decisions.md` и `logs/checkpoint.yaml`;
- dispatcher не закрывает feature, пока final verification не зафиксирована;
- если после максимального числа review/fix rounds остаются findings, работа останавливается и эскалируется пользователю.

В текущей live-сессии Codex может физически выполнять задачи сам, если пользователь не запускал отдельные sub-agents. Но артефакты всё равно должны разделять coordination state и implementation details.

## Артефакты workspace

Advanced workspace добавляет:

- `logs/execution-plan.md` — план волн, зависимостей, проверок и границ;
- `logs/checkpoint.yaml` — состояние resume, текущая волна, статусы задач, final verification;
- `decisions.md` — журнал решений, deviations, verification evidence и escalation entries;
- `tasks/T-xxx.md` — задачи с `wave`, `status`, `depends_on`, `verify`, `reviewers` и `reviewer_hints`.

Создать advanced workspace:

```bash
bash template-repo/scripts/init-feature-workspace.sh --feature-id feat-example --title "Example" --advanced-execution
```

Проверить advanced artifacts:

```bash
python3 template-repo/scripts/validate-feature-execution-lite.py --workspace template-repo/work/features/feat-example --require-advanced
```

## Волны задач

`wave` группирует задачи, которые можно делать независимо. Простое правило:

- задача без dependencies может быть в первой волне;
- задача с `depends_on` должна быть в более поздней волне, чем все её зависимости;
- задача в `done` не считается закрытой без `Verify-smoke` или явного `Verify-user`;
- финальная волна должна включать audit/final verification task или отдельную запись в checkpoint.

## Checkpoint и resume

После каждой волны обновляйте `logs/checkpoint.yaml`:

- `last_completed_wave`;
- `next_wave`;
- `tasks.<task_id>.status`;
- `tasks.<task_id>.verify_smoke`;
- `tasks.<task_id>.verify_user`;
- `decisions_updated`;
- `internal_work_remaining`, `external_user_action_required`, `runtime_backlog`.

Resume начинается не с памяти чата, а с repo artifacts: `checkpoint.yaml`, `execution-plan.md`, task frontmatter и `decisions.md`.

## Журнал решений

`decisions.md` хранит только полезную память:

- что было решено и почему;
- какие deviations появились;
- какие проверки реально выполнены;
- какие findings ушли в backlog;
- где нужен user approval.

Не копируйте туда полный diff, длинные логи тестов или весь review report.

## Раунды review/fix

Для рискованных задач укажите reviewer hints. По умолчанию максимум `3` review/fix rounds:

- `1` — быстрый feedback;
- `2` — проверка исправлений;
- `3` — последняя попытка перед эскалацией.

Если после `max_review_rounds` остаются findings, не закрывайте задачу как done. Запишите escalation в `decisions.md`, отметьте blocker в checkpoint и попросите пользовательское решение.

## Финальное закрытие и архив

Feature можно архивировать в `work/completed/` только если:

- все задачи в checkpoint имеют `done`;
- `final_verification.status: passed`;
- `decisions.md` обновлён;
- internal work, external user action и runtime backlog явно разделены;
- runtime backlog не замаскирован как выполненная работа.

Если live runtime remediation не входила в scope, она должна остаться отдельным runtime backlog, а не evidence overclaim.

## Отображение в lifecycle dashboard

Для сложной многоэтапной feature `project-lifecycle-dashboard` должен показывать состояние без чтения всех файлов workspace вручную:

- `current_wave`;
- completed tasks;
- blocked tasks;
- next task;
- `final_verification.status`;
- можно ли архивировать feature в `work/completed/`.

Dashboard не заменяет `logs/checkpoint.yaml`, `execution-plan.md`, `decisions.md` и task files. Он агрегирует их как operator-facing summary. Если задача или wave отмечена `done/passed/completed`, у нее должен быть evidence artifact или accepted reason; иначе validator считает это false green.

Если `final_verification.status` не `passed`, dashboard обязан показывать archive blocker, даже если отдельные задачи уже выполнены.

## Связь со standards navigator

Для больших фич `feature-execution-lite` должен обновлять не только task/wave state, но и standards evidence:

- если фича меняет user-facing UI, обновить `accessibility_minimum_checked`;
- если фича меняет auth, payments, data, deploy или network boundary, обновить `security_minimum_checked` и при web app scope `web_security_checked`;
- если фича добавляет AI model calls, agents, tool use или high-impact AI outputs, включить `ai_safety_gate`;
- если фича готовит commercial/production release, перейти с `solo_lightweight` на `commercial_production` или записать future-boundary blocker.

Закрытие feature как `done` без final verification и без актуального standards gate evidence считается false green.

## Связанные файлы

- `template-repo/template/work-templates/execution-plan.md.template`
- `template-repo/template/work-templates/checkpoint.yaml.template`
- `template-repo/template/work-templates/tasks/task.md.template`
- `template-repo/template/work-templates/decisions.md.template`
- `template-repo/scripts/init-feature-workspace.sh`
- `template-repo/scripts/validate-feature-execution-lite.py`
