---
name: skill-master-lite
description: Создает или улучшает lightweight factory-template skills и prompt-like artifacts. Используй, когда Codex просят набросать новый repo skill, уточнить skill trigger, сократить разросшийся prompt artifact, улучшить usefulness scenario/runbook instructions или подготовить artifact к optional skill quality loop без внедрения full benchmark system.
---

# Skill Master Lite / мастер компактных skills

Используйте этот skill, чтобы превратить черновой skill или prompt-like artifact в маленький, triggerable и полезный repo artifact. Держите workflow lightweight и optional; это advanced factory-maintenance path, а не beginner default.

## Workflow / процесс

1. Определите artifact type:
   - Codex skill: `template-repo/skills/<name>/SKILL.md`
   - Prompt-like artifact: scenario, runbook, handoff block, policy note, checklist, or task template.

2. Сначала напишите trigger contract:
   - какая task должна активировать artifact;
   - какая task не должна его активировать;
   - какие repo rules остаются выше по приоритету.

3. Держите body процедурным:
   - включите минимальный workflow, который нужен другой Codex instance;
   - переносите long examples или report shapes в `references/`;
   - не добавляйте full comparison repo, benchmark harness или novice-facing mandatory step.

4. Добавьте usefulness check:
   - какой output должен стать лучше после использования artifact;
   - какой failure докажет, что trigger слишком широкий, слишком узкий или неясный;
   - какой файл нужно проверить через `skill-tester-lite`.

5. Передавайте в `skill-tester-lite`, когда пользователь просит validation, trigger QA, usefulness QA или improvement loop.

## Форма skill

Для Codex skill держите эту структуру, если в repo нет более сильной локальной convention:

```text
---
name: short-hyphen-name
description: What the skill does and exact situations when to use it.
---

# Human Title

Короткий purpose paragraph.

## Workflow
Numbered steps.

## Boundaries
Чего избегать, что остается optional, что out of scope.
```

В YAML frontmatter используйте только `name` и `description`.

## Форма prompt-like artifact

Для scenarios, runbooks, handoffs или policy prompts:

- укажите decision point до процедуры;
- разделяйте advisory text и executable routing;
- называйте required inputs, outputs и verification;
- предпочитайте один clear path плюс explicit fallback вместо нескольких равнозначных branches;
- добавляйте короткую пометку "не для beginner default path", если artifact является advanced-only.

## Checklist улучшения

Перед завершением проверьте:

- Trigger: future Codex instance может понять, когда использовать artifact.
- Usefulness: artifact меняет поведение, а не только wording.
- Scope: он не добавляет required novice step.
- Repo-first: он указывает на repo files и сохраняет scenario-pack/router precedence.
- Testability: можно написать хотя бы один realistic test prompt для `skill-tester-lite`.

## Output / результат

Когда просят создать или улучшить artifact, верните:

- files changed;
- trigger/usefulness changes;
- optional QA suggestion, если пользователь еще не просил запускать loop.
