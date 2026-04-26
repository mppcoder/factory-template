#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from dataclasses import dataclass
from pathlib import Path


VALID_PRESETS = {"starter", "app-db", "reverse-proxy-tls", "reverse-proxy", "backup", "healthcheck", "production"}
PRESET_ORDER = ["app-db", "reverse-proxy-tls", "backup", "healthcheck"]
PRESET_ALIASES = {
    "reverse-proxy": ["reverse-proxy-tls"],
    "production": ["app-db", "reverse-proxy-tls", "backup", "healthcheck"],
}
PRESET_COMPOSE_FILES = {
    "starter": ["deploy/presets/starter.yaml"],
    "app-db": ["deploy/presets/app-db.yaml"],
    "reverse-proxy-tls": ["deploy/presets/reverse-proxy-tls.yaml"],
    "backup": ["deploy/presets/backup.yaml"],
    "healthcheck": ["deploy/presets/healthcheck.yaml"],
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


def valid_duration(value: str) -> bool:
    return bool(re.fullmatch(r"[1-9][0-9]*(ms|s|m|h)", value.strip()))


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


def validate_volume_name(value: str) -> bool:
    return bool(value) and bool(re.fullmatch(r"[A-Za-z0-9_.-]+", value))


def validate_backup_path(value: str) -> bool:
    if not value or value.strip() in {"/", "."}:
        return False
    return not re.search(r"[\x00\r\n]", value)


def validate_healthcheck_endpoint(value: str) -> bool:
    if not value or re.search(r"\s", value):
        return False
    if value.startswith("/"):
        return True
    return bool(re.fullmatch(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+", value))


def parse_preset_expression(value: str) -> tuple[list[str], list[str]]:
    raw_parts = [part.strip() for part in re.split(r"[,+]", value or "starter") if part.strip()]
    if not raw_parts:
        raw_parts = ["starter"]

    tokens: list[str] = []
    unknown: list[str] = []
    for part in raw_parts:
        if part in PRESET_ALIASES:
            expanded = PRESET_ALIASES[part]
        elif part in VALID_PRESETS:
            expanded = [part]
        else:
            unknown.append(part)
            continue
        for token in expanded:
            if token != "starter" and token not in tokens:
                tokens.append(token)

    if not tokens:
        tokens = ["starter"]
    else:
        tokens = [token for token in PRESET_ORDER if token in tokens]
    return tokens, unknown


def add(findings: list[Finding], level: str, key: str, message: str) -> None:
    findings.append(Finding(level=level, key=key, message=message))


def validate(root: Path, env_path: Path, requested_preset: str | None, allow_placeholders: bool) -> tuple[str, list[Finding]]:
    env = parse_env_file(env_path)
    preset = requested_preset or env.get("OPERATOR_PRESET") or "starter"
    preset_tokens, unknown_presets = parse_preset_expression(preset)
    findings: list[Finding] = []

    if unknown_presets:
        add(findings, "fail", "OPERATOR_PRESET", f"Неизвестный preset: {', '.join(unknown_presets)}. Используйте starter, app-db, reverse-proxy-tls, backup, healthcheck или production.")
        return preset, findings

    required_compose = ["deploy/compose.yaml", "deploy/compose.production.yaml"]
    for token in preset_tokens:
        required_compose.extend(PRESET_COMPOSE_FILES[token])
    for rel in required_compose:
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

    for key, default in [("APP_PORT", "8080")]:
        if not valid_port(env.get(key, default)):
            add(findings, "fail", key, f"{key} должен быть TCP port от 1 до 65535.")

    bind_address = env.get("APP_BIND_ADDRESS", "0.0.0.0")
    if not validate_bind_address(bind_address):
        add(findings, "fail", "APP_BIND_ADDRESS", "APP_BIND_ADDRESS должен быть IP address или localhost.")

    app_volume = env.get("APP_DATA_VOLUME", "factory-template-app-data")
    if not validate_volume_name(app_volume):
        add(findings, "fail", "APP_DATA_VOLUME", "APP_DATA_VOLUME должен быть безопасным Docker volume name.")

    health_endpoint = env.get("HEALTHCHECK_ENDPOINT") or env.get("APP_HEALTHCHECK_ENDPOINT") or env.get("APP_HEALTHCHECK_PATH", "/")
    if not validate_healthcheck_endpoint(health_endpoint):
        add(findings, "fail", "HEALTHCHECK_ENDPOINT", "Healthcheck endpoint должен быть HTTP path вроде `/health` или полный http(s) URL без пробелов.")
    for key, default in [
        ("APP_HEALTHCHECK_INTERVAL", "30s"),
        ("APP_HEALTHCHECK_TIMEOUT", "5s"),
        ("APP_HEALTHCHECK_START_PERIOD", "20s"),
    ]:
        if not valid_duration(env.get(key, default)):
            add(findings, "fail", key, f"{key} должен быть duration вроде 30s, 5s или 1m.")
    if not valid_positive_int(env.get("APP_HEALTHCHECK_RETRIES", "3")):
        add(findings, "fail", "APP_HEALTHCHECK_RETRIES", "APP_HEALTHCHECK_RETRIES должен быть положительным целым числом.")

    uses_db = "app-db" in preset_tokens or "backup" in preset_tokens
    uses_backup = "backup" in preset_tokens
    uses_tls = "reverse-proxy-tls" in preset_tokens

    if uses_db:
        db_password = env.get("DB_PASSWORD", "")
        if len(db_password) < 16:
            add(findings, "fail", "DB_PASSWORD", "DB_PASSWORD должен быть не короче 16 символов для app-db/backup presets.")
        elif is_placeholder(db_password):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "DB_PASSWORD", "DB_PASSWORD все еще похож на example placeholder.")
        for key in ["DB_NAME", "DB_USER"]:
            if not env.get(key):
                add(findings, "fail", key, f"{key} обязателен для app-db/production presets.")
        db_port = env.get("DB_PORT", "5432")
        if not valid_port(db_port):
            add(findings, "fail", "DB_PORT", "DB_PORT должен быть TCP port от 1 до 65535.")
        db_volume = env.get("DB_DATA_VOLUME", "factory-template-db-data")
        if not validate_volume_name(db_volume):
            add(findings, "fail", "DB_DATA_VOLUME", "DB_DATA_VOLUME должен быть безопасным Docker volume name.")

    if uses_backup and "app-db" not in preset_tokens:
        add(findings, "fail", "OPERATOR_PRESET", "Preset `backup` требует `app-db`, например OPERATOR_PRESET=app-db,backup.")
    if uses_backup or as_bool(env.get("BACKUP_ENABLED", "false")):
        if uses_backup and not as_bool(env.get("BACKUP_ENABLED", "false")):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "BACKUP_ENABLED", "Для активного `backup` preset установите BACKUP_ENABLED=true.")
        retention = env.get("BACKUP_RETENTION_DAYS", "7")
        if not valid_positive_int(retention):
            add(findings, "fail", "BACKUP_RETENTION_DAYS", "BACKUP_RETENTION_DAYS должен быть положительным целым числом.")
        backup_path = env.get("BACKUP_PATH", "")
        if not validate_backup_path(backup_path):
            add(findings, "fail", "BACKUP_PATH", "BACKUP_PATH должен быть непустым безопасным host path и не должен указывать на корень filesystem.")

    if uses_tls:
        domain = env.get("DOMAIN", "")
        tls_email = env.get("TLS_EMAIL", "")
        acme_agree = env.get("ACME_AGREE", "false")
        if not validate_domain(domain):
            level = "warn" if allow_placeholders and domain == "example.com" else "fail"
            add(findings, level, "DOMAIN", "DOMAIN должен быть реальным публичным hostname для reverse-proxy-tls/production presets.")
        if "@" not in tls_email or is_placeholder(tls_email):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "TLS_EMAIL", "TLS_EMAIL должен быть реальным operator email для ACME/TLS уведомлений.")
        if not as_bool(acme_agree):
            level = "warn" if allow_placeholders else "fail"
            add(findings, level, "ACME_AGREE", "Установите ACME_AGREE=true после принятия условий CA subscriber terms.")
        for key, default in [("HTTP_PORT", "80"), ("HTTPS_PORT", "443")]:
            if not valid_port(env.get(key, default)):
                add(findings, "fail", key, f"{key} должен быть TCP port от 1 до 65535.")
        if env.get("HTTP_PORT", "80") == env.get("HTTPS_PORT", "443"):
            add(findings, "fail", "HTTP_PORT/HTTPS_PORT", "HTTP_PORT и HTTPS_PORT не должны совпадать.")
        for key, default in [
            ("CADDY_DATA_VOLUME", "factory-template-caddy-data"),
            ("CADDY_CONFIG_VOLUME", "factory-template-caddy-config"),
        ]:
            if not validate_volume_name(env.get(key, default)):
                add(findings, "fail", key, f"{key} должен быть безопасным Docker volume name.")
        if bind_address != "127.0.0.1":
            add(findings, "warn", "APP_BIND_ADDRESS", "Для reverse-proxy-tls/production установите APP_BIND_ADDRESS=127.0.0.1, чтобы app был доступен только через TLS proxy.")

    if preset_tokens == ["starter"]:
        add(findings, "ok", "OPERATOR_PRESET", "Выбран starter preset; DB/TLS secrets опциональны и не обязательны.")
    else:
        add(findings, "ok", "OPERATOR_PRESET", f"Выбран preset `{preset}`; активные overlays: {', '.join(preset_tokens)}.")

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
    print(f"preset_tokens={','.join(parse_preset_expression(preset)[0])}")
    print(f"status={'fail' if failures else 'pass'}")
    print(f"failures={failures}")
    print(f"warnings={warnings}")
    for index, finding in enumerate(findings, 1):
        print(f"finding_{index}={finding.level}:{finding.key}:{finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверить operator deploy env для starter и optional production presets.")
    parser.add_argument("root", nargs="?", default=None, help="Корень repo")
    parser.add_argument("--env-file", help="Env file для проверки. По умолчанию deploy/.env или deploy/.env.example.")
    parser.add_argument("--preset", help="Переопределить OPERATOR_PRESET из env. Можно указать starter, app-db, reverse-proxy-tls, backup, healthcheck, production или список через запятую.")
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
