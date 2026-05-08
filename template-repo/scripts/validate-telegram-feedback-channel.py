#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


CONFIG_SCHEMA = "telegram-feedback-channel-config/v1"
EVENT_SCHEMA = "telegram-feedback-event-schema/v1"
PLACEHOLDER_RE = re.compile(r"^REPLACE_WITH_[A-Z0-9_]+$")
SECRET_RE = re.compile(
    r"(?i)(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"
)
SUSPICIOUS_RE = re.compile(r"(?i)(-----BEGIN|\.env(?:\s|$)|private transcript)")

DEFAULT_KINDS = {
    "task.completed",
    "codex.completed",
    "user_action.required",
    "bug.detected",
    "bug.fixed",
    "verification.failed",
    "update.available",
    "update.recommended",
    "release.published",
    "deploy.done",
}
DEFAULT_ALLOWED_COMMANDS = {"status", "ack", "defer", "bug", "handoff_draft", "feedback"}
DEFAULT_FORBIDDEN_COMMANDS = {"shell", "codex_run", "deploy", "delete", "merge", "push"}


def load_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text) or {}


def as_mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(f"{path} должен быть mapping")
    return {}


def as_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{path} должен быть list")
    return []


def contains_secret(value: Any) -> bool:
    dumped = yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    for line in dumped.splitlines():
        stripped = line.strip()
        if stripped.startswith(("bot_token_env:", "allowed_chat_ids_env:", "allowed_user_ids_env:")):
            continue
        if stripped.startswith(("TELEGRAM_BOT_TOKEN:", "TELEGRAM_ALLOWED_CHAT_IDS:", "TELEGRAM_ALLOWED_USER_IDS:")):
            continue
        if SECRET_RE.search(line) or SUSPICIOUS_RE.search(line):
            return True
    return False


