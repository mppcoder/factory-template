#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ipaddress
import os
import socket
from pathlib import Path


SECRET_PLACEHOLDERS = {
    "DB_PASSWORD": "change-me-generate-a-long-random-secret",
    "TLS_EMAIL": "REPLACE_ME_REAL_EMAIL_FOR_ACME",
}
PLACEHOLDER_VALUES = set(SECRET_PLACEHOLDERS.values()) | {
    "ops@example.com",
    "example@example.com",
}


def parse_env(path: Path) -> tuple[list[str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    values: dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return lines, values


def write_env(path: Path, lines: list[str], updates: dict[str, str]) -> None:
    seen: set[str] = set()
    output: list[str] = []
    for line in lines:
        if "=" in line and not line.lstrip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in updates:
                output.append(f"{key}={updates[key]}")
                seen.add(key)
                continue
        output.append(line)
    if output and output[-1] != "":
        output.append("")
    for key, value in updates.items():
        if key not in seen:
            output.append(f"{key}={value}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    path.chmod(0o600)


def derive_sslip_domain() -> str:
    candidates: list[str] = []
    try:
        candidates.extend(socket.gethostbyname_ex(socket.gethostname())[2])
    except OSError:
        pass
    candidates.extend(os.popen("hostname -I 2>/dev/null").read().split())
    for raw_ip in candidates:
        try:
            ip = ipaddress.ip_address(raw_ip)
        except ValueError:
            continue
        if ip.version == 4 and not (ip.is_private or ip.is_loopback or ip.is_link_local):
            return f"{str(ip).replace('.', '-')}.sslip.io"
    return "REPLACE_ME_REAL_DOMAIN"


def is_missing_or_placeholder(values: dict[str, str], key: str) -> bool:
    value = values.get(key, "").strip()
    return not value or value in PLACEHOLDER_VALUES or "REPLACE_ME" in value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare non-secret production deploy env defaults and leave only secrets/manual values for the operator.",
    )
    parser.add_argument("--env-file", default="deploy/.env")
    parser.add_argument("--domain", default=None)
    parser.add_argument("--backup-path", default="/var/backups/factory-template-postgres")
    parser.add_argument("--app-image", default="nginx:1.27-alpine")
    parser.add_argument("--app-pull-policy", default=None)
    parser.add_argument(
        "--placeholder-image-url",
        default="/placeholder.svg",
        help="Use a generated static placeholder page and set its image URL. Pass an external URL if you want the placeholder page to reference a custom image.",
    )
    parser.add_argument("--no-placeholder", action="store_true", help="Do not set placeholder mode fields.")
    parser.add_argument("--db-name", default="factory_template")
    parser.add_argument("--db-user", default="factory_template")
    args = parser.parse_args()

    env_path = Path(args.env_file)
    if not env_path.exists():
        example = env_path.with_name(".env.example")
        if example.exists():
            env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            env_path.write_text("", encoding="utf-8")

    lines, values = parse_env(env_path)
    domain = args.domain or derive_sslip_domain()
    updates = {
        "OPERATOR_PRESET": "production",
        "APP_IMAGE": values.get("APP_IMAGE") or args.app_image,
        "APP_PULL_POLICY": values.get("APP_PULL_POLICY") or args.app_pull_policy or "always",
        "APP_BIND_ADDRESS": "127.0.0.1",
        "DB_NAME": values.get("DB_NAME") or args.db_name,
        "DB_USER": values.get("DB_USER") or args.db_user,
        "BACKUP_ENABLED": "true",
        "BACKUP_PATH": args.backup_path,
        "BACKUP_RETENTION_DAYS": values.get("BACKUP_RETENTION_DAYS") or "7",
        "DOMAIN": values.get("DOMAIN") if values.get("DOMAIN") not in {"", "example.com"} else domain,
        "ACME_AGREE": "true",
    }
    if not args.no_placeholder:
        updates["APP_PLACEHOLDER_MODE"] = "static"
        updates["APP_PLACEHOLDER_IMAGE_URL"] = args.placeholder_image_url
    for key, placeholder in SECRET_PLACEHOLDERS.items():
        if is_missing_or_placeholder(values, key):
            updates[key] = placeholder

    write_env(env_path, lines, updates)
    Path(args.backup_path).mkdir(parents=True, exist_ok=True)
    Path(args.backup_path).chmod(0o700)

    _, final_values = parse_env(env_path)
    remaining = [
        key
        for key in SECRET_PLACEHOLDERS
        if is_missing_or_placeholder(final_values, key)
    ]
    print("production_env_defaults_prepared=true")
    print(f"env_file={env_path}")
    print(f"backup_path={args.backup_path}")
    print(f"domain={final_values.get('DOMAIN', '')}")
    if not args.no_placeholder:
        print(f"placeholder_image_url={final_values.get('APP_PLACEHOLDER_IMAGE_URL', '')}")
    print("remaining_user_fields=" + (",".join(remaining) if remaining else "none"))
    if final_values.get("APP_IMAGE", "").startswith("nginx:"):
        print("warning=APP_IMAGE is demo nginx; runtime proof is infrastructure-level until a real app image is set.")
        print("hint=run build-placeholder-app-image.py to generate a local placeholder APP_IMAGE when no real application image exists yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
