# Сквозной пример change: от intake до done

Этот файл объясняет, как читать готовый демонстрационный пример в папке:

`working-project-examples/example-change-end-to-end/`

## Что показывает пример
Пример показывает полный жизненный цикл одного изменения внутри фабрики:

1. стартовый intake;
2. выбор профиля проекта и профиля изменения;
3. закрытие этапов Reuse / Reality / Conflict;
4. подготовку user spec и tech spec;
5. декомпозицию в task index;
6. создание рабочего change с задачами;
7. verification;
8. done report.

## Как читать пример
Идите по файлам в таком порядке:

1. `.chatgpt/intake.yaml`
2. `.chatgpt/project-profile.yaml`
3. `.chatgpt/policy-status.yaml`
4. `.chatgpt/stage-state.yaml`
5. `.chatgpt/reuse-check.md`
6. `.chatgpt/reality-check.md`
7. `.chatgpt/conflict-report.md`
8. `.chatgpt/evidence-register.md`
9. `.chatgpt/user-spec.md`
10. `.chatgpt/user-spec-validation.md`
11. `.chatgpt/tech-spec.md`
12. `.chatgpt/tech-spec-validation.md`
13. `.chatgpt/task-index.yaml`
14. `work/active/<change-id>/tasks/`
15. `.chatgpt/verification-report.md`
16. `.chatgpt/done-report.md`

## На что смотреть особенно
- как stage-gates меняются по ходу примера;
- как доказательства помечаются тегами `[PROJECT]`, `[FIX]`, `[DOC]`, `[REAL]`, `[ASSUMPTION]`;
- как один change распадается на несколько задач;
- как verification и done завершают цикл.

## Для чего использовать
Этот пример нужен не как шаблон для копирования один в один, а как ориентир по качеству заполнения и по логике связей между файлами.
