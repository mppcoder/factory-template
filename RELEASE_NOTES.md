# Release Notes

## 2.4.3 - 2026-04-22

### О чём этот релиз

Релиз `2.4.3` собирает полный release-facing пакет по самому `factory-template`.
Главная цель релиза: сделать описание проекта, архитектуры, дерева репозитория, ключевых workflow и release contour полным, каноническим и пригодным для downstream-consumed repo-first работы без параллельных источников истины.

### Что вошло

- добавлен root-level `RELEASE_NOTES.md` как канонический notes source для релиза и release executor;
- `docs/template-architecture-and-event-workflows.md` расширен до полного reference-doc по:
  - функциональному назначению проекта;
  - архитектуре и разделению advisory/executable layers;
  - дереву репозитория и source-of-truth boundaries;
  - ключевым workflow от intake до выпуска релиза;
- release-facing пакет нормализован вокруг одного набора файлов:
  - `README.md`
  - `VERSION.md`
  - `CHANGELOG.md`
  - `RELEASE_NOTES.md`
  - `CURRENT_FUNCTIONAL_STATE.md`
  - `docs/template-architecture-and-event-workflows.md`
- release pack, manifests, meta-template notes и `.chatgpt` closeout artifacts синхронизированы под `2.4.3`.

### Архитектурные изменения в документации

- теперь явно разделены `advisory/policy layer` и `executable routing layer`;
- отдельно описаны handoff, self-handoff, remediation, verification, release-followup и completion-package contours;
- зафиксировано, какие каталоги и файлы являются source-of-truth для текущего repo и для downstream repos;
- release-facing reference layer больше не опирается на разрозненные частичные описания.

### Что важно для downstream

- для factory-template ChatGPT Project canonical instruction не менялась по сути, но должна ссылаться на актуальный repo и repo-first rule set;
- для downstream/battle repos source-of-truth по `AGENTS` остаётся в `template-repo/AGENTS.md`;
- completion package и source/export contours теперь должны использовать новый `RELEASE_NOTES.md` как часть release-facing канона;
- для `hot15` сохраняется правило flat folder без подпапок.

### Проверка и выпуск

Релизный пакет рассчитан на прохождение:

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh`
- `bash PRE_RELEASE_AUDIT.sh`
- `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- `bash VALIDATE_RELEASE_DECISION.sh`
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`

### Ограничения

- semantic quality проверки по-прежнему частично эвристические;
- публикация GitHub Release зависит от доступности и авторизации `gh`;
- release-facing reference layer остаётся живым каноном и требует синхронного обновления при следующих process changes.
