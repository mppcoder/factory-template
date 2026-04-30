# Defect capture: Windows bootstrapper PowerShell/defaults UX gap

Дата: `2026-04-30`.

## Симптом

Beginner-facing install guidance did not explicitly recommend PowerShell 7, and the interactive installer did not show safe default values for common prompts such as SSH username, SSH port and fallback archive filenames.

## Классификация слоя

- task class: release-followup
- layer: Windows beginner bootstrapper UX
- affected artifacts:
  - `windows-bootstrap/install-windows.ps1`
  - `windows-bootstrap/README.md`
  - `windows-bootstrap/tests/validate-windows-bootstrap.py`

## Remediation

- Added PowerShell 7 recommendation and `winget` install command.
- Added default values for `SSH username=root`, `SSH port=22`, `TargetRoot=/projects/factory-template`, `IncomingDir=/projects/factory-template/_incoming`, GitHub-first install source and `factory-v2.5.2` fallback artifact names.
- Left `VPS host/IP` as required input because there is no safe universal default.

## Evidence

```bash
python3 windows-bootstrap/tests/validate-windows-bootstrap.py .
bash -n windows-bootstrap/scripts/remote-install-factory-template.sh RELEASE_BUILD.sh PRE_RELEASE_AUDIT.sh template-repo/scripts/verify-all.sh
```
