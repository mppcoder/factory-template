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
            "nonstandard_vps_folder_intake",
            "legacy_runtime_source_required: false",
            "active source roots",
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
    "- Куда вставить:",
    "- Ожидаемый результат:",
    "- Если ошибка:",
    "- Evidence:",
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
    "FT-150A",
    "FT-150B",
    "FT-160",
    "FT-170",
    "FT-180",
]
FACTORY_REQUIRED_COMMANDS = [
    '$KEY="$env:USERPROFILE\\.ssh\\factory_timeweb_ed25519"',
    'ssh-keygen -t ed25519 -C "factory-template-timeweb-vps" -f $KEY',
    'Get-Content "$KEY.pub"',
    "notepad $env:USERPROFILE\\.ssh\\config",
    "Host factory-vps",
    "HostName <VPS_IP>",
    "User root",
    "IdentityFile ~/.ssh/factory_timeweb_ed25519",
    "IdentitiesOnly yes",
    "ssh factory-vps",
    "root@<server-hostname>:~#",
]
FACTORY_CODEX_AUTOMATION_TOKENS = [
    "whoami",
    "pwd",
    "uname -a",
    "lsb_release -a || cat /etc/os-release",
    "apt-get update",
    "apt-get install -y git curl ca-certificates gnupg unzip jq build-essential python3 python3-venv python3-pip pipx",
    "corepack",
    "pnpm",
    "gh --version",
    "npm i -g @openai/codex",
    "codex --version",
    "mkdir -p /projects",
    "git clone https://github.com/mppcoder/factory-template.git factory-template",
    "sed -n '1,240p' AGENTS.md",
    "bash template-repo/scripts/verify-all.sh quick",
    "bash VERIFIED_SYNC.sh",
    "git status --short --branch",
]
BEGINNER_REMOTE_ACCEPTANCE_TOKENS = [
    "REMOTE_CONTEXT_MARKER",
    "Do not paste into local Codex",
    "do not paste into local Codex",
    "No hidden second shell step",
    "no hidden second shell step",
]
FORBIDDEN_USER_CHECKLIST_PHRASES = [
    "Advisory/policy layer",
    "advisory layer",
    "defect-capture",
    "Defect-capture",
    "release-facing",
    "route receipt",
    "self-handoff",
    "handoff route receipt",
    "Dashboard отражает",
    "обновлены только релевантные docs",
]
GREENFIELD_FORBIDDEN_USER_PHRASES = [
    "GitHub repo создан",
    "GitHub repo/access",
    "<repo-owner>",
    "<repo-name>",
    "пользователь должен сам создать GitHub repo",
    "сам создать GitHub repo",
    "сам клонировать",
    "сам добавлять origin",
    "пользователь делает initial commit/push",
    "Сообщить Codex название",
    "сообщить Codex название",
]
GREENFIELD_FORBIDDEN_CHATGPT_UI_AUTOMATION_CLAIMS = [
    "Codex создает ChatGPT Project",
    "Codex создаёт ChatGPT Project",
    "Codex создает battle ChatGPT Project",
    "Codex создаёт battle ChatGPT Project",
    "Codex создает боевой ChatGPT Project",
    "Codex создаёт боевой ChatGPT Project",
    "Codex вставляет instruction",
    "Codex вставляет repo-first instruction",
    "Codex сохраняет настройки",
    "Codex opens Project settings",
    "Codex inserts ChatGPT Project instructions",
    "Codex saves ChatGPT Project instructions",
    "Codex creates ChatGPT Project",
]
GREENFIELD_REQUIRED_USER_TOKENS = [
    "GF-000",
    "GF-005",
    "GF-010",
    "GF-015",
    "GF-020",
    "GF-030",
    "GF-040",
    "GF-050",
    "GF-060",
    "GF-070",
    "GF-080",
    "GF-090",
    "GF-100",
    "ChatGPT Project шаблона фабрики",
    "новый проект",
    "опрос",
    "default-decision",
    "recommendation-first",
    "стартовый Codex handoff",
    "template-repo/scenario-pack/00-master-router.md",
    "Readiness checklist",
    "боевого ChatGPT Project",
    "Factory-template ChatGPT Project остается",
    "Пользователь не создает GitHub repo",
    "не выбирает slug/repo name вручную",
    "не создает VPS project root",
    "не запускает launcher/wizard",
    "открывает Project settings/instructions",
    "сохраняет настройки",
    "Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст.",
]
GREENFIELD_LEGACY_USER_TOKENS = [
    "создает ChatGPT Project",
    "вставляет готовую repo-first instruction",
]
GREENFIELD_REQUIRED_CHECKLIST_IDS = [
    "GF-000",
    "GF-005",
    "GF-010",
    "GF-015",
    "GF-020",
    "GF-030",
    "GF-040",
    "GF-050",
    "GF-060",
    "GF-070",
    "GF-080",
    "GF-090",
    "GF-100",
]
GREENFIELD_REQUIRED_CHECKLIST_TOKENS = [
    "ChatGPT Project шаблона фабрики",
    "`новый проект`",
    "Default decision mode selected",
    "Defaults accepted or overridden",
    "custom overrides captured",
    "Опрос завершен",
    "Readiness state",
    "Handoff block",
    "Handoff receipt",
    "Repo URL, verify, sync",
    "Saved instruction",
    "Project settings/instructions",
    "создан пользователем",
]
GREENFIELD_REQUIRED_CODEX_TOKENS = [
    "ChatGPT-generated handoff",
    "не голое название проекта",
    "не проводить заново весь пользовательский опрос",
    "Нормализовать project slug",
    "создать GitHub repo",
    "Создать/подготовить VPS project root",
    "first-project-wizard.py",
    "Materialize repo-first core",
    "Добавить `origin`",
    "initial commit/push",
    "bash scripts/verify-all.sh quick",
    "verified sync",
    "готовую repo-first instruction",
    "готовый текст repo-first instruction",
    "пошаговую инструкцию пользователю",
    "Пользователь создает ChatGPT Project в UI и вставляет готовый текст",
]
GREENFIELD_DASHBOARD_REQUIRED_FIELDS = [
    "intake_channel",
    "trigger_command",
    "default_decision_mode",
    "defaults_count",
    "overrides_count",
    "unresolved_decisions_count",
    "next_decision",
    "readiness_to_generate_handoff",
    "handoff_ready",
    "codex_takeover_ready",
    "battle_chatgpt_project_created",
    "battle_repo_created_by",
    "chatgpt_project_ui_owner",
    "repo_first_instruction_prepared_by",
    "repo_first_instruction_pasted_by",
]
DEFAULT_DECISION_DASHBOARD_FIELDS = [
    "default_decision_mode",
    "defaults_count",
    "overrides_count",
    "unresolved_decisions_count",
    "next_decision",
    "readiness_to_generate_handoff",
]
SOFTWARE_UPDATE_GOVERNANCE_TOKENS = [
    "software-update-governance",
    "software-inventory.yaml",
    "software-update-watchlist.yaml",
    "software-update-readiness.yaml",
    "reports/software-updates/README.md",
    "manual-approved-upgrade",
    "unattended-upgrades",
    "Ubuntu LTS",
    "provider image id",
    "later package update state",
    "Docker/Compose",
    "Node/Python",
    "GitHub Actions",
    "base Docker images/tags/digests",
    "critical runtime dependencies",
    "auto-install без approval",
    "migration/upgrade project",
]
DEFAULT_DECISION_CONTRACT_TOKENS = [
    "Beginner questionnaires must be recommendation-first",
    "Blank expert-only questions are forbidden if safe defaults exist",
    "Every default must be explainable and overrideable",
    "global-defaults mode",
    "per-question-default mode",
    "Risky, paid, destructive, security, privacy, legal, secret-related decisions still require explicit user confirmation",
]
DEFAULT_DECISION_STATE_TOKENS = [
    "default_decision_mode",
    "accepted_defaults",
    "overridden_defaults",
    "default_source_basis",
    "uncertainty_notes",
    "decisions_requiring_user_confirmation",
]
FORCED_DEFAULT_RE = re.compile(
    r"(?i)(default|по умолчанию|recommended default|рекомендац).{0,160}(forced|без override|нельзя изменить|always|обязательно принимается|автоматически принимается)"
)


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
    if normalized.startswith("-"):
        return True
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
        "Контролируемые обновления ПО",
        "manual-approved-upgrade",
        "unattended-upgrades",
    ]:
        if token not in contract:
            errors.append(f"package contract не содержит обязательный маркер `{token}`")
    for token in DEFAULT_DECISION_CONTRACT_TOKENS:
        if token not in contract:
            errors.append(f"package contract не содержит default-decision contract marker `{token}`")
    for token in DEFAULT_DECISION_STATE_TOKENS:
        if token not in contract:
            errors.append(f"package contract не содержит default-decision state marker `{token}`")

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
        for token in SOFTWARE_UPDATE_GOVERNANCE_TOKENS:
            if token not in combined:
                errors.append(f"`{package}` не содержит software update governance marker `{token}`")
        if "02-codex-runbook.md" in PACKAGE_FILES:
            codex_path = package_dir / "02-codex-runbook.md"
            if codex_path.exists():
                codex_text = read(codex_path)
                if package == "01-factory-template" and "Язык ответа Codex: русский" not in codex_text:
                    errors.append("factory-template Codex runbook не содержит language contract")
                if "уже открыт" in codex_text and "не является" not in codex_text:
                    errors.append(f"`{codex_path}` может содержать fake already-open session switch wording")


