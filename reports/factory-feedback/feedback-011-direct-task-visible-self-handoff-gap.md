# Factory Feedback: visible direct-task self-handoff still lacks enough process enforcement

## Исходный bug report
`reports/bugs/bug-011-direct-task-visible-self-handoff-gap.md`

## Почему это проблема фабрики
Фабрика уже научилась создавать executable routing и artifact-level self-handoff для direct task, но still allows a softer failure mode: Codex может не показать self-handoff явно в стартовом ответе пользователю и начать remediation по накопленному контексту.

## Где проявилось
`factory-template`, direct task to Codex, scenario-pack/runbook/validator response layer.

## Повторяемый паттерн
- scenario says "сначала self-handoff";
- artifact layer exists;
- but response-layer enforcement is weak;
- therefore direct task can skip visible gate in practice.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- scenario-pack
- codex runbook / AGENTS guidance
- response validator layer
- template `.chatgpt` direct-task artifacts

## Как проверить исправление
1. Direct task response начинается с explicit self-handoff summary before remediation.
2. Scenario-pack и runbooks прямо запрещают переход к implementation/verification без visible self-handoff.
3. Validator layer умеет ловить direct-task response без required self-handoff fields.
