# Релизный artifact вышел за пределы project root

## Title

`RELEASE_BUILD.sh` по умолчанию положил release archive в `/projects`, нарушив project-root layout policy.

## Observed behavior

После сборки `bash RELEASE_BUILD.sh` были созданы файлы:

- `/projects/factory-v2.5.1.zip`
- `/projects/factory-v2.5.1.zip.sha256`
- `/projects/factory-v2.5.1.manifest.yaml`

`/projects` должен содержать только project roots, а не release artifacts.

## Expected behavior

Release package artifacts должны оставаться внутри project root `factory-template`.
Для manual upload/fallback каноническое место уже задано как:

```text
/projects/factory-template/_incoming
```

## Affected layer

- release packaging
- install-from-scratch runbook
- closeout artifact location

## Evidence

- `RELEASE_BUILD.sh` использовал default `OUT_ZIP="${1:-$ROOT/../$REL_NAME.zip}"`.
- Для repo root `/projects/factory-template` это вычисляется как `/projects/factory-v2.5.1.zip`.
- Пользователь указал на нарушение правила плоского дерева `/projects`.

## Remediation plan

1. Сменить default output `RELEASE_BUILD.sh` на `$ROOT/_incoming/$REL_NAME.zip`.
2. Исключить `_incoming/` из release archive, чтобы собранные artifacts не попадали внутрь zip.
3. Обновить runbook/build report/register paths.
4. Пересобрать package в `/projects/factory-template/_incoming`.
5. Удалить ошибочные файлы из `/projects`.
6. Прогнать checksum/package validation и verified sync.

## Status

closed

## Remediation evidence

- `RELEASE_BUILD.sh` default output changed to `$ROOT/_incoming/factory-v<VERSION>.zip`.
- `.releaseignore` excludes `_incoming/`, so generated release artifacts do not enter the archive.
- `.gitignore` excludes `_incoming/`, so local downloadable artifacts stay untracked.
- `template-repo/tree-contract.yaml` now permits `_incoming` as project-root inbound/transient boundary.
- Old flat files were removed from `/projects`.
- `bash RELEASE_BUILD.sh` rebuilt the package in `/projects/factory-template/_incoming`.
- `(cd /projects/factory-template/_incoming && sha256sum -c factory-v2.5.1.zip.sha256)` passed.
- Package validator and unpacked `verify-all.sh quick` passed.
