# Defect: промежуточные repo могли трактоваться как отдельные project roots

Дата: 2026-04-28

## Контекст

В canonical VPS layout уже было правило, что `/projects` содержит только project roots, а temporary/intermediate/reconstructed repos не должны лежать плоско рядом в `/projects`.

## Gap

Формулировка "внутри соответствующего project root" оставляла неоднозначность: промежуточный brownfield/reconstruction repo можно было ошибочно принять за самостоятельный project root. Это ослабляло запрет плоского дерева проектов.

## Риск

- загрязнение `/projects` helper repo и временными staging-каталогами;
- расхождение между целевым `greenfield-product` repo и временными реконструкциями;
- путаница при downstream sync, verified sync и operator handoff;
- повторяемый дефект в generated guidance.

## Remediation

- Зафиксировать правило: все temporary/intermediate/reconstructed/helper repos для intake/adoption/reconstruction живут только внутри repo целевого `greenfield-product`.
- Обновить active docs, scenario-pack и bootstrap guidance.
- Добавить machine-readable `workspace_layout_policy` и validator coverage.
- Добавить Artifact Eval `project-root-boundary`.

## Статус

`fixed-in-current-scope`
