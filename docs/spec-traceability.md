# Spec traceability / трассировка спецификации

Этот слой нужен, чтобы технические решения не отрывались от пользовательских требований.

## Короткая модель

- `User Intent Anchors` в `user-spec.md` фиксируют требования как `US-001`, `US-002`, `US-003`.
- `User Intent Binding` в `tech-spec.md` и задачах показывает, на какие `US-*` опирается решение.
- `User-Spec Deviations` фиксирует осознанные отклонения от user-spec.

## Когда писать deviation

Пишите `DEV-*`, если техническое решение:

- сужает обещанный scope;
- меняет критерий приемки;
- переносит часть требования за пределы первой версии;
- выбирает другой путь, чем явно ожидался в user-spec.

Формат записи:

```text
DEV-001 | anchor=US-004 | decision=... | reason=... | validation=...
```

`decision` говорит, что меняем. `reason` объясняет почему. `validation` показывает, как проверим, что отклонение не сломало пользовательскую ценность.

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
- structural drift: исчезла обязательная секция из template или generated artifact.

Это lightweight audit. Он не заменяет review, но быстро показывает, где план потерял связь с исходным пользовательским намерением.
