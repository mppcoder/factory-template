# TEST REPORT v2.4.0

## Что проверено
- pre-release audit
- factory-template ops policy validator
- fresh scaffold: greenfield + small-fix + manual
- fresh scaffold: brownfield + brownfield-audit + manual
- golden examples
- versioning / defect-capture / alignment layer
- curated Sources packs and boundary-actions policy layer
- feedback validator and ingest dry-run path

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
- Golden examples и fresh scaffold синхронизированы с финальным versioning layer.
- curated `sources-pack-core-20`, `sources-pack-release-20`, `sources-pack-bugfix-20` собираются из декларативного policy manifest.
- boundary-actions guide генерируется из markdown template и проверяется вместе с ops-policy слоем.

## Что вошло в финальный релиз
- синхронизированы root/template/meta-template/example версии и release labels;
- `RELEASE_BUILD.sh` перестал использовать вручную вшитый legacy-id релиза;
- prerelease-аудит усилен проверками version drift и запрещенных legacy-ссылок.
- golden examples дополнительно синхронизированы по `project-origin.md`, чтобы versioning validator проходил end-to-end.
- для `factory-template` добавлен декларативный ops-policy layer и его автоматический validator.

## Известные ограничения
- `MATRIX_TEST.sh` остаётся representative prerelease runner, а не exhaustive full-matrix coverage для всех 22 допустимых комбинаций;
- back-sync по-прежнему controlled safe-apply flow, а не full auto-sync.
- curated pack quality пока проверяется структурно, без отдельной semantic/relevance оценки состава Sources.
