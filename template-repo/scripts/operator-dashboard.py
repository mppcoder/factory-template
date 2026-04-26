#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class StatusRow:
    title: str
    status: str  # ok | warn | fail
    details: str


STATUS_LABEL = {
    "ok": "OK",
    "warn": "ВНИМАНИЕ",
    "fail": "НУЖНО ИСПРАВИТЬ",
}

PRESET_COMPOSE_FILES = {
    "starter": ["deploy/presets/starter.yaml"],
    "app-db": ["deploy/presets/app-db.yaml"],
    "reverse-proxy-tls": ["deploy/presets/reverse-proxy-tls.yaml"],
    "backup": ["deploy/presets/backup.yaml"],
    "healthcheck": ["deploy/presets/healthcheck.yaml"],
}
PRESET_ORDER = ["app-db", "reverse-proxy-tls", "backup", "healthcheck"]
PRESET_ALIASES = {
    "reverse-proxy": ["reverse-proxy-tls"],
    "production": ["app-db", "reverse-proxy-tls", "backup", "healthcheck"],
}


def detect_repo_root() -> Path:
    script = Path(__file__).resolve()
    for parent in script.parents:
        if (parent / "template-repo" / "scripts").exists() and (parent / "README.md").exists():
            return parent
        if (parent / "scripts").exists() and (parent / ".chatgpt").exists():
            return parent
    return Path.cwd().resolve()


def script_path(root: Path, name: str) -> Path:
    source_path = root / "template-repo" / "scripts" / name
    if source_path.exists():
        return source_path
    return root / "scripts" / name


def script_hint(root: Path, name: str) -> str:
    source_hint = root / "template-repo" / "scripts" / name
    if source_hint.exists():
        return f"template-repo/scripts/{name}"
    return f"scripts/{name}"


