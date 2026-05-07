# Factory Feedback: downstream index identity generation

## Исходный bug report
`reports/bugs/2026-05-07-downstream-ft-index-identity-inheritance.md`

## Почему это проблема фабрики
The defect is in reusable project creation logic. Any downstream project created from the template could inherit factory-only `FT` ChatGPT/Codex index identity.

## Где проявилось
`factory-template` generated-project bootstrap: `template-repo/launcher.sh` copies `template-repo/template/.chatgpt/*`.

## Повторяемый паттерн
Seed artifacts with real factory ids are safe inside `factory-template`, but unsafe when copied into downstream repos without a materialization step.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- bootstrap;
- `.chatgpt` template seed;
- validators;
- guided launcher runbook.

## Как проверить исправление
Create a generated project and run:

```bash
python3 scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml
python3 scripts/validate-codex-work-index.py .chatgpt/codex-work-index.yaml
python3 scripts/validate-project-index-identity.py .
```

Expected result: generated indexes use the downstream `PROJECT_CODE`, CH/CX counters start independently at `1`, `items: []`, and no downstream index has `project_code: FT`.
