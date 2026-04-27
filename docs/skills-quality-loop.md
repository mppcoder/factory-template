# Цикл качества skills

Этот контур нужен для развития самого `factory-template`: когда мы добавляем skill, scenario, handoff rule или другой prompt-like артефакт, можно быстро проверить, срабатывает ли он в нужный момент и правда ли помогает.

Это advanced mode. Он не входит в beginner default path и не нужен человеку, который просто запускает первый проект по `docs/first-project.md` или `docs/guided-launcher.md`.

## Короткая модель

```text
создал -> протестировал -> улучшил trigger/usefulness
```

- `skill-master-lite` помогает создать или улучшить небольшой skill/prompt artifact.
- `skill-tester-lite` помогает проверить trigger, usefulness, baseline vs guided и границы применения.
- Artifact Eval Harness добавляет optional machine-readable `artifact-eval/v1` spec и deterministic report для reusable artifacts.
- References внутри tester skill дают простой формат тест-кейсов, отчета и spec.

## Когда использовать

Используйте этот цикл, если меняете reusable factory artifact:

- `template-repo/skills/<skill-name>/SKILL.md`;
- сценарий в `template-repo/scenario-pack/`;
- handoff/runbook/policy текст;
- task template или checklist, который должен менять поведение Codex.
- advanced execution artifact вроде `feature-execution-lite`.

Не используйте его как обязательный шаг для новичка. Для обычного первого проекта достаточно guided launcher и существующих validators.

## Workflow / процесс

1. Создайте или улучшите артефакт через `skill-master-lite`.
2. Выберите 2-4 коротких кейса:
   - очевидный positive case;
   - пограничный positive case;
   - соседний negative case;
   - boundary/regression case, если есть.
3. Прогоните кейсы через `skill-tester-lite`.
4. Исправьте только то, что улучшает trigger/usefulness или boundary clarity.
5. При необходимости сохраните короткий отчет по шаблону:
   `template-repo/skills/skill-tester-lite/references/report-template.md`.
6. Если нужен reusable deterministic report, используйте:
   `docs/artifact-eval-harness.md` и `template-repo/scripts/eval-artifact.py`.

## Пример на артефакте factory-template

Целевой artifact:

```text
template-repo/skills/skill-master-lite/SKILL.md
```

Positive case:

```text
Create a new lightweight Codex skill for validating factory-template handoff blocks.
```

Ожидание: `skill-master-lite` должен сработать, потому что задача про создание repo skill.

Соседний negative case:

```text
I am starting my first project from the factory template. What command do I run?
```

Ожидание: `skill-master-lite` не должен сработать. Это beginner path, его ведут `docs/first-project.md` и `docs/guided-launcher.md`.

Проверка usefulness:

```text
После применения skill новый артефакт должен иметь trigger contract, boundaries и минимум один тестируемый QA case.
```

## Что считать успехом

- Артефакт понятно выбирается на правильных запросах.
- Похожие, но чужие запросы не затягиваются в этот skill/scenario.
- Текст помогает Codex действовать лучше, а не просто звучит подробнее.
- Beginner path не становится длиннее.
- Repo-first и routing boundaries остаются явными.
- Для durable checks есть валидный report, который проходит `validate-artifact-eval-report.py`.

## Что не делать

- Не переносить целиком внешний comparison repo.
- Не строить benchmark harness без отдельного решения.
- Не переносить Claude-specific runners, parallel teams или transcript graders в default path.
- Не добавлять этот цикл в mandatory onboarding.
- Не считать advisory text автоматическим переключением model/profile/reasoning.
