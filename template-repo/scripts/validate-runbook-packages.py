#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


PACKAGE_ROOT = Path("docs/operator/runbook-packages")
PACKAGE_FILES = [
    "01-user-runbook.md",
    "02-codex-runbook.md",
    "03-checklist.md",
    "04-verify.md",
    "05-closeout.md",
]
PACKAGES = {
    "01-factory-template": {
        "must": [
            "factory-producer-owned",
            "VS Code Remote SSH",
            "Codex extension / Codex chat",
            "USER-ONLY SETUP",
            "CODEX-AUTOMATION",
            "codex-app-remote-ssh",
            "vscode-remote-ssh-codex-extension",
            "Codex takeover point",
            "Внешних действий не требуется",
        ],
        "final": ["greenfield-product", "factory-producer-owned"],
    },
    "02-greenfield-product": {
        "must": [
            "greenfield-product",
            "greenfield-active",
            "VS Code Remote SSH",
            "Codex extension / Codex chat",
            "USER-ONLY SETUP",
            "CODEX-AUTOMATION",
            "codex-app-remote-ssh",
            "vscode-remote-ssh-codex-extension",
            "takeover point",
        ],
        "final": ["greenfield-product", "greenfield"],
    },
    "03-brownfield-with-repo-to-greenfield": {
        "must": [
            "Brownfield with repo не является финальным типом проекта",
            "conversion",
            "greenfield-product",
            "greenfield-converted",
            "documented blocker",
            "archive",
            "USER-ONLY SETUP",
            "CODEX-AUTOMATION",
            "codex-app-remote-ssh",
            "vscode-remote-ssh-codex-extension",
            "takeover point",
            "validate-brownfield-transition.py",
            "validate-greenfield-conversion.py",
        ],
        "final": ["greenfield-product", "greenfield-converted"],
    },
    "04-brownfield-without-repo-to-greenfield": {
        "must": [
            "Brownfield without repo",
            "не финальный тип проекта",
            "_incoming",
            "не является sibling в `/projects`",
            "reconstructed-repo",
            "greenfield-product",
            "greenfield-converted",
            "documented blocker",
            "archived/renamed/moved",
            "USER-ONLY SETUP",
            "CODEX-AUTOMATION",
            "codex-app-remote-ssh",
            "vscode-remote-ssh-codex-extension",
            "takeover point",
        ],
        "final": ["greenfield-product", "greenfield-converted"],
    },
}
REQUIRED_ROOT_FILES = [
    "README.md",
    "00-package-contract.md",
]
REQUIRED_SCRIPTS = {
    "validate-runbook-packages.py",
    "validate-brownfield-transition.py",
    "validate-greenfield-conversion.py",
    "validate-codex-routing.py",
    "validate-project-lifecycle-dashboard.py",
    "verify-all.sh",
    "resolve-codex-task-route.py",
    "first-project-wizard.py",
    "preflight-vps-check.py",
    "validate-project-preset.py",
}
COMMAND_RE = re.compile(r"^\s*(?:python3|bash)\s+([^\s]+)", re.MULTILINE)
FAKE_AUTOSWITCH_PATTERNS = [
    re.compile(r"(?i)(handoff|advisory|scenario).{0,80}(auto[- ]?switch|switches model|switches profile)"),
    re.compile(r"(?i)(handoff|advisory|сценари|инструкц).{0,100}(автоматически переключает|сам переключает)"),
]
HIDDEN_SHELL_PATTERN = re.compile(r"(?i)(default|по умолчанию).{0,120}(запустите|run).{0,40}(orchestrate|launch-codex|codex --profile)")
BEGINNER_STEP_FIELDS = [
    "- Окно:",
    "- Делает:",
    "- Зачем:",
    "- Что нужно до начала:",
    "- Где взять значения:",
    "- Команды для копирования:",
    "- Куда вставить:",
    "- Ожидаемый результат:",
    "- Если ошибка:",
    "- Следующий шаг:",
]
FACTORY_REQUIRED_STEPS = [
    "FT-000",
    "FT-010",
    "FT-020",
    "FT-030",
    "FT-040",
    "FT-050",
    "FT-060",
    "FT-070",
    "FT-080",
    "FT-090",
    "FT-100",
    "FT-110",
    "FT-120",
    "FT-130",
    "FT-140",
    "FT-200",
    "FT-300",
    "FT-400",
    "FT-500",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def add_missing(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"отсутствует файл `{path}`")


def command_target_exists(root: Path, target: str) -> bool:
    normalized = target.strip()
    direct = root / normalized
    if direct.exists():
        return True
    if normalized.startswith("scripts/"):
        return (root / "template-repo" / normalized).exists() or (
            root / "template-repo" / "scripts" / Path(normalized).name
        ).exists()
    if normalized.startswith("template-repo/scripts/"):
        return (root / normalized).exists()
    return Path(normalized).name in REQUIRED_SCRIPTS and (root / "template-repo" / "scripts" / Path(normalized).name).exists()


def validate_package_files(root: Path, errors: list[str]) -> None:
    base = root / PACKAGE_ROOT
    for rel in REQUIRED_ROOT_FILES:
        add_missing(base / rel, errors)
    contract = read(base / "00-package-contract.md") if (base / "00-package-contract.md").exists() else ""
    for token in [
        "Advisory/policy layer",
        "Executable routing",
        "Browser ChatGPT Project",
        "VS Code Remote SSH",
        "greenfield-product",
        "Brownfield",
        "conversion",
    ]:
        if token not in contract:
            errors.append(f"package contract не содержит обязательный маркер `{token}`")

    for package, spec in PACKAGES.items():
        package_dir = base / package
        if not package_dir.is_dir():
            errors.append(f"отсутствует package directory `{package_dir}`")
            continue
        combined = ""
        for rel in PACKAGE_FILES:
            path = package_dir / rel
            add_missing(path, errors)
            if path.exists():
                text = read(path)
                combined += "\n" + text
                if len(text.strip()) < 120:
                    errors.append(f"`{path}` слишком короткий для usable runbook/checklist")
        for token in spec["must"]:
            if token not in combined:
                errors.append(f"`{package}` не содержит обязательный маркер `{token}`")
        for token in spec["final"]:
            if token not in combined:
                errors.append(f"`{package}` не фиксирует final-state marker `{token}`")
        if "02-codex-runbook.md" in PACKAGE_FILES:
            codex_path = package_dir / "02-codex-runbook.md"
            if codex_path.exists():
                codex_text = read(codex_path)
                if package == "01-factory-template" and "Язык ответа Codex: русский" not in codex_text:
                    errors.append("factory-template Codex runbook не содержит language contract")
                if "уже открыт" in codex_text and "не является" not in codex_text:
                    errors.append(f"`{codex_path}` может содержать fake already-open session switch wording")


def validate_beginner_flow(root: Path, errors: list[str]) -> None:
    base = root / PACKAGE_ROOT
    for package in PACKAGES:
        user_path = base / package / "01-user-runbook.md"
        codex_path = base / package / "02-codex-runbook.md"
        if not user_path.exists() or not codex_path.exists():
            continue
        user_text = read(user_path)
        codex_text = read(codex_path)
        for marker in ["USER-ONLY SETUP", "CODEX-AUTOMATION"]:
            if marker not in user_text:
                errors.append(f"`{user_path}` не содержит beginner boundary `{marker}`")
            if marker not in codex_text:
                errors.append(f"`{codex_path}` не содержит automation boundary `{marker}`")
        if "takeover point" not in user_text.lower() and "takeover-точ" not in user_text.lower():
            errors.append(f"`{user_path}` не фиксирует Codex takeover point")
        if "Codex сам" not in user_text and "Codex выполняет" not in user_text:
            errors.append(f"`{user_path}` не отделяет Codex automation от user-only steps")
        missing_fields = [field for field in BEGINNER_STEP_FIELDS if field not in user_text]
        if missing_fields:
            errors.append(f"`{user_path}` не содержит поля beginner step card: {', '.join(missing_fields)}")
        if package == "01-factory-template":
            for step_id in FACTORY_REQUIRED_STEPS:
                if step_id not in user_text:
                    errors.append(f"`{user_path}` не содержит обязательный шаг `{step_id}`")
            for token in [
                "ChatGPT plan",
                "GitHub account",
                "Timeweb Cloud",
                "Ubuntu 24.04",
                "ssh factory-vps",
                "remote_connections = true",
                "npm i -g @openai/codex",
                "mppcoder/factory-template",
            ]:
                if token not in user_text + "\n" + codex_text:
                    errors.append(f"`{package}` не содержит beginner setup token `{token}`")


def validate_command_lint(root: Path, errors: list[str]) -> None:
    for path in sorted((root / PACKAGE_ROOT).glob("**/*.md")):
        text = read(path)
        for match in COMMAND_RE.finditer(text):
            target = match.group(1)
            if not command_target_exists(root, target):
                errors.append(f"`{path}` ссылается на несуществующую command path `{target}`")
        for pattern in FAKE_AUTOSWITCH_PATTERNS:
            found = pattern.search(text)
            if found:
                line = found.group(0)
                lowered = line.lower()
                if "не " not in lowered and "not " not in lowered:
                    errors.append(f"`{path}` содержит возможный fake auto-switch claim: {line}")
        hidden = HIDDEN_SHELL_PATTERN.search(text)
        if hidden and "fallback" not in text[hidden.start() : hidden.start() + 220].lower():
            errors.append(f"`{path}` может продвигать hidden shell step как default")


def validate_dashboard(root: Path, errors: list[str]) -> None:
    dashboard = load_yaml(root / "template-repo" / "template" / ".chatgpt" / "project-lifecycle-dashboard.yaml")
    packages = dashboard.get("runbook_packages")
    if not isinstance(packages, list) or len(packages) != 4:
        errors.append("project-lifecycle-dashboard должен содержать 4 runbook_packages")
        return
    seen: set[str] = set()
    for index, item in enumerate(packages, 1):
        if not isinstance(item, dict):
            errors.append(f"runbook_packages[{index}] должен быть mapping")
            continue
        package_id = str(item.get("id") or "")
        seen.add(package_id)
        for key in ["id", "path", "current_phase", "gates", "blockers", "next_action", "owner_boundary"]:
            if key not in item:
                errors.append(f"runbook_packages[{package_id or index}] не содержит `{key}`")
        if package_id and package_id not in PACKAGES:
            errors.append(f"dashboard содержит неизвестный runbook package `{package_id}`")
        if str(item.get("owner_boundary") or "") != "internal-repo-follow-up":
            errors.append(f"runbook package `{package_id}` должен иметь owner_boundary internal-repo-follow-up")
        if not isinstance(item.get("gates"), list) or not item.get("gates"):
            errors.append(f"runbook package `{package_id}` должен содержать gates")
        if not isinstance(item.get("blockers"), list):
            errors.append(f"runbook package `{package_id}` blockers должен быть list")
        path = str(item.get("path") or "")
        if path and not (root / path).exists():
            errors.append(f"dashboard runbook package `{package_id}` ссылается на отсутствующий path `{path}`")
    missing = sorted(set(PACKAGES) - seen)
    if missing:
        errors.append("dashboard не содержит packages: " + ", ".join(missing))


def validate_validator_coverage(root: Path, errors: list[str]) -> None:
    script = root / "template-repo" / "scripts" / "validate-runbook-packages.py"
    add_missing(script, errors)
    verify = read(root / "template-repo" / "scripts" / "verify-all.sh")
    if "validate-runbook-packages" not in verify:
        errors.append("verify-all.sh quick не запускает validate-runbook-packages")
    for required in REQUIRED_SCRIPTS:
        if required == "validate-runbook-packages.py":
            continue
        if not (root / "template-repo" / "scripts" / required).exists() and required not in {"validate-project-preset.py"}:
            errors.append(f"ожидаемый validator/script отсутствует: `{required}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует слой runbook-checklist packages.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    validate_package_files(root, errors)
    validate_beginner_flow(root, errors)
    validate_command_lint(root, errors)
    validate_dashboard(root, errors)
    validate_validator_coverage(root, errors)

    if errors:
        print("RUNBOOK PACKAGES НЕВАЛИДНЫ")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RUNBOOK PACKAGES ВАЛИДНЫ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
