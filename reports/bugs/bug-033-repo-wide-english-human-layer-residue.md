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
fixed-active-source-layer-with-documented-archival-exceptions

## Self-handoff решение
current-route-valid

## Решение / статус
fixed

## Remediation 2026-04-25
- Добавлен canonical policy split для active source-facing русского слоя и documented archival exceptions: `template-repo/language-archive-exceptions.yaml`, `docs/language-layer-policy.md`.
- Добавлен validator `template-repo/scripts/validate-human-language-layer.py` и подключен в `template-repo/scripts/verify-all.sh quick`.
- Активные docs, release-facing artifacts, reusable skills, template handoff artifacts и routing/model docs нормализованы так, чтобы active findings были равны `0`.
- Исторические reports, `work/completed`, legacy packs, bootstrap notes и fixture evidence оставлены как archival exceptions с явной причиной.

## Verification 2026-04-25
- `python3 template-repo/scripts/validate-human-language-layer.py .` -> active findings `0`, archival exception findings `171`.
