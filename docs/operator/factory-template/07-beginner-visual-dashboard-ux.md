# Beginner visual dashboard UX

Цель beginner visual dashboard — дать оператору короткий readout без web app, daemon, realtime monitoring или отдельной панели.

## Карточка состояния

Минимальная карточка для текущего проекта:

```text
Проект: factory-template
Фаза: execution -> verification
Задача: p9-lifecycle-standards-navigator
Оркестрация: parent executing, child tasks 5/8 done
Стандарты: solo_lightweight, gates 0/9 passed; не хватает security_minimum_checked
Verify: targeted pending
Следующий шаг: заполнить standards evidence и запустить quick verify
```

## Правила

- Показывать standards progress одной строкой.
- Не писать, что проект сертифицирован или compliant, если нет отдельного scoped audit evidence.
- Если `allowed_to_advance_phase=false`, показывать missing evidence, а не зеленую фазу.
- User/manual actions показывать только если они реально нужны сейчас; future-boundary approvals остаются deferred.

## Где это отображается

- `reports/project-lifecycle-dashboard.md` после render.
- `reports/orchestration/orchestration-cockpit.md` для parent/child handoff state.
- Финальный closeout Codex, если есть реальные внешние действия.
