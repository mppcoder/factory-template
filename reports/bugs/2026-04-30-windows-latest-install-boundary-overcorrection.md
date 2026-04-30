# Windows latest install guide moved SSH preparation outside installer boundary

Date: 2026-04-30
Status: fixed in working tree

## Summary

The latest Windows install guide overcorrected the ordering problem by moving VPS/SSH preparation into the pre-executable section. That blurred the intended product boundary: `windows-bootstrap/install-windows.ps1` is the executable automation path for SSH key setup, existing-key checks, VPS connection, repo install and Codex prompt preparation.

## Evidence

User feedback:

```text
у нас в исполняемом файле как раз автоматизация настройки ssh и т.д.
в предварительной инструкции до запуска исполняемого файла должны быть шаги по настройке powershell,
скачивания дистрибутива и запуска исполняемого файла - далее шаги исполняемого файла
до вставки хэндофф в кодекс - шаги под управлением кодекс
```

## Classification

- Layer: Windows beginner onboarding / release follow-up docs
- Impact: user guidance could imply manual SSH setup before running the installer
- Reusable template issue: yes, beginner docs must preserve executable automation boundaries

## Fix

Reworked `WINDOWS_INSTALL_LATEST.md` into three clear phases:

- before executable path: PowerShell 7, latest package download, SHA256 verification, unzip and `install-windows.ps1` launch;
- inside installer: answer VPS prompts while installer automates SSH key setup, existing-key check, remote install and Codex prompt copy;
- after handoff: Codex operates inside the repo-first route on the VPS.
