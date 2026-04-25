# Spec traceability / трассировка спецификации

Этот слой нужен, чтобы технические решения не отрывались от пользовательских требований.

## Короткая модель

- `user-spec.md` — что хочет пользователь. Он пишется простым языком и фиксирует intent через `US-001`, `US-002`, `US-003`.
- `tech-spec.md` — как агент собирается реализовать это желание. Он обязан показать `User Intent Binding`, то есть связь с `US-*`.
- task-файлы — маленькие шаги реализации. Каждый task должен ссылаться на `US-*` и иметь путь проверки.
- `decisions.md` — что реально решили и проверили после выполнения задач.
- `User-Spec Deviations` — где агент не следует исходному user-spec, почему это допустимо и как это проверить.

## Когда писать deviation

Пишите `DEV-*`, если техническое решение:

- сужает обещанный scope;
- меняет критерий приемки;
- переносит часть требования за пределы первой версии;
- выбирает другой путь, чем явно ожидался в user-spec.

Формат записи:

```text
DEV-001 | anchor=US-004 | decision=... | reason=... | validation=... | approval=pending
```

`decision` говорит, что меняем. `reason` объясняет почему. `validation` показывает, как проверим, что отклонение не сломало пользовательскую ценность.

Если документ переведён в `status: approved`, deviation не должен оставаться `approval=pending`. Утверждённая запись выглядит так:

```text
DEV-001 | anchor=US-004 | decision=... | reason=... | validation=... | approval=approved
```

## Verification path для задач

Task считается готовым к реализации только если понятно, как его проверять:
- `Verify-smoke` — агент может сам запустить команду, тест, validator, local server check или другой быстрый smoke.
- `Verify-user` — пользователь должен глазами или вручную подтвердить UI/поведение/результат.

Для простой внутренней задачи достаточно короткой smoke-проверки вроде "запустить validator" или "проверить, что task закрывает primary `US-*`".

## Validator / проверка

Проверить factory templates и сгенерированные workspaces:

```bash
python3 template-repo/scripts/validate-spec-traceability.py
```

Этот validator входит в:

```bash
bash template-repo/scripts/verify-all.sh quick
bash template-repo/scripts/verify-all.sh ci
```

Проверить конкретную feature:

```bash
python3 template-repo/scripts/validate-spec-traceability.py --workspace template-repo/work/features/feat-my-first-flow
```

Validator ловит:

- missing trace: tech-spec или task не ссылается на `US-*`;
- undocumented deviation: найден сигнал отклонения без `DEV-*` record или record без `anchor/reason/validation`;
- unapproved deviation: approved документ содержит pending deviation;
- missing verification: task не содержит `Verify-smoke`, `Verify-user` или другой понятный путь проверки;
- structural drift: исчезла обязательная секция из template или generated artifact.

Это lightweight audit. Он не заменяет review, но быстро показывает, где план потерял связь с исходным пользовательским намерением.
