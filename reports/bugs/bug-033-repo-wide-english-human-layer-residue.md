# Отчет о дефекте

## Идентификатор
bug-033-repo-wide-english-human-layer-residue

## Краткий заголовок
В repo остается английский человекочитаемый слой за пределами свежего handoff/closeout контура.

## Тип дефекта
reusable-process-defect

## Где найдено
- Source-facing docs: `README.md`, `docs/*`, `template-repo/template/docs/*`.
- Skill templates: `template-repo/skills/*`.
- Исторические reports/work artifacts: `reports/bugs/*`, `reports/factory-feedback/*`, `work/completed/*`.

## Шаги воспроизведения
1. Запустить repo-wide поиск по Markdown headings и типовым английским prose-фразам.
2. Найти английские заголовки вроде `Operator Next Step`, `Goal`, `Troubleshooting`, `Current Mapping`, `Workflow`, `Scope`.
3. Отделить technical literal values от человекочитаемого prose.

## Ожидаемое поведение
- Актуальный source-facing слой для `factory-template` пишет человекочитаемые заголовки и инструкции на русском.
- Английский остается только для technical literal values, команд, имен файлов, model IDs, YAML keys и внешних product names.
- Исторические artifacts либо нормализованы, либо явно классифицированы как archival exception.

## Фактическое поведение
- Свежий handoff/closeout контур теперь прикрыт validator-ами.
- Но repo-wide audit все еще находит английские human-readable headings/prose в source docs, skill templates и historical reports.

## Evidence
- [PROJECT] `docs/operator-next-step.md` содержал heading `Operator Next Step`.
- [PROJECT] `docs/releases/2.5-roadmap.md` содержал field `Goal`.
- [PROJECT] `template-repo/template/docs/integrations.md` содержал англоязычный troubleshooting list.
- [PROJECT] `template-repo/skills/skill-tester-lite/references/report-template.md` содержал `## Goal`, `## Cases`, `## Findings`.
- [PROJECT] repo-wide heading scan показывает множество archival English headings в старых reports/work artifacts.

## Слой дефекта
factory-template

## Классификация failing layer
language layer / source docs / historical artifacts

## Связь с текущим scope
partially-fixed-current-source-layer; archival cleanup remains separate

## Self-handoff решение
current-route-valid

## Решение / статус
partial-remediation
