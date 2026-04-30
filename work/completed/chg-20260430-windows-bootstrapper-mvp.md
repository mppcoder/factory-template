# chg-20260430-windows-bootstrapper-mvp

## Суть

Добавлен beginner-friendly Windows bootstrapper MVP для установки `factory-template` с Windows PC на VPS в `/projects/factory-template`.

## Изменено

- `windows-bootstrap/`: PowerShell entrypoint, remote bash installer, prompts, README, future exe packaging contract and targeted validator.
- Release package integration: `RELEASE_BUILD.sh` generates root `readme.txt`; release manifest and package validator now include `windows-bootstrap/`.
- Verification integration: `template-repo/scripts/verify-all.sh quick` runs the Windows bootstrap validator.
- Docs/release layer: README, operator runbook, release notes, changelogs, current state, verify/test reports.
- Tree/language contracts updated for the new top-level source directory and generated `.release-stage/` exclusion.

## Проверка

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .` — pass.
- `python3 template-repo/scripts/validate-tree-contract.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass.
- `bash RELEASE_BUILD.sh /tmp/factory-v2.5.1-windows-bootstrap-test.zip` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.

## Ограничения

- `FactoryTemplateSetup.exe` не был собран: текущий repo environment не содержит reviewed Windows exe packaging/signing toolchain. MVP executable path — `windows-bootstrap/install-windows.ps1`.
- PowerShell runtime check не запускался локально, потому что PowerShell недоступен в текущем Linux environment.
