#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from dataclasses import dataclass
from pathlib import Path


VALID_PRESETS = {"starter", "app-db", "reverse-proxy", "production"}
PRESET_COMPOSE_FILES = {
    "starter": [],
    "app-db": ["deploy/presets/app-db.yaml"],
    "reverse-proxy": ["deploy/presets/reverse-proxy.yaml"],
    "production": ["deploy/presets/app-db.yaml", "deploy/presets/reverse-proxy.yaml"],
}
SECRET_PLACEHOLDERS = {
    "",
    "change-me",
    "changeme",
    "password",
    "secret",
    "example",
    "change-me-generate-a-long-random-secret",
}


@dataclass(frozen=True)
class Finding:
    level: str
    key: str
    message: str


def detect_repo_root() -> Path:
    script = Path(__file__).resolve()
    for parent in script.parents:
        if (parent / "deploy").exists() and (parent / "template-repo" / "scripts").exists():
            return parent
        if (parent / "deploy").exists() and (parent / "scripts").exists():
            return parent
    return Path.cwd().resolve()


def parse_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        env[key.strip()] = value
    return env


def as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def valid_port(value: str) -> bool:
    try:
        port = int(value)
    except ValueError:
        return False
    return 1 <= port <= 65535


def valid_positive_int(value: str) -> bool:
    try:
        number = int(value)
    except ValueError:
        return False
    return number > 0


def is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in SECRET_PLACEHOLDERS:
        return True
    return normalized.startswith("change-me") or normalized.endswith("@example.com")


def validate_domain(value: str) -> bool:
    if not value or value in {"localhost", "example.com"}:
        return False
    if re.search(r"\s", value):
        return False
    if "." not in value:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9.-]+", value))


def validate_bind_address(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return value in {"localhost"}


def add(findings: list[Finding], level: str, key: str, message: str) -> None:
    findings.append(Finding(level=level, key=key, message=message))


def validate(root: Path, env_path: Path, requested_preset: str | None, allow_placeholders: bool) -> tuple[str, list[Finding]]:
    env = parse_env_file(env_path)
    preset = requested_preset or env.get("OPERATOR_PRESET") or "starter"
    findings: list[Finding] = []

    if preset not in VALID_PRESETS:
        add(findings, "fail", "OPERATOR_PRESET", f"Неизвестный preset `{preset}`. Используйте один из: {', '.join(sorted(VALID_PRESETS))}.")
        return preset, findings

    for rel in ["deploy/compose.yaml", "deploy/compose.production.yaml", *PRESET_COMPOSE_FILES[preset]]:
        if not (root / rel).exists():
            add(findings, "fail", rel, f"Отсутствует обязательный compose artifact `{rel}`.")

    if not env_path.exists():
        add(findings, "fail", "env_file", f"Env file не найден: {env_path}.")
        return preset, findings

    app_image = env.get("APP_IMAGE", "nginx:1.27-alpine")
    if not app_image:
        add(findings, "fail", "APP_IMAGE", "APP_IMAGE не должен быть пустым.")
    elif preset != "starter" and app_image in {"nginx:1.27-alpine", "public.ecr.aws/nginx/nginx:stable"}:
        add(findings, "warn", "APP_IMAGE", "Production presets должны использовать явный application image, а не demo nginx image.")

    app_port = env.get("APP_PORT", "8080")
    if not valid_port(app_port):
        add(findings, "fail", "APP_PORT", "APP_PORT должен быть TCP port от 1 до 65535.")

    bind_address = env.get("APP_BIND_ADDRESS", "0.0.0.0")
    if not validate_bind_address(bind_address):
        add(findings, "fail", "APP_BIND_ADDRESS", "APP_BIND_ADDRESS должен быть IP address или localhost.")

    if preset in {"app-db", "production"}:
        db_password = env.get("DB_PASSWORD", "")
        if len(db_password) < 16:
            add(findings, "fail", "DB_PASSWORD", "DB_PASSWORD должен быть не короче 16 символов для app-db/production presets.")
        elif is_placeholder(db_password):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "DB_PASSWORD", "DB_PASSWORD все еще похож на example placeholder.")
        for key in ["DB_NAME", "DB_USER"]:
            if not env.get(key):
                add(findings, "fail", key, f"{key} обязателен для app-db/production presets.")
        db_port = env.get("DB_PORT", "5432")
        if not valid_port(db_port):
            add(findings, "fail", "DB_PORT", "DB_PORT должен быть TCP port от 1 до 65535.")
        retention = env.get("BACKUP_RETENTION_DAYS", "7")
        if not valid_positive_int(retention):
            add(findings, "fail", "BACKUP_RETENTION_DAYS", "BACKUP_RETENTION_DAYS должен быть положительным целым числом.")
        if as_bool(env.get("BACKUP_ENABLED", "false")) and not env.get("BACKUP_PATH"):
            add(findings, "fail", "BACKUP_PATH", "BACKUP_PATH обязателен, если BACKUP_ENABLED=true.")

    if preset in {"reverse-proxy", "production"}:
        domain = env.get("DOMAIN", "")
        tls_email = env.get("TLS_EMAIL", "")
        acme_agree = env.get("ACME_AGREE", "false")
        if not validate_domain(domain):
            level = "warn" if allow_placeholders and domain == "example.com" else "fail"
            add(findings, level, "DOMAIN", "DOMAIN должен быть реальным публичным hostname для reverse-proxy/production presets.")
        if "@" not in tls_email or is_placeholder(tls_email):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "TLS_EMAIL", "TLS_EMAIL должен быть реальным operator email для ACME/TLS уведомлений.")
        if not as_bool(acme_agree):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "ACME_AGREE", "Установите ACME_AGREE=true после принятия условий CA subscriber terms.")
        if bind_address != "127.0.0.1":
            add(findings, "warn", "APP_BIND_ADDRESS", "Для reverse-proxy/production установите APP_BIND_ADDRESS=127.0.0.1, чтобы app был доступен только через TLS proxy.")

    if preset == "starter":
        add(findings, "ok", "OPERATOR_PRESET", "Выбран starter preset; DB/TLS secrets опциональны и не обязательны.")
    else:
        add(findings, "ok", "OPERATOR_PRESET", f"Выбран {preset} preset; optional production checks активны.")

    return preset, findings


