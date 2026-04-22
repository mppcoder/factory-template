# Bug Report: direct Codex task can skip visible self-handoff in the response even when scenario-pack requires it

## Идентификатор
bug-011-direct-task-visible-self-handoff-gap

## Краткий заголовок
`factory-template` уже требует direct-task self-handoff на уровне сценариев и `.chatgpt` артефактов, но не закрепляет достаточно жёстко, что этот self-handoff должен быть явно показан пользователю в самом стартовом ответе Codex до remediation.

## Где найдено
Repo: `factory-template`

Затронутые зоны:
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/17-direct-task-self-handoff.md`
- `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md`
- `factory_template_only_pack/07-AGENTS-factory-template.md`
- `template-repo/scripts/validate-handoff-response-format.py`

## Шаги воспроизведения
1. Дать Codex прямую задачу вне ChatGPT Project.
2. Убедиться, что задача defect-class или remediation-class и требует router/self-handoff discipline.
3. Наблюдать, что Codex может начать анализ, verification или даже implementation, ссылаясь на уже известный контекст, но не вывести явный self-handoff блок в ответе.
4. Проверить, что existing process layer валидирует handoff block для handoff в Codex, но не валидирует аналогичную видимую форму direct-task self-handoff в ответе Codex.

## Ожидаемое поведение
- Для direct task первый substantive ответ Codex должен явно содержать self-handoff summary до remediation.
- Такой self-handoff должен включать как минимум:
  - classification
  - selected project profile
  - selected scenario
  - current pipeline stage
  - artifacts to update
  - handoff allowed
  - defect-capture path при defect-class задаче
- После этого уже допустимы анализ, implementation, verification или closeout.

## Фактическое поведение
- Repo хорошо описывает artifact-level direct-task self-handoff.
- Но direct task still may skip visible self-handoff in the actual assistant response.
- В результате Codex может формально "знать", что self-handoff нужен, но не материализовать его как явный gate before remediation.

## Evidence
- `template-repo/scenario-pack/17-direct-task-self-handoff.md` требует self-handoff sequence, но не фиксирует достаточно жёстко, что он должен быть явно показан пользователю в стартовом ответе.
- `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md` закрепляет общий handoff/footer behavior, но не делает visible direct-task self-handoff обязательным first response artifact.
- `template-repo/scripts/validate-handoff-response-format.py` проверяет single-block handoff format, но не покрывает direct-task self-handoff response contract.

## Слой дефекта
factory-template

## Временный обход
- При каждой direct task вручную требовать от Codex сначала вывести self-handoff summary текстом в ответе и только потом продолжать.

## Решение / статус
in-progress
