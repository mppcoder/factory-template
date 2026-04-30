# Defect capture: Windows bootstrapper missing SSH key step

Дата: `2026-04-30`.

## Симптом

Beginner-facing install plan and bootstrapper flow covered SSH host/user/port, but did not explicitly set up key-based SSH login. As a result, a user could be asked for the VPS password repeatedly during `ssh` and `scp` operations.

## Классификация слоя

- task class: release-followup
- layer: Windows beginner bootstrapper UX/security
- affected artifacts:
  - `windows-bootstrap/install-windows.ps1`
  - `windows-bootstrap/README.md`
  - `windows-bootstrap/tests/validate-windows-bootstrap.py`

## Remediation

- Added optional default-yes SSH key setup.
- Installer creates or reuses `%USERPROFILE%\.ssh\factory-template-vps-ed25519`.
- Installer appends the public key to VPS `~/.ssh/authorized_keys` with safe permissions.
- After key setup, installer uses `ssh.exe -i` and `scp.exe -i`.
- If user skips key setup, installer warns that repeated password prompts may happen.

## Evidence

```bash
python3 windows-bootstrap/tests/validate-windows-bootstrap.py .
bash template-repo/scripts/verify-all.sh quick
```
