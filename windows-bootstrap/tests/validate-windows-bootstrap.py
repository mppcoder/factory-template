#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "install-windows.ps1",
    "prompts/codex-install-prompt.txt",
    "prompts/chatgpt-project-instructions.txt",
    "scripts/remote-install-factory-template.sh",
    "build/build-windows-bootstrap.ps1",
    "tests/validate-windows-bootstrap.py",
]

REMOTE_REQUIRED_MARKERS = [
    "/projects/factory-template",
    "/projects/factory-template/_incoming",
    "https://github.com/mppcoder/factory-template.git",
    "bash POST_UNZIP_SETUP.sh",
    "python3 template-repo/scripts/validate-release-package.py",
    "bash template-repo/scripts/verify-all.sh quick",
    "PASS:",
    "FAIL:",
]

README_REQUIRED_MARKERS = [
    "FactoryTemplateSetup.exe",
    "install-windows.ps1",
    "GitHub clone/download",
    "release artifact archive",
    "factory-v2.5.4.zip",
    "factory-v2.5.4.manifest.yaml",
    "factory-v2.5.4.zip.sha256",
    "SmartScreen",
    "SHA256",
    "PowerShell 7",
    "SSH username`: `root",
    "SSH port`: `22",
    "SSH key login",
    "factory-template-vps-ed25519",
    "authorized_keys",
]

ROOT_README_MARKERS = [
    "Установка с Windows для новичка",
    "GitHub clone/download",
    "fallback archive",
]

POWERSHELL_MARKERS = [
    "ssh.exe",
    "scp.exe",
    "ssh-keygen.exe",
    "git.exe",
    "code.exe",
    "PowerShell 7",
    "DefaultSshUser",
    "DefaultSshPort",
    "Ensure-SshKeyLogin",
    "authorized_keys",
    "factory-template-vps-ed25519",
    "VPS host/IP",
    "SSH username",
    "/projects/factory-template/_incoming",
]

NPM_SUPPORT_PATTERNS = [
    re.compile(r"npm\s+path\s+supported\s*:\s*true", re.IGNORECASE),
    re.compile(r"factory-template.*npm\s+(install|i)\s+supported", re.IGNORECASE),
]


def fail(errors: list[str]) -> int:
    print("WINDOWS BOOTSTRAP VALIDATOR FAIL")
    for error in errors:
        print(f"- {error}")
    return 1


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_markers(text: str, markers: list[str], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label}: missing marker `{marker}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Windows bootstrapper MVP artifacts.")
    parser.add_argument("root", nargs="?", default=".", help="factory-template repo root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    bootstrap = root / "windows-bootstrap"
    errors: list[str] = []

    if not bootstrap.exists():
        return fail(["windows-bootstrap directory is missing"])

    for rel in REQUIRED_FILES:
        path = bootstrap / rel
        if not path.exists():
            errors.append(f"missing required file: windows-bootstrap/{rel}")
        elif path.is_file() and not read(path).strip():
            errors.append(f"required file is empty: windows-bootstrap/{rel}")

    if errors:
        return fail(errors)

    ps_text = read(bootstrap / "install-windows.ps1")
    remote_text = read(bootstrap / "scripts/remote-install-factory-template.sh")
    readme_text = read(bootstrap / "README.md")
    codex_prompt = read(bootstrap / "prompts/codex-install-prompt.txt")
    chatgpt_prompt = read(bootstrap / "prompts/chatgpt-project-instructions.txt")
    root_readme = read(root / "README.md") if (root / "README.md").exists() else ""

    require_markers(ps_text, POWERSHELL_MARKERS, "install-windows.ps1", errors)
    require_markers(remote_text, REMOTE_REQUIRED_MARKERS, "remote-install-factory-template.sh", errors)
    require_markers(readme_text, README_REQUIRED_MARKERS, "windows-bootstrap/README.md", errors)
    require_markers(root_readme, ROOT_README_MARKERS, "README.md", errors)
    require_markers(codex_prompt, ["template-repo/scenario-pack/00-master-router.md", "repo-first"], "codex prompt", errors)
    require_markers(chatgpt_prompt, ["SCENARIO_PACK_PATH=template-repo/scenario-pack", "repo-first"], "ChatGPT Project Instructions", errors)

    combined_bootstrap = "\n".join([ps_text, remote_text, readme_text, codex_prompt, chatgpt_prompt])
    for pattern in NPM_SUPPORT_PATTERNS:
        if pattern.search(combined_bootstrap):
            errors.append(f"npm is advertised as supported install path: {pattern.pattern}")
    for line in combined_bootstrap.splitlines():
        normalized = line.lower()
        if "npm" not in normalized:
            continue
        if "factory-template" not in normalized:
            continue
        if "not supported" in normalized or "не поддерж" in normalized or "unsupported" in normalized:
            continue
        if re.search(r"npm\s+(install|i)", line, re.IGNORECASE):
            errors.append(f"npm install appears to be advertised for factory-template: {line.strip()}")

    if "FactoryTemplateSetup.exe build is not implemented" not in read(bootstrap / "build/build-windows-bootstrap.ps1"):
        errors.append("build script must state that exe build is not implemented in current portable environment")

    if errors:
        return fail(errors)

    print("WINDOWS BOOTSTRAP VALIDATOR PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
