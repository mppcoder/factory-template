# Factory feedback 034: spec-governance traceability gap

Дата: 2026-04-25
Источник: `reports/bugs/2026-04-25-spec-governance-gap.md`
Слой: `factory-template`
Статус: remediation in progress

## Суть

Feature planning flow должен оставаться понятным новичку, но ему не хватает нескольких lightweight governance anchors:
- decision log для завершённых задач;
- явные task verification anchors;
- approval-aware deviations;
- final verification / audit-lite section в tech-spec;
- validator checks для gaps, которые реально ломают traceability.

## Требование к исправлению

Решение не должно копировать тяжёлую multi-agent методологию целиком. Нужно адаптировать только минимальные идеи:
- user-spec описывает исходное желание пользователя;
- tech-spec объясняет, как агент реализует это желание;
- deviation явно показывает, где агент не следует исходному intent и почему;
- decisions log сохраняет важные решения после выполнения;
- task не считается готовой без понятного пути проверки.

## Ожидаемый устойчивый результат

Fresh scaffold и downstream template sync получают beginner-safe planning flow без обязательной профессиональной audit/reviewer инфраструктуры.

