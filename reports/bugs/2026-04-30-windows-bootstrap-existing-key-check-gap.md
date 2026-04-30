# Defect capture: Windows bootstrapper existing SSH key check gap

Дата: `2026-04-30`.

## Симптом

Installer reused an existing local SSH key file, but still attempted to append the public key to VPS `authorized_keys`. This could ask for the VPS password even when the existing key already worked.

## Классификация слоя

- task class: release-followup
- layer: Windows beginner bootstrapper UX/security
- affected artifacts:
  - `windows-bootstrap/install-windows.ps1`
  - `windows-bootstrap/README.md`
  - `windows-bootstrap/tests/validate-windows-bootstrap.py`

## Remediation

- Added `ssh -o BatchMode=yes -i <key>` check before touching `authorized_keys`.
- If the existing key already works, authorized key installation is skipped and no password is requested.
- If private key exists but `.pub` is missing, public key is recreated via `ssh-keygen.exe -y`.
- If key installation is needed, key login is verified again after updating `authorized_keys`.

## Evidence

```bash
python3 windows-bootstrap/tests/validate-windows-bootstrap.py .
bash template-repo/scripts/verify-all.sh quick
```