def parse_report(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def active_env(root: Path) -> tuple[Path | None, str]:
    env_file = root / "deploy" / ".env"
    env_example = root / "deploy" / ".env.example"
    if env_file.exists():
        return env_file, "custom"
    if env_example.exists():
        return env_example, "example"
    return None, "missing"


def selected_preset(root: Path, preset_override: str | None = None) -> str:
    if preset_override:
        return preset_override
    env_path, _mode = active_env(root)
    env = parse_env_file(env_path) if env_path else {}
    return env.get("OPERATOR_PRESET") or "starter"


def parse_preset_expression(value: str) -> tuple[list[str], list[str]]:
    raw_parts = [part.strip() for part in re.split(r"[,+]", value or "starter") if part.strip()]
    if not raw_parts:
        raw_parts = ["starter"]
    tokens: list[str] = []
    unknown: list[str] = []
    valid = {"starter", "app-db", "reverse-proxy-tls", "reverse-proxy", "backup", "healthcheck", "production"}
    for part in raw_parts:
        if part in PRESET_ALIASES:
            expanded = PRESET_ALIASES[part]
        elif part in valid:
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


def validate_operator_env(root: Path, env_path: Path | None, env_mode: str, preset: str) -> dict[str, str]:
    if env_path is None:
        return {"status": "fail", "failures": "1", "warnings": "0"}
    validator = script_path(root, "validate-operator-env.py")
    if not validator.exists():
        return {"status": "fail", "failures": "1", "warnings": "0"}
    command = [
        sys.executable,
        str(validator),
        str(root),
        "--env-file",
        str(env_path),
        "--preset",
        preset,
        "--format",
        "report",
    ]
    if env_mode == "example":
        command.append("--allow-example-placeholders")
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    data: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    if not data:
        data["status"] = "fail"
        data["failures"] = "1"
        data["warnings"] = "0"
    return data


def _compose_status() -> tuple[str, str]:
    if shutil.which("docker"):
        proc = subprocess.run(
            ["docker", "compose", "version"],
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0:
            return "ok", "Доступен `docker compose`."
    if shutil.which("docker-compose"):
        return "warn", "Доступен только legacy `docker-compose` (рекомендуется `docker compose`)."
    return "fail", "Не найден Docker Compose (`docker compose` или `docker-compose`)."


def build_status_rows(root: Path, preset_override: str | None = None) -> list[StatusRow]:
    compose_base = root / "deploy" / "compose.yaml"
    compose_prod = root / "deploy" / "compose.production.yaml"
    env_path, env_mode = active_env(root)
    verify_summary = root / "VERIFY_SUMMARY.md"
    dry_run_report = root / ".factory-runtime" / "reports" / "deploy-dry-run-latest.txt"
    deploy_report = root / ".factory-runtime" / "reports" / "deploy-last-run.txt"
    preset = selected_preset(root, preset_override)
    preset_tokens, unknown_presets = parse_preset_expression(preset)

    rows: list[StatusRow] = []

    missing_compose = [str(p.relative_to(root)) for p in [compose_base, compose_prod] if not p.exists()]
    if missing_compose:
        rows.append(
            StatusRow(
                title="Deploy baseline",
                status="fail",
                details=f"Не хватает файлов: {', '.join(missing_compose)}.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Deploy baseline",
                status="ok",
                details="`deploy/compose.yaml` и `deploy/compose.production.yaml` на месте.",
            )
        )

    if env_mode == "custom" and env_path is not None:
        rows.append(
            StatusRow(
                title="Environment файл",
                status="ok",
                details="Найден `deploy/.env` (используются ваши переменные окружения).",
            )
        )
    elif env_mode == "example" and env_path is not None:
        rows.append(
            StatusRow(
                title="Environment файл",
                status="warn",
                details="`deploy/.env` не найден, будет использован безопасный пример `deploy/.env.example`.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Environment файл",
                status="fail",
                details="Нет ни `deploy/.env`, ни `deploy/.env.example`.",
            )
        )

    if unknown_presets:
        rows.append(
            StatusRow(
                title="Operator preset",
                status="fail",
                details=f"Неизвестный preset: {', '.join(unknown_presets)}. Допустимо: starter, app-db, reverse-proxy-tls, backup, healthcheck, production.",
            )
        )
    elif preset_tokens == ["starter"]:
        preset_files = PRESET_COMPOSE_FILES["starter"]
        missing_preset_files = [rel for rel in preset_files if not (root / rel).exists()]
        status = "fail" if missing_preset_files else "ok"
        rows.append(
            StatusRow(
                title="Operator preset",
                status=status,
                details="`starter`: минимальный запуск одного приложения без обязательных DB/TLS секретов.",
            )
        )
    else:
        preset_files: list[str] = []
        for token in preset_tokens:
            preset_files.extend(PRESET_COMPOSE_FILES[token])
        missing_preset_files = [rel for rel in preset_files if not (root / rel).exists()]
        status = "fail" if missing_preset_files else "ok"
        detail = (
            f"`{preset}` активен; overlays: {', '.join(preset_tokens)}; файлы: {', '.join(preset_files)}."
            if not missing_preset_files
            else f"`{preset}` активен, но не хватает overlays: {', '.join(missing_preset_files)}."
        )
        rows.append(StatusRow(title="Operator preset", status=status, details=detail))

    env_validation = validate_operator_env(root, env_path, env_mode, preset)
    if env_validation.get("status") == "pass":
        warnings = env_validation.get("warnings", "0")
        status = "warn" if warnings not in {"", "0"} else "ok"
        rows.append(
            StatusRow(
                title="Operator env validation",
                status=status,
                details=f"Проверка preset env прошла; warnings={warnings}.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Operator env validation",
                status="fail",
                details=f"Проверка env не прошла; ошибок={env_validation.get('failures', 'unknown')}, предупреждений={env_validation.get('warnings', 'unknown')}.",
            )
        )

    compose_state, compose_details = _compose_status()
    rows.append(StatusRow(title="Docker Compose", status=compose_state, details=compose_details))

    dry_data = parse_report(dry_run_report)
    dry_status = dry_data.get("status")
    if dry_status == "pass":
        when = dry_data.get("timestamp", "unknown time")
        services = dry_data.get("services", "unknown")
        dry_preset = dry_data.get("preset", "unknown")
        row_status = "ok" if dry_preset == preset else "warn"
        rows.append(
            StatusRow(
                title="Последний dry-run",
                status=row_status,
                details=f"PASS ({when}), preset: {dry_preset}, services: {services}.",
            )
        )
    elif dry_data:
        rows.append(
            StatusRow(
                title="Последний dry-run",
                status="warn",
                details=f"Последний dry-run завершился со статусом `{dry_status or 'unknown'}`.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Последний dry-run",
                status="warn",
                details="Dry-run ещё не запускался в этом окружении.",
            )
        )

    deploy_data = parse_report(deploy_report)
    deploy_status = deploy_data.get("status")
    if deploy_status == "deployed":
        when = deploy_data.get("timestamp", "unknown time")
        services = deploy_data.get("services", "unknown")
        deploy_preset = deploy_data.get("preset", "unknown")
        row_status = "ok" if deploy_preset == preset else "warn"
        rows.append(
            StatusRow(
                title="Последний deploy",
                status=row_status,
                details=f"Завершён ({when}), preset: {deploy_preset}, services: {services}.",
            )
        )
    elif deploy_data:
        rows.append(
            StatusRow(
                title="Последний deploy",
                status="warn",
                details=f"Последний deploy со статусом `{deploy_status or 'unknown'}`.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Последний deploy",
                status="warn",
                details="Deploy ещё не запускался в этом окружении.",
            )
        )

    if verify_summary.exists():
        text = verify_summary.read_text(encoding="utf-8", errors="ignore")
        pass_count = text.count("PASS")
        fail_count = text.count("FAIL")
        status = "ok" if fail_count == 0 and pass_count > 0 else "warn"
        rows.append(
            StatusRow(
                title="Verify summary",
                status=status,
                details=f"Маркеры в VERIFY_SUMMARY.md: PASS={pass_count}, FAIL={fail_count}.",
            )
        )
    else:
        rows.append(
            StatusRow(
                title="Verify summary",
                status="warn",
                details="Файл VERIFY_SUMMARY.md не найден.",
            )
        )
    return rows


def recommend_next_step(root: Path, rows: list[StatusRow], preset: str) -> str:
    by_title = {row.title: row for row in rows}
    preset_tokens, _unknown = parse_preset_expression(preset)
    preset_arg = "" if preset == "starter" else f" --preset {preset}"
    dry_run_cmd = f"bash {script_hint(root, 'deploy-dry-run.sh')}{preset_arg}"
    deploy_cmd = f"bash {script_hint(root, 'deploy-local-vps.sh')} --yes{preset_arg}"
    verify_cmd = f"bash {script_hint(root, 'verify-all.sh')} quick"
    env_cmd = "cp deploy/.env.example deploy/.env"

    if by_title["Deploy baseline"].status == "fail":
        return "Сначала восстановите deploy-файлы (`deploy/compose*.yaml`)."
    if by_title["Environment файл"].status == "fail":
        return f"Создайте env-файл: `{env_cmd}`."
    if by_title["Operator preset"].status == "fail":
        return "Исправьте `OPERATOR_PRESET` или восстановите дополнительные deploy-файлы выбранного preset."
    if by_title["Operator env validation"].status == "fail":
        return f"Исправьте deploy env (файл с настройками окружения): `python3 {script_hint(root, 'validate-operator-env.py')} --preset {preset}`."
    if by_title["Последний dry-run"].status != "ok":
        return f"Запустите безопасную проверку перед деплоем: `{dry_run_cmd}`."
    if by_title["Последний deploy"].status != "ok":
        return f"Запустите one-button-ish deploy (с автоматическим dry-run): `{deploy_cmd}`."
    if by_title["Verify summary"].status != "ok":
        return f"Обновите верификацию: `{verify_cmd}`."
    if preset_tokens == ["starter"]:
        return "Starter baseline в рабочем состоянии. Когда понадобится stateful сервис, следующий безопасный шаг: dry-run `--preset app-db`."
    if preset_tokens == ["app-db"]:
        return "`app-db` в рабочем состоянии. Перед production cutover добавьте backup через `--preset app-db,backup` и проверьте restore drill."
    if "reverse-proxy-tls" in preset_tokens and "app-db" not in preset_tokens:
        return "`reverse-proxy-tls` в рабочем состоянии. Проверьте DNS, firewall 80/443 и держите app bind на `127.0.0.1`."
    if "backup" in preset_tokens:
        return f"`{preset}` в рабочем состоянии. Проверьте свежий backup-файл, restore drill и rollback перед production cutover."
    if "healthcheck" in preset_tokens:
        return f"`{preset}` в рабочем состоянии. Проверьте endpoint healthcheck после deploy и перед rollback."
    return f"`{preset}` в рабочем состоянии. Повторите dry-run перед расширением production preset."


def print_verify_summary(root: Path, max_lines: int = 12) -> None:
    path = root / "VERIFY_SUMMARY.md"
    print("\nVERIFY SUMMARY (коротко)")
    print("-" * 72)
    if not path.exists():
        print("VERIFY_SUMMARY.md не найден.")
        return

    interesting: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and ("PASS" in stripped or "FAIL" in stripped):
            interesting.append(stripped)
    if not interesting:
        print("Не найдено PASS/FAIL строк в bullet-формате.")
        return

    for line in interesting[:max_lines]:
        print(line)
    if len(interesting) > max_lines:
        print(f"... и ещё {len(interesting) - max_lines} строк(и).")


def run_shell(root: Path, command: list[str]) -> int:
    proc = subprocess.run(command, cwd=root, check=False)
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Минимальная операторская панель: статус, следующий шаг, dry-run и verify summary.",
    )
    parser.add_argument(
        "--run-dry-run",
        action="store_true",
        help="Сразу запустить deploy dry-run и затем показать обновлённый статус.",
    )
    parser.add_argument(
        "--verify-summary",
        action="store_true",
        help="Показать короткую выжимку из VERIFY_SUMMARY.md.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Запустить dry-run и показать verify summary.",
    )
    parser.add_argument(
        "--preset",
        help="Override OPERATOR_PRESET from env for dashboard and optional dry-run.",
    )
    args = parser.parse_args()

    root = detect_repo_root()
    preset = selected_preset(root, args.preset)

    if args.run_dry_run or args.full:
        dry_script = script_path(root, "deploy-dry-run.sh")
        if dry_script.exists():
            preset_args = ["--preset", preset] if args.preset else []
            print(f"Запуск dry-run: bash {script_hint(root, 'deploy-dry-run.sh')} {' '.join(preset_args)}".rstrip())
            code = run_shell(root, ["bash", str(dry_script), *preset_args])
            if code != 0:
                print(f"\nDry-run завершился с кодом {code}.")
        else:
            print("Dry-run скрипт не найден.")

    rows = build_status_rows(root, args.preset)
    print("Панель оператора")
    print("-" * 72)
    print(f"Папка проекта: {root}")
    print(f"Deploy preset (набор настроек деплоя): {preset}")
    print(f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    for row in rows:
        label = STATUS_LABEL.get(row.status, row.status.upper())
        print(f"[{label}] {row.title}")
        print(f"  {row.details}")
    print()
    print("Следующий шаг:")
    print(f"- {recommend_next_step(root, rows, preset)}")
    print(f"- Вернуться в launcher: python3 {script_hint(root, 'factory-launcher.py')} --continue")

    if args.verify_summary or args.full:
        print_verify_summary(root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
