# Шаблон lite QA report

Используйте этот template, когда нужен persistent QA note. Держите reports короткими: loop намеренно lightweight.

```markdown
# Lite QA report: <artifact>

Дата: YYYY-MM-DD
Цель проверки: <path>
Тип artifact: skill | prompt-like
Проверяющий: Codex

## Цель
Какое поведение должно улучшиться?

## Кейсы

| Кейс | Prompt / situation | Ожидание | Результат | Notes |
| --- | --- | --- | --- | --- |
| positive-obvious | ... | trigger/use | PASS | ... |
| positive-edge | ... | trigger/use | PASS/FAIL/UNCLEAR | ... |
| negative-adjacent | ... | do not trigger/use | PASS/FAIL/UNCLEAR | ... |
| regression-boundary | ... | preserve boundary | PASS/FAIL/UNCLEAR | ... |

## Находки
- ...

## Примененные улучшения
- ...

## Остаточный риск
- ...
```

Если QA выявляет defect в repo process, до remediation создайте bug report по defect-capture path, который требует task или router.