def parse_utc(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.astimezone(timezone.utc).utcoffset().total_seconds() == 0


def validate_schema(schema: dict[str, Any], errors: list[str]) -> dict[str, set[str]]:
    if schema.get("schema") != EVENT_SCHEMA:
        errors.append(f"event schema должен иметь schema: {EVENT_SCHEMA}")
    required = set(as_list(schema.get("required_fields", []), "required_fields", errors))
    for field in [
        "event_id",
        "project_id",
        "project_type",
        "repo",
        "source",
        "kind",
        "severity",
        "title",
        "summary",
        "task_id",
        "chat_id",
        "codex_work_id",
        "status",
        "required_user_action",
        "recommendation",
        "evidence",
        "links",
        "created_utc",
        "dedupe_key",
    ]:
        if field not in required:
            errors.append(f"event schema required_fields не содержит `{field}`")
    return {
        "project_types": {str(item) for item in schema.get("allowed_project_types", []) or []},
        "kinds": {str(item) for item in schema.get("allowed_kinds", []) or []},
        "severities": {str(item) for item in schema.get("allowed_severities", []) or []},
        "statuses": {str(item) for item in schema.get("allowed_statuses", []) or []},
        "required": required,
    }


def validate_config(config: dict[str, Any], *, allow_placeholders: bool, errors: list[str]) -> None:
    if config.get("schema") != CONFIG_SCHEMA:
        errors.append(f"config должен иметь schema: {CONFIG_SCHEMA}")
    if contains_secret(config):
        errors.append("config содержит secret-like content; token допускается только через env key name")

    telegram = as_mapping(config.get("telegram"), "telegram", errors)
    if telegram.get("bot_token_env") != "TELEGRAM_BOT_TOKEN":
        errors.append("telegram.bot_token_env должен ссылаться на TELEGRAM_BOT_TOKEN")
    if telegram.get("allowed_chat_ids_env") != "TELEGRAM_ALLOWED_CHAT_IDS":
        errors.append("telegram.allowed_chat_ids_env должен ссылаться на TELEGRAM_ALLOWED_CHAT_IDS")
    if telegram.get("allowed_user_ids_env") != "TELEGRAM_ALLOWED_USER_IDS":
        errors.append("telegram.allowed_user_ids_env должен ссылаться на TELEGRAM_ALLOWED_USER_IDS")

    paths = as_mapping(config.get("paths"), "paths", errors)
    for key in ["event_schema", "outbox_jsonl", "inbound_audit_jsonl"]:
        if not str(paths.get(key) or "").strip():
            errors.append(f"paths.{key} обязателен")
    for key in ["outbox_jsonl", "inbound_audit_jsonl"]:
        value = str(paths.get(key) or "")
        if not value.endswith(".jsonl"):
            errors.append(f"paths.{key} должен указывать на .jsonl")

    routing = as_mapping(config.get("routing"), "routing", errors)
    topics = as_mapping(config.get("topics"), "topics", errors)
    default_topic = str(routing.get("default_topic") or "")
    if default_topic not in topics:
        errors.append("routing.default_topic должен ссылаться на topics")
    kind_to_topic = as_mapping(routing.get("kind_to_topic"), "routing.kind_to_topic", errors)
    missing_kinds = sorted(DEFAULT_KINDS - set(kind_to_topic))
    if missing_kinds:
        errors.append("routing.kind_to_topic не содержит P0 kinds: " + ", ".join(missing_kinds))
    for kind, topic_name in kind_to_topic.items():
        if str(topic_name) not in topics:
            errors.append(f"routing.kind_to_topic.{kind} ссылается на неизвестный topic `{topic_name}`")

    for topic_name, topic in topics.items():
        topic_map = as_mapping(topic, f"topics.{topic_name}", errors)
        chat_id = topic_map.get("chat_id")
        if chat_id in (None, ""):
            errors.append(f"topics.{topic_name}.chat_id обязателен")
        elif isinstance(chat_id, int):
            pass
        else:
            chat_text = str(chat_id)
            if PLACEHOLDER_RE.match(chat_text):
                if not allow_placeholders:
                    errors.append(f"topics.{topic_name}.chat_id содержит placeholder")
            elif not re.match(r"^-?\d+$", chat_text):
                errors.append(f"topics.{topic_name}.chat_id должен быть numeric id или placeholder в example config")
        thread_id = topic_map.get("message_thread_id")
        if thread_id in (None, ""):
            continue
        if isinstance(thread_id, int):
            continue
        thread_text = str(thread_id)
        if PLACEHOLDER_RE.match(thread_text):
            if not allow_placeholders:
                errors.append(f"topics.{topic_name}.message_thread_id содержит placeholder")
        elif not re.match(r"^\d+$", thread_text):
            errors.append(f"topics.{topic_name}.message_thread_id должен быть numeric id или null")

    inbound = as_mapping(config.get("inbound_commands"), "inbound_commands", errors)
    allowed = {str(item) for item in inbound.get("allowed", []) or []}
    forbidden = {str(item) for item in inbound.get("forbidden", []) or []}
    if allowed != DEFAULT_ALLOWED_COMMANDS:
        errors.append("inbound_commands.allowed должен быть ровно safe P0 command set")
    if not DEFAULT_FORBIDDEN_COMMANDS.issubset(forbidden):
        errors.append("inbound_commands.forbidden должен запрещать shell/codex_run/deploy/delete/merge/push")
    if allowed & forbidden:
        errors.append("inbound_commands содержит command одновременно в allowed и forbidden")


def normalize_events(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("events"), list):
        return [item for item in data["events"] if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def validate_event(event: dict[str, Any], contract: dict[str, set[str]], path: str, errors: list[str]) -> None:
    if contains_secret(event):
        errors.append(f"{path}: event содержит secret-like content")
    for field in sorted(contract["required"]):
        if field not in event:
            errors.append(f"{path}: отсутствует обязательное поле `{field}`")
    for field in ["event_id", "project_id", "project_type", "repo", "source", "kind", "severity", "title", "summary", "status", "created_utc", "dedupe_key"]:
        if not str(event.get(field, "")).strip():
            errors.append(f"{path}: поле `{field}` не должно быть пустым")
    if event.get("project_type") not in contract["project_types"]:
        errors.append(f"{path}: неизвестный project_type `{event.get('project_type')}`")
    if event.get("kind") not in contract["kinds"]:
        errors.append(f"{path}: неизвестный kind `{event.get('kind')}`")
    if event.get("severity") not in contract["severities"]:
        errors.append(f"{path}: неизвестный severity `{event.get('severity')}`")
    if event.get("status") not in contract["statuses"]:
        errors.append(f"{path}: неизвестный status `{event.get('status')}`")
    if not isinstance(event.get("evidence"), list):
        errors.append(f"{path}: evidence должен быть list")
    if not isinstance(event.get("links"), list):
        errors.append(f"{path}: links должен быть list")
    if not parse_utc(str(event.get("created_utc") or "")):
        errors.append(f"{path}: created_utc должен быть UTC ISO-8601 timestamp")
    if len(str(event.get("dedupe_key") or "")) < 12 or " " in str(event.get("dedupe_key") or ""):
        errors.append(f"{path}: dedupe_key должен быть стабильным непустым ключом без пробелов")
    if event.get("kind") == "user_action.required" and not str(event.get("required_user_action") or "").strip():
        errors.append(f"{path}: user_action.required требует required_user_action")
    if event.get("kind") in {"update.recommended", "verification.failed"} and not str(event.get("recommendation") or "").strip():
        errors.append(f"{path}: {event.get('kind')} требует recommendation")


def collect_event_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(item for item in path.rglob("*") if item.suffix in {".yaml", ".yml", ".json"}))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repo-native Telegram feedback channel config, schema and fixtures.")
    parser.add_argument("--root", default=".", help="Repo root.")
    parser.add_argument("--config", default="template-repo/template/.chatgpt/telegram-feedback-channel.example.yaml")
    parser.add_argument("--schema", default="template-repo/template/.chatgpt/telegram-feedback-event.schema.yaml")
    parser.add_argument("--events", nargs="*", default=["tests/telegram-feedback-channel/events"])
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow safe placeholders in example config.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = root / args.config
    schema_path = root / args.schema
    errors: list[str] = []

    if not config_path.exists():
        errors.append(f"config not found: {config_path}")
        config = {}
    else:
        config = as_mapping(load_data(config_path), str(config_path), errors)
        validate_config(config, allow_placeholders=args.allow_placeholders, errors=errors)

    if not schema_path.exists():
        errors.append(f"schema not found: {schema_path}")
        schema = {}
    else:
        schema = as_mapping(load_data(schema_path), str(schema_path), errors)
    contract = validate_schema(schema, errors)

    seen_dedupe: set[str] = set()
    for event_file in collect_event_files([root / item for item in args.events]):
        if not event_file.exists():
            errors.append(f"event fixture not found: {event_file}")
            continue
        events = normalize_events(load_data(event_file))
        if not events:
            errors.append(f"{event_file}: не содержит event или events")
        for index, event in enumerate(events, 1):
            validate_event(event, contract, f"{event_file}:{index}", errors)
            dedupe_key = str(event.get("dedupe_key") or "")
            if dedupe_key in seen_dedupe:
                errors.append(f"{event_file}:{index}: duplicate dedupe_key `{dedupe_key}`")
            seen_dedupe.add(dedupe_key)

    fixture_kinds: set[str] = set()
    for event_file in collect_event_files([root / item for item in args.events]):
        if event_file.exists():
            fixture_kinds.update(str(event.get("kind")) for event in normalize_events(load_data(event_file)))
    missing_p0 = DEFAULT_KINDS - fixture_kinds
    if missing_p0:
        errors.append("event fixtures не покрывают P0 kinds: " + ", ".join(sorted(missing_p0)))

    if errors:
        print("TELEGRAM FEEDBACK CHANNEL НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("TELEGRAM FEEDBACK CHANNEL ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
