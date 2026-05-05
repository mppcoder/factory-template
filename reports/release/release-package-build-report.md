# Отчет сборки release package

Дата: 2026-05-05

## Область

- release line: `2.5.8`
- package: `factory-v2.5.8`
- source commit: `5ecf7f1a35749452d79adc6e3f087abb5c3c200a`
- package stage: `release publication / release artifact assembly`
- publication boundary: GitHub Release/tag publication was not executed; this report covers artifact assembly and validation only.

## Артефакты

- archive: `/projects/factory-template/_incoming/factory-v2.5.8.zip`
- manifest: `/projects/factory-template/_incoming/factory-v2.5.8.manifest.yaml`
- checksum: `/projects/factory-template/_incoming/factory-v2.5.8.zip.sha256`
- archive root: `factory-v2.5.8/`
- archive size: `2026502 bytes`
- SHA256: `f74e0c65d5da4a9fb5bf676ce142b10d9ef5c1e4a34914398272097f1dccd83e`

## Проверка

- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.8.zip` -> passed.
- `cd _incoming && sha256sum -c factory-v2.5.8.zip.sha256` -> passed.
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.8.zip --checksum _incoming/factory-v2.5.8.zip.sha256 --manifest _incoming/factory-v2.5.8.manifest.yaml` -> passed.
- embedded manifest says `stage_version_sync: passed`, `stage_pre_release_audit: passed`, `archive_validator: passed`.

## Safety boundary / граница

- npm install/download path remains unsupported.
- `FactoryTemplateSetup.exe` remains a future signed wrapper boundary and is not built by this package.
- GitHub Release publication, tag creation and release approval remain outside this artifact assembly step.