STEP_RE = re.compile(r"^###\s+([A-Z]+-[0-9]+[A-Z]?)\.\s+(.+)$", re.MULTILINE)
CHECKLIST_ID_RE = re.compile(r"^\|\s*([A-Z]+-[0-9]+[A-Z]?)\s*\|", re.MULTILINE)


def extract_step_sections(text: str) -> dict[str, str]:
    matches = list(STEP_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[start:end]
    return sections


def extract_checklist_ids(text: str) -> set[str]:
    ids: set[str] = set()
    for match in CHECKLIST_ID_RE.finditer(text):
        step_id = match.group(1)
        if step_id not in {"ID"}:
            ids.add(step_id)
    return ids


def validate_step_cards(path: Path, sections: dict[str, str], errors: list[str]) -> None:
    for step_id, section in sorted(sections.items()):
        missing_fields = [field for field in BEGINNER_STEP_FIELDS if field not in section]
        if missing_fields:
            errors.append(f"`{path}` шаг `{step_id}` не содержит поля: {', '.join(missing_fields)}")
        if "- Команды для копирования:" not in section and "UI path" not in section:
            errors.append(f"`{path}` шаг `{step_id}` не содержит `Команды для копирования` или UI path")


def validate_checklist_mirror(user_path: Path, checklist_path: Path, user_text: str, checklist_text: str, errors: list[str]) -> None:
    user_sections = extract_step_sections(user_text)
    checklist_ids = extract_checklist_ids(checklist_text)
    if not checklist_ids:
        errors.append(f"`{checklist_path}` не содержит табличные user step IDs")
        return
    missing_in_checklist = sorted(set(user_sections) - checklist_ids)
    extra_in_checklist = sorted(checklist_ids - set(user_sections))
    if missing_in_checklist:
        errors.append(f"`{checklist_path}` не содержит user-runbook шаги: {', '.join(missing_in_checklist)}")
    if extra_in_checklist:
        errors.append(f"`{checklist_path}` содержит ID без user-runbook шага: {', '.join(extra_in_checklist)}")
    for phrase in FORBIDDEN_USER_CHECKLIST_PHRASES:
        if phrase in checklist_text:
            errors.append(f"`{checklist_path}` содержит запрещенную meta-policy фразу `{phrase}`")
    for column in ["ID", "Статус [ ]", "Окно", "Кто делает", "Действие", "Команда / UI path", "Ожидаемый результат", "Evidence", "Следующий шаг"]:
        if column not in checklist_text:
            errors.append(f"`{checklist_path}` не содержит колонку `{column}`")


def validate_default_decision_layer(package: str, package_dir: Path, combined: str, errors: list[str]) -> None:
    for token in DEFAULT_DECISION_STATE_TOKENS:
        if token not in combined:
            errors.append(f"`{package}` не содержит default-decision state token `{token}`")
    for token in ["recommendation-first", "defaults accepted or overridden"]:
        if token not in combined.lower():
            errors.append(f"`{package}` не содержит default-decision UX marker `{token}`")
    if FORCED_DEFAULT_RE.search(combined) and not re.search(r"(?i)(override|overrideable|переопредел|свой вариант|можно заменить)", combined):
        errors.append(f"`{package}` содержит forced default wording без override path")
    risky_default = re.search(
        r"(?i)(risky|paid|destructive|security|privacy|legal|secret).{0,120}(silently default|auto-accept|auto-accepted|автопринима|silently)",
        combined,
    )
    if risky_default:
        window = combined[max(0, risky_default.start() - 40) : risky_default.end() + 40].lower()
        if not any(negation in window for negation in ["не ", "not ", "нельзя", "forbidden", "запрещ"]):
            errors.append(f"`{package}` может silent-default risky/paid/destructive/security/privacy/legal/secret decision")

    if package == "02-greenfield-product":
        for token in [
            "Рекомендация по умолчанию",
            "Enter / \"по умолчанию\"",
            "GitHub repo visibility default",
            "VPS root path default",
            "verification mode default",
            "no hidden forced defaults for risky actions",
        ]:
            if token not in combined:
                errors.append(f"`{package}` не содержит greenfield default-decision marker `{token}`")
    if package == "03-brownfield-with-repo-to-greenfield":
        for token in [
            "keep existing repo as canonical root",
            "do not overwrite product-owned code",
            "evidence-first audit before remediation",
        ]:
            if token not in combined:
                errors.append(f"`{package}` не содержит brownfield-with-repo default marker `{token}`")
    if package == "04-brownfield-without-repo-to-greenfield":
        for token in [
            "/projects/<target-slug>/_incoming",
            "reconstructed/intermediate repos live only inside target project root",
            "evidence inventory",
        ]:
            if token not in combined:
                errors.append(f"`{package}` не содержит brownfield-without-repo default marker `{token}`")


def validate_beginner_flow(root: Path, errors: list[str]) -> None:
    base = root / PACKAGE_ROOT
    for package in PACKAGES:
        user_path = base / package / "01-user-runbook.md"
        codex_path = base / package / "02-codex-runbook.md"
        checklist_path = base / package / "03-checklist.md"
        if not user_path.exists() or not codex_path.exists():
            continue
        user_text = read(user_path)
        codex_text = read(codex_path)
        checklist_text = read(checklist_path) if checklist_path.exists() else ""
        package_combined = "\n".join([user_text, codex_text, checklist_text])
        validate_default_decision_layer(package, base / package, package_combined, errors)
        for marker in ["USER-ONLY SETUP", "CODEX-AUTOMATION"]:
            if marker not in user_text:
                errors.append(f"`{user_path}` не содержит beginner boundary `{marker}`")
            if marker not in codex_text:
                errors.append(f"`{codex_path}` не содержит automation boundary `{marker}`")
        if "takeover point" not in user_text.lower() and "takeover-точ" not in user_text.lower():
            errors.append(f"`{user_path}` не фиксирует Codex takeover point")
        if "Codex сам" not in user_text and "Codex выполняет" not in user_text:
            errors.append(f"`{user_path}` не отделяет Codex automation от user-only steps")
        step_sections = extract_step_sections(user_text)
        validate_step_cards(user_path, step_sections, errors)
        if checklist_text:
            validate_checklist_mirror(user_path, checklist_path, user_text, checklist_text, errors)
        if package == "01-factory-template":
            for step_id in FACTORY_REQUIRED_STEPS:
                if step_id not in user_text:
                    errors.append(f"`{user_path}` не содержит обязательный шаг `{step_id}`")
            for stale_step_id in ["FT-200", "FT-300", "FT-400", "FT-500"]:
                if stale_step_id in user_text or stale_step_id in checklist_text:
                    errors.append(f"`{package}` содержит устаревший шаг `{stale_step_id}`")
            for command in FACTORY_REQUIRED_COMMANDS:
                if command not in user_text:
                    errors.append(f"`{user_path}` не содержит обязательную команду/вывод `{command}`")
            for token in ["codex-app-remote-ssh", "vscode-remote-ssh-codex-extension", "FT-170", "Codex делает clone/setup/verify сам"]:
                if token not in user_text:
                    errors.append(f"`{user_path}` не содержит takeover/contour marker `{token}`")
            for placeholder in ["<VPS_IP>", "<GITHUB_USER>", "<server-hostname>", "<handoff block>"]:
                if placeholder not in user_text:
                    errors.append(f"`{user_path}` не объясняет placeholder `{placeholder}`")
            for token in FACTORY_CODEX_AUTOMATION_TOKENS:
                if token not in codex_text:
                    errors.append(f"`{codex_path}` не содержит automation step token `{token}`")
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
            for token in ["REMOTE_CONTEXT_MARKER", "do not paste into local Codex", "no hidden second shell step"]:
                if token not in package_combined:
                    errors.append(f"`{package}` не содержит beginner remote acceptance marker `{token}`")
        if package == "02-greenfield-product":
            greenfield_combined = "\n".join([user_text, codex_text, checklist_text])
            for token in GREENFIELD_REQUIRED_USER_TOKENS:
                if token not in user_text:
                    errors.append(f"`{user_path}` не содержит greenfield user-boundary token `{token}`")
            for token in GREENFIELD_LEGACY_USER_TOKENS:
                if token not in user_text:
                    errors.append(f"`{user_path}` не содержит greenfield external UI token `{token}`")
            for token in GREENFIELD_REQUIRED_CODEX_TOKENS:
                if token not in codex_text:
                    errors.append(f"`{codex_path}` не содержит greenfield Codex automation token `{token}`")
            checklist_ids = extract_checklist_ids(checklist_text)
            missing_greenfield_ids = sorted(set(GREENFIELD_REQUIRED_CHECKLIST_IDS) - checklist_ids)
            extra_greenfield_ids = sorted(checklist_ids - set(GREENFIELD_REQUIRED_CHECKLIST_IDS))
            if missing_greenfield_ids:
                errors.append(f"`{checklist_path}` не содержит greenfield checklist IDs: {', '.join(missing_greenfield_ids)}")
            if extra_greenfield_ids:
                errors.append(f"`{checklist_path}` содержит лишние greenfield checklist IDs: {', '.join(extra_greenfield_ids)}")
            ordered_ids = [match.group(1) for match in CHECKLIST_ID_RE.finditer(checklist_text) if match.group(1) != "ID"]
            if ordered_ids and ordered_ids != GREENFIELD_REQUIRED_CHECKLIST_IDS:
                errors.append(f"`{checklist_path}` содержит неверный порядок greenfield шагов: {', '.join(ordered_ids)}")
            for token in GREENFIELD_REQUIRED_CHECKLIST_TOKENS:
                if token not in checklist_text:
                    errors.append(f"`{checklist_path}` не содержит greenfield checklist token `{token}`")
            for phrase in GREENFIELD_FORBIDDEN_USER_PHRASES:
                if phrase in user_text or phrase in checklist_text:
                    errors.append(f"`{package}` user-facing файлы содержат запрещенную greenfield boundary phrase `{phrase}`")
            for phrase in GREENFIELD_FORBIDDEN_CHATGPT_UI_AUTOMATION_CLAIMS:
                if phrase in greenfield_combined:
                    errors.append(f"`{package}` содержит запрещенный claim о ChatGPT Project UI automation: `{phrase}`")
            for token in [
                "Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст.",
                "Открыть Project settings/instructions",
                "Сохранить настройки",
                "GitHub repo creation",
                "initial commit/push",
                "VPS project root",
                "verified sync",
                "REMOTE_CONTEXT_MARKER",
                "Do not paste into local Codex",
                "No hidden second shell step",
                "GF-050 continuity",
                "First project ready proof",
            ]:
                if token not in greenfield_combined:
                    errors.append(f"`{package}` не содержит greenfield ChatGPT UI boundary token `{token}`")


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
        for key in [
            "id",
            "path",
            "current_phase",
            "current_step",
            "active_contour",
            "takeover_ready",
            "checklist_path",
            "gates",
            "blockers",
            "next_action",
            "owner_boundary",
        ]:
            if key not in item:
                errors.append(f"runbook_packages[{package_id or index}] не содержит `{key}`")
        for key in DEFAULT_DECISION_DASHBOARD_FIELDS:
            if key not in item:
                errors.append(f"runbook_packages[{package_id or index}] не содержит default-decision field `{key}`")
        if "default_decision_mode" in item and str(item.get("default_decision_mode") or "") not in {
            "not_selected",
            "global-defaults",
            "confirm-each-default",
            "manual",
        }:
            errors.append(f"runbook package `{package_id}` содержит неизвестный default_decision_mode")
        for int_field in ["defaults_count", "overrides_count", "unresolved_decisions_count"]:
            if int_field in item and not isinstance(item.get(int_field), int):
                errors.append(f"runbook package `{package_id}` `{int_field}` должен быть integer")
        if "readiness_to_generate_handoff" in item and not isinstance(item.get("readiness_to_generate_handoff"), bool):
            errors.append(f"runbook package `{package_id}` readiness_to_generate_handoff должен быть boolean")
        if package_id and package_id not in PACKAGES:
            errors.append(f"dashboard содержит неизвестный runbook package `{package_id}`")
        if package_id == "02-greenfield-product":
            for field in GREENFIELD_DASHBOARD_REQUIRED_FIELDS:
                if field not in item:
                    errors.append(f"dashboard runbook package `{package_id}` не содержит `{field}`")
            if str(item.get("default_decision_mode") or "") not in {
                "not_selected",
                "global-defaults",
                "confirm-each-default",
                "manual",
            }:
                errors.append("greenfield dashboard default_decision_mode должен быть not_selected/global-defaults/confirm-each-default/manual")
            for int_field in ["defaults_count", "overrides_count", "unresolved_decisions_count"]:
                if not isinstance(item.get(int_field), int):
                    errors.append(f"greenfield dashboard `{int_field}` должен быть integer")
            if not str(item.get("next_decision") or "").strip():
                errors.append("greenfield dashboard next_decision обязателен")
            if not isinstance(item.get("readiness_to_generate_handoff"), bool):
                errors.append("greenfield dashboard readiness_to_generate_handoff должен быть boolean")
            if str(item.get("intake_channel") or "") != "factory-template-chatgpt-project":
                errors.append("greenfield dashboard intake_channel должен быть factory-template-chatgpt-project")
            if str(item.get("trigger_command") or "") != "новый проект":
                errors.append("greenfield dashboard trigger_command должен быть `новый проект`")
            if str(item.get("battle_repo_created_by") or "") != "codex":
                errors.append("greenfield dashboard battle_repo_created_by должен быть codex")
            if str(item.get("chatgpt_project_ui_owner") or "") != "user":
                errors.append("greenfield dashboard chatgpt_project_ui_owner должен быть user")
            if str(item.get("repo_first_instruction_prepared_by") or "") != "codex":
                errors.append("greenfield dashboard repo_first_instruction_prepared_by должен быть codex")
            if str(item.get("repo_first_instruction_pasted_by") or "") != "user":
                errors.append("greenfield dashboard repo_first_instruction_pasted_by должен быть user")
            for bool_field in ["handoff_ready", "codex_takeover_ready", "battle_chatgpt_project_created"]:
                if not isinstance(item.get(bool_field), bool):
                    errors.append(f"greenfield dashboard `{bool_field}` должен быть boolean")
        if str(item.get("owner_boundary") or "") != "internal-repo-follow-up":
            errors.append(f"runbook package `{package_id}` должен иметь owner_boundary internal-repo-follow-up")
        if not isinstance(item.get("gates"), list) or not item.get("gates"):
            errors.append(f"runbook package `{package_id}` должен содержать gates")
        if not isinstance(item.get("blockers"), list):
            errors.append(f"runbook package `{package_id}` blockers должен быть list")
        path = str(item.get("path") or "")
        if path and not (root / path).exists():
            errors.append(f"dashboard runbook package `{package_id}` ссылается на отсутствующий path `{path}`")
        checklist_path = str(item.get("checklist_path") or "")
        if checklist_path and not (root / checklist_path).exists():
            errors.append(f"dashboard runbook package `{package_id}` ссылается на отсутствующий checklist_path `{checklist_path}`")
        if str(item.get("active_contour") or "") not in {
            "not_selected",
            "codex-app-remote-ssh",
            "vscode-remote-ssh-codex-extension",
        }:
            errors.append(f"runbook package `{package_id}` содержит неизвестный active_contour")
        if not isinstance(item.get("takeover_ready"), bool):
            errors.append(f"runbook package `{package_id}` takeover_ready должен быть boolean")
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
