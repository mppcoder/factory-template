# Windows latest install one-file guide gap

Date: 2026-04-30
Status: fixed in working tree

## Summary

Beginner Windows installation guidance required the user to know the current release folder name and run `windows-bootstrap/install-windows.ps1` from the correctly extracted ZIP tree. This caused an avoidable failure when the user entered a versioned folder that did not contain the script.

## Evidence

Observed user failure:

```text
.\windows-bootstrap\install-windows.ps1: The term '.\windows-bootstrap\install-windows.ps1' is not recognized as a name of a cmdlet, function, script file, or executable program.
```

The user also requested one file with links and copy-paste blocks that downloads latest versions rather than fixed version names.

## Classification

- Layer: Windows beginner onboarding / release follow-up docs
- Impact: new-user install path can fail before the bootstrapper starts
- Reusable template issue: yes, release instructions should avoid fixed version folder guessing for beginner flows

## Fix

Added `WINDOWS_INSTALL_LATEST.md` with:

- latest release link;
- current executable path boundary;
- PowerShell 7 setup block;
- GitHub API latest-release download block;
- ZIP, manifest and SHA256 asset detection without hard-coded version;
- SHA256 verification before unzip;
- recursive discovery of `windows-bootstrap/install-windows.ps1`;
- default answers for VPS SSH, port, target root and SSH key login;
- recovery block for the missing-script error.

README now points Windows beginners to the new one-file latest install guide.
