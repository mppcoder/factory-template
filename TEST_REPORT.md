# TEST REPORT v2.4.2

## Что проверено
- pre-release audit
- factory-template ops policy validator
- fresh scaffold: greenfield + small-fix + manual
- fresh scaffold: brownfield + brownfield-audit + manual
- golden examples
- versioning / defect-capture / alignment layer
- curated reference/export packs and boundary-actions policy layer
- feedback validator and ingest dry-run path
- codex task pack validator
- semantic validator для curated reference/export packs
- phase-aware recommendation layer для boundary-actions и pack summary
- automatic phase detection helper
- synthetic phase detection self-test
- repo-first ChatGPT Project instruction mode

## Ожидаемое поведение на fresh scaffold
Проходят structural / versioning / defect / alignment проверки.
Evidence / quality / DoD до смыслового наполнения артефактов не проходят.

## Фактический результат
- `PRE_RELEASE_AUDIT.sh` проходит на чистом пакете.
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh` проходит на чистом пакете.
- `SMOKE_TEST.sh` проходит на чисто распакованном финальном архиве.
- `EXAMPLES_TEST.sh` проверяет 36 из 36 комбинаций и проходит зелёно.
- `MATRIX_TEST.sh` проходит на чисто распакованном финальном архиве.
- `MATRIX_TEST.sh` подтверждает, что сырой `meta-feedback` блокируется validator, а после заполнения dry-run ingest проходит.
- `MATRIX_TEST.sh` подтверждает, что generated `codex task pack` проходит отдельный semantic validator и подхватывает active scenario routing.
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh` подтверждает semantic profile для `sources-pack-core-20`, `sources-pack-release-20` и `sources-pack-bugfix-20`.
- `EXPORT_FACTORY_TEMPLATE_SOURCES.sh` и `GENERATE_BOUNDARY_ACTIONS.sh` публикуют phase-aware рекомендацию для `controlled-fixes`, `release` и `bugfix-drift`.
- `DETECT_FACTORY_TEMPLATE_PHASE.sh` корректно различает `release` и `bugfix-drift` на rule-based changed path signals.
- `PHASE_DETECTION_TEST.sh` автоматически проверяет synthetic `controlled-fixes`, `release` и `bugfix-drift` сценарии.
- launcher smoke на временном scaffold подтверждает, что создание проекта больше не зависит от внешнего staging URL и сразу переводит проект в repo-first режим.
- `POST_UNZIP_SETUP.sh` остаётся безопасным для non-interactive verify path и не блокирует test runs prompt'ом.
- validator `validate-codex-task-pack.sh` теперь требует, чтобы handoff pack явно фиксировал приоритет правил repo.
- validator `validate-codex-task-pack.sh` теперь также требует правило: handoff пользователю выдаётся только одним цельным copy-paste блоком, а не ссылкой на файл и не несколькими блоками.
- `validate-handoff-response-format.sh` проверяет готовый markdown handoff-response и ловит file-based handoff, несколько handoff-заголовков и отсутствие fenced copy-paste блока.
- `release` определяется только при сочетании release-path signals и checked intent markers в `RELEASE_CHECKLIST.md`.
- `bugfix-drift` определяется только при сочетании bug/validator path signals и bug-report intent markers в `reports/bugs/*.md`.
- Golden examples и fresh scaffold синхронизированы с финальным versioning layer.
- curated `sources-pack-core-20`, `sources-pack-release-20`, `sources-pack-bugfix-20` собираются из декларативного policy manifest.
- boundary-actions guide генерируется из markdown template и проверяется вместе с ops-policy слоем.

## Что вошло в релиз 2.4.2
- синхронизированы root/template/meta-template/example версии и release labels;
- `RELEASE_BUILD.sh` перестал использовать вручную вшитый legacy-id релиза;
- prerelease-аудит усилен проверками version drift и запрещенных legacy-ссылок.
- golden examples дополнительно синхронизированы по `project-origin.md`, чтобы versioning validator проходил end-to-end.
- для `factory-template` добавлен декларативный ops-policy layer и его автоматический validator.
- release-oriented pack теперь несет release-facing docs (`RELEASE_CHECKLIST.md`, `VERIFY_SUMMARY.md`, `RELEASE_NOTE_TEMPLATE.md`) вместо временного audit snapshot.
- bugfix-oriented pack теперь включает handoff/feedback validators, которые реально нужны для drift-исправлений.
- policy layer теперь хранит `default_phase`, phase-specific recommendation matrix и detection rules для Sources upload.
- policy layer теперь хранит `default_phase`, phase detection rules и recommendation matrix для reference/export packs.
- archive/reference pack generation теперь строятся из единого declarative manifest.
- ChatGPT Project переведён на repo-first режим с обязательным чтением `00-master-router.md` из GitHub repo.

## Известные ограничения
- `MATRIX_TEST.sh` остаётся representative prerelease runner, а не exhaustive full-matrix coverage для всех 22 допустимых комбинаций;
- back-sync по-прежнему controlled safe-apply flow, а не full auto-sync.
- semantic/relevance оценка curated packs пока остается rule-based, а не phase-aware recommendation engine.
- phase detection пока rule-based по changed paths и может не уловить более сложный operator intent без явных файловых сигналов.
- документальные intent signals сейчас реализованы только для `release`, а не для всех фаз.
- document intent signals сейчас реализованы для `release` и `bugfix-drift`, но ещё не покрывают возможные более тонкие подфазы внутри controlled fixes.
- phase-aware export/reference packs остаются вспомогательным слоем и не заменяют чтение сценариев из GitHub repo.
