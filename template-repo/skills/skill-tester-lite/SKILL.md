---
name: skill-tester-lite
description: Проверяет factory-template skills и prompt-like artifacts через легкие проверки trigger/usefulness. Используй, когда Codex просят провалидировать skill, проверить момент срабатывания skill, оценить пользу prompt/scenario, сравнить expected vs actual на маленьких примерах или запустить optional create-test-improve loop для advanced template maintenance.
---

# Skill Tester Lite / проверка компактных skills

Используйте этот skill для малого QA loop по skills и prompt-like artifacts. Цель не в benchmark platform; цель в том, чтобы поймать неясные triggers, слабую usefulness и пропущенные repo-first boundaries до того, как artifact станет reusable.

## Workflow / процесс

1. Выберите target artifact и классифицируйте его:
   - `skill`: `template-repo/skills/<name>/SKILL.md`
   - `prompt-like`: scenario, runbook, handoff, policy note, checklist, task template.

2. Прочитайте target artifact и, если нужно, `references/test-design-guide.md`.

3. Определите expected behavior:
   - trigger-positive cases;
   - trigger-negative cases;
   - usefulness expectation;
   - repo boundary or beginner-path constraint.

4. Запустите lightweight desk test:
   - используйте 2-4 реалистичных prompts или task fragments;
   - оцените, будет ли artifact выбран корректно;
   - оцените, улучшит ли следование ему output или routing.

5. Зафиксируйте findings:
   - используйте `references/report-template.md`, если нужен durable report;
   - иначе дайте короткий inline result с pass/fail и recommended edits.

6. Улучшайте artifact только по запросу или если текущая задача включает remediation. Держите edits минимальными и повторно проверьте измененный trigger/usefulness surface.

## References / справочные файлы

- Читайте `references/test-design-guide.md`, когда проектируете cases или оцениваете trigger/usefulness.
- Читайте `references/report-template.md`, когда пишете persistent QA report.

## Критерии прохождения

Target проходит lite loop, если:

- positive trigger cases явно in scope;
- negative trigger cases явно out of scope;
- expected output полезнее generic response;
- beginner default path не становится тяжелее;
- repo-first и executable-routing boundaries остаются явными там, где это важно.

## Границы

- Не требуйте этот loop от first-time users или обычных generated projects.
- Не стройте full benchmark harness без явного запроса.
- Не считайте advisory text executable profile/model switch.
- Не прячьте defect: если тестирование выявило repo process bug, следуйте repo defect-capture path.