def print_text(preset: str, findings: list[Finding]) -> None:
    print("Проверка operator env")
    print("-" * 72)
    print(f"Preset: {preset}")
    for finding in findings:
        print(f"[{finding.level.upper()}] {finding.key}: {finding.message}")


def print_report(preset: str, findings: list[Finding]) -> None:
    failures = sum(1 for finding in findings if finding.level == "fail")
    warnings = sum(1 for finding in findings if finding.level == "warn")
    print(f"preset={preset}")
    print(f"status={'fail' if failures else 'pass'}")
    print(f"failures={failures}")
    print(f"warnings={warnings}")
    for index, finding in enumerate(findings, 1):
        print(f"finding_{index}={finding.level}:{finding.key}:{finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверить operator deploy env для starter и optional production presets.")
    parser.add_argument("root", nargs="?", default=None, help="Корень repo")
    parser.add_argument("--env-file", help="Env file для проверки. По умолчанию deploy/.env или deploy/.env.example.")
    parser.add_argument("--preset", choices=sorted(VALID_PRESETS), help="Переопределить OPERATOR_PRESET из env.")
    parser.add_argument("--allow-example-placeholders", action="store_true", help="Понизить ошибки example secrets/domain до предупреждений.")
    parser.add_argument("--format", choices=["text", "report"], default="text")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else detect_repo_root()
    if args.env_file:
        env_path = Path(args.env_file).resolve()
    elif (root / "deploy" / ".env").exists():
        env_path = root / "deploy" / ".env"
    else:
        env_path = root / "deploy" / ".env.example"

    preset, findings = validate(root, env_path, args.preset, args.allow_example_placeholders)
    if args.format == "report":
        print_report(preset, findings)
    else:
        print_text(preset, findings)
    return 1 if any(finding.level == "fail" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
