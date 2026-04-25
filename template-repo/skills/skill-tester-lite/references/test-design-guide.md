# Guide по test design

Используйте этот guide для optional advanced QA loop:

```text
create -> test -> improve trigger/usefulness
```

Loop нужен для улучшения самого factory-template. Это не обязательный шаг для новичков, использующих template.

## Test surface / поверхность проверки

Тестируйте только surface, важный для reuse:

- trigger fit: when the skill or prompt should activate;
- trigger rejection: when it should stay silent;
- usefulness: what behavior becomes better after using it;
- boundary safety: repo-first, routing, beginner-path, and defect-capture constraints.

## Минимальный набор cases

Используйте 2-4 cases:

1. Очевидный positive case: должен trigger.
2. Пограничный positive case: должен trigger, но требует аккуратной интерпретации.
3. Соседний negative case: не должен trigger, хотя слова пересекаются.
4. Regression case: проверяет известную repo boundary, если она есть.

Для prompt-like artifacts замените "trigger" на "route/use": нужно ли применять этот scenario, runbook или handoff rule?

## Scoring / оценка

Используйте простой result для каждого case:

```text
PASS | FAIL | UNCLEAR
```

Оценивайте три измерения:

- selection: was the right artifact chosen;
- execution: were the required steps concrete enough;
- restraint: did it avoid adding mandatory work outside the requested scope.

## Heuristics улучшения

Если positive cases fail:

- добавьте concrete trigger phrases в description или opening rule;
- сделайте первый workflow step более decisive;
- назовите artifact classes, которые он покрывает.

Если negative cases fail:

- добавьте exclusions в boundaries;
- уберите broad wording из description;
- вынесите unrelated capabilities в другой artifact.

Если usefulness fails:

- добавьте expected output shape;
- добавьте короткий checklist;
- перенесите long background text в reference file.

Если beginner-path safety fails:

- пометьте workflow как optional advanced mode;
- уберите его из quick-start paths;
- ссылайтесь на него только из maintenance или quality sections.

## Пример factory-template

Target: `template-repo/skills/skill-master-lite/SKILL.md`

Positive prompt:

```text
Create a new lightweight Codex skill for validating factory-template handoff blocks.
```

Ожидание: `skill-master-lite` должен trigger, потому что запрос просит создать repo skill.

Negative prompt:

```text
I am starting my first project from the factory template. What command do I run?
```

Ожидание: `skill-master-lite` не должен trigger. Beginner path должен оставаться в `docs/first-project.md` или `docs/guided-launcher.md`.

Проверка usefulness:

```text
После использования skill новый artifact должен иметь clear trigger contract, boundaries и testable QA surface.
```
