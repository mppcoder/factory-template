# Дефект: лёгкий spec-governance слой не закрывает traceability до задач

Дата: 2026-04-25
Слой: `factory-template`
Статус: remediation in progress

## Контекст

В шаблоне уже есть базовые секции `User Intent Anchors`, `User Intent Binding` и `User-Spec Deviations`, но они не доводят цепочку до полного beginner-safe governance flow.

## Наблюдение

- Нет `decisions.md.template`, хотя завершение feature должно сохранять решения, отклонения и проверки после выполнения задач.
- Task template не фиксирует явный verification path через `Verify-smoke` / `Verify-user`.
- Tech-spec template не содержит лёгких секций `Decisions`, `Acceptance Criteria`, `Audit Wave Lite` и `Final Verification`.
- Validator проверяет только базовые anchors/deviations и не ловит approved docs с pending deviations или task без проверки.
- Документация объясняет traceability, но недостаточно ясно разделяет `user-spec = что хочет пользователь`, `tech-spec = как агент делает`, `deviation = где агент осознанно не следует исходному intent`.

## Риск

Downstream-проект может выглядеть формально подготовленным, но:
- решение потеряет связь с исходным пользовательским намерением;
- deviation останется неутвержденным после approval;
- задача будет реализована без понятного smoke/user verification path;
- завершение feature не сохранит decisions для будущего Project Knowledge.

## Классификация

- `project-only`: нет
- `factory-template`: да
- `shared/unknown`: нет

## Remediation

В текущем scope нужно:
- добавить `decisions.md.template`;
- расширить tech/task templates без профессионального перегруза;
- обновить генераторы `generate-user-spec.py` и `decompose-feature.py`;
- усилить `validate-spec-traceability.py`;
- обновить docs и project-knowledge;
- подтвердить `bash template-repo/scripts/verify-all.sh ci`.

