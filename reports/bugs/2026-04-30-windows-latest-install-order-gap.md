# Windows latest install guide launches installer too early

Date: 2026-04-30
Status: fixed in working tree

## Summary

`WINDOWS_INSTALL_LATEST.md` downloaded, verified, unzipped and launched `windows-bootstrap/install-windows.ps1` inside one PowerShell block. For a new user this skipped the human preparation boundary: creating the VPS, collecting IP/password, checking SSH tools and understanding the default answers before the executable path starts asking questions.

## Evidence

User feedback:

```text
порядок нарушен, нужно помочь пользователю сделать шаги до запуска исполняемого файла
```

## Classification

- Layer: Windows beginner onboarding / release follow-up docs
- Impact: user can reach installer prompts before having VPS data and local SSH prerequisites ready
- Reusable template issue: yes, beginner install guides must separate preparation, download/verification and executable launch

## Fix

Reordered `WINDOWS_INSTALL_LATEST.md`:

- Step 0 now lists required VPS and Windows inputs before any command execution.
- PowerShell 7 setup and OpenSSH Client checks happen before package download.
- Latest release download/checksum/unzip is a separate block that does not launch the installer.
- A separate pre-launch review step lists the exact VPS values needed.
- `install-windows.ps1` launch is its own later step.
