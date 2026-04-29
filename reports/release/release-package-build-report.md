# Отчет сборки релизного пакета

## Область

- chat_id: `FT-CH-0010`
- task: `release-package-updated-bootstrap`
- release decision: `patch-release-2.5.1`
- publication decision: `.chatgpt/release-decision.yaml` is `no-release`; tag/GitHub Release publication is intentionally skipped until a separate explicit release decision.

## Карта источников

- router: `template-repo/scenario-pack/00-master-router.md`
- handoff scenario: `template-repo/scenario-pack/15-handoff-to-codex.md`
- user runbook: `docs/operator/factory-template/01-runbook-dlya-polzovatelya-factory-template.md`
- Codex runbook: `docs/operator/factory-template/02-runbook-dlya-codex-factory-template.md`
- release truth source: `docs/releases/release-scorecard.yaml`
- release builder: `RELEASE_BUILD.sh`
- package validator: `template-repo/scripts/validate-release-package.py`
- defect capture: `reports/bugs/2026-04-29-release-package-updated-bootstrap-gaps.md`

## Версионный gate

- previous repo version: `2.5.0`
- selected decision: `patch-release-2.5.1`
- rationale: manifest/checksum generation, fallback archive verification and install-from-scratch package validation change the release-facing installation contract.
- npm path: unsupported; no `package.json` exists in repo.

## Артефакты

- archive: `/projects/factory-v2.5.1.zip`
- manifest: `/projects/factory-v2.5.1.manifest.yaml`
- checksum: `/projects/factory-v2.5.1.zip.sha256`
- archive root: `factory-v2.5.1/`
- SHA256 value: recorded in `/projects/factory-v2.5.1.zip.sha256`.

## Проверка

- `bash VERSION_SYNC_CHECK.sh` — passed.
- `bash PRE_RELEASE_AUDIT.sh` — passed after cleanup.
- `bash RELEASE_BUILD.sh` — passed and produced archive, manifest and checksum.
- `(cd /projects && sha256sum -c factory-v2.5.1.zip.sha256)` — passed.
- `python3 template-repo/scripts/validate-release-package.py /projects/factory-v2.5.1.zip --checksum /projects/factory-v2.5.1.zip.sha256 --manifest /projects/factory-v2.5.1.manifest.yaml` — passed.
- Temp unpack root: `/tmp/tmp.uBnftPUVea/factory-v2.5.1`.
- Temp unpack `bash POST_UNZIP_SETUP.sh` — passed.
- Temp unpack `bash template-repo/scripts/verify-all.sh quick` — passed.
- Working repo `bash CLEAN_VERIFY_ARTIFACTS.sh && bash template-repo/scripts/verify-all.sh quick` — passed.

## Известные ограничения

- GitHub Release/tag publication was not executed in this scope.
- npm install/download is not supported.
- Full `verify-all.sh` / smoke / examples / matrix were not rerun after this patch because package quick verification and pre-release audit covered the changed packaging/docs/validator contour.
