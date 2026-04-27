# Дефект: closeout не фиксирует continuation outcome

Date: 2026-04-27

reusable: yes
learning_patch_status: not_required
learning_patch_reason: Это прямое усиление уже существующего closeout/boundary guardrail; отдельный learning proposal не нужен, потому что remediation меняет сценарии, generated checklist и validators в этом же scope.

## Summary

Финальные ответы могли корректно сказать `Внешних действий не требуется.`, но при этом не объяснить, что пользователю делать для продолжения roadmap, или не сказать явно, что все задачи текущего scope полностью выполнены.

## Evidence

Пользователь дважды запросил уточнение после closeout:

- сначала после runtime/roadmap stage, потому что не было ясно, что дальше;
- затем после roadmap-continuity fix, потому что финал снова не отделил "следующий внешний этап существует" от "в текущем repo-scope задач больше нет".

## Layer Classification

- Layer: closeout / completion package / direct-task response.
- Defect class: missing continuation outcome.
- Owner boundary: repo scenario-pack, generated `.chatgpt` artifacts and validators.
- External boundary: пользователь получает инструкцию только если есть реальный внешний шаг; иначе получает explicit fully-done outcome.

## Remediation

Усилить контракт closeout:

- если есть внешний/пользовательский next step, финал обязан завершаться `## Инструкция пользователю`;
- если внешнего шага нет, финал обязан сказать `Внешних действий не требуется.` и явно указать, что следующий пользовательский шаг отсутствует / текущий scope полностью закрыт;
- если есть будущий roadmap stage, но он не actionable сейчас, финал обязан назвать его как future boundary и объяснить, что сейчас делать нечего;
- validators должны проверять наличие continuation outcome в generated task pack/direct-task guidance.

## Status

Captured and remediated in current scope.
