---
name: skill-tester-lite
description: Проверяет factory-template skills, scenario-pack, handoff blocks, runbooks, policy docs и prompt-like artifacts через легкие trigger/usefulness или artifact-eval проверки. Используй, когда Codex просят провалидировать reusable artifact, проверить момент срабатывания, сравнить baseline vs guided, оценить process/outcome/compliance assertions или запустить optional create-test-improve loop для advanced template maintenance.
---

# Skill Tester Lite / проверка компактных artifacts

Используйте этот skill для малого QA loop по skills и prompt-like artifacts. Цель не в benchmark platform; цель в том, чтобы поймать неясные triggers, слабую usefulness, слабый baseline delta и пропущенные repo-first boundaries до того, как artifact станет reusable.

## Workflow / процесс

1. Выберите target artifact и классифицируйте его:
   - `skill`: `template-repo/skills/<name>/SKILL.md`
   - `scenario-pack`: routing scenario или master-router.
   - `handoff-block`: Codex handoff, normalized handoff, response format.
   - `runbook`: operator или Codex runbook.
   - `policy-doc`: repo-first, routing, language, sync или boundary policy.
   - `prompt-like`: checklist, task template, launcher doc.
   - `advanced-execution`: `feature-execution-lite` docs/templates/checkpoint/decisions/task waves.

2. Прочитайте target artifact и, если нужно, `references/test-design-guide.md` или `references/artifact-eval-spec.md`.

3. Определите expected behavior:
   - trigger-positive cases;
   - trigger-negative cases;
   - baseline vs guided expectation;
   - process/outcome/compliance assertions;
   - usefulness expectation;
   - repo boundary or beginner-path constraint.

4. Запустите lightweight desk test:
   - используйте 2-4 реалистичных prompts или task fragments;
   - оцените, будет ли artifact выбран корректно;
   - оцените, улучшит ли следование ему output или routing.

5. Если нужен durable report, оформите `artifact-eval/v1` spec и запустите deterministic harness:
   ```bash
   python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/<name>.yaml --output /tmp/<name>-artifact-eval.md
   python3 template-repo/scripts/validate-artifact-eval-report.py /tmp/<name>-artifact-eval.md
   ```

6. Зафиксируйте findings:
   - используйте `references/report-template.md`, если нужен durable report;
   - используйте `references/artifact-eval-spec.md`, если нужен machine-readable spec;
   - иначе дайте короткий inline result с pass/fail и recommended edits.

7. Улучшайте artifact только по запросу или если текущая задача включает remediation. Держите edits минимальными и повторно проверьте измененный trigger/usefulness surface.

## References / справочные файлы

- Читайте `references/test-design-guide.md`, когда проектируете cases или оцениваете trigger/usefulness.
- Читайте `references/report-template.md`, когда пишете persistent QA report.
- Читайте `references/artifact-eval-spec.md`, когда нужен reusable spec и deterministic report.

## Критерии прохождения

Target проходит lite loop, если:

- positive trigger cases явно in scope;
- negative trigger cases явно out of scope;
- expected output полезнее generic response;
- baseline vs guided comparison показывает value или честно фиксирует non-discriminating assertions;
- process/outcome/compliance assertions проверяемы через artifact text;
- beginner default path не становится тяжелее;
- repo-first и executable-routing boundaries остаются явными там, где это важно.

## Границы

- Не требуйте этот loop от first-time users или обычных generated projects.
- Не стройте full benchmark harness или runner farm без явного запроса.
- Не переносите Claude-specific runners, parallel teams, transcript graders или timing capture в default path.
- Не считайте advisory text executable profile/model switch.
- Не прячьте defect: если тестирование выявило repo process bug, следуйте repo defect-capture path.
