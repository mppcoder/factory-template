#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SAFE_COMMANDS = {"status", "ack", "defer", "bug", "handoff_draft", "feedback"}
FORBIDDEN_COMMANDS = {"shell", "codex_run", "deploy", "delete", "merge", "push"}
SECRET_RE = re.compile(
    r"(?i)(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"
)
SUSPICIOUS_RE = re.compile(r"(?i)(-----BEGIN|\.env(?:\s|$)|private transcript)")


class NotifyError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text) or {}


def load_config(root: Path, path: Path) -> dict[str, Any]:
    config_path = path if path.is_absolute() else root / path
    data = load_data(config_path)
    if not isinstance(data, dict):
        raise NotifyError(f"config must be mapping: {config_path}")
    return data


def normalize_events(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("events"), list):
        return [item for item in data["events"] if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    raise NotifyError("event input must be mapping, list, or mapping with events")


def secret_like(value: Any) -> bool:
    dumped = yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    return bool(SECRET_RE.search(dumped) or SUSPICIOUS_RE.search(dumped))


def redact_text(text: str) -> str:
    text = SECRET_RE.sub("[REDACTED_SECRET]", text)
    text = re.sub(r"(?i)-----BEGIN[^\\n]+", "[REDACTED_PRIVATE_BLOCK]", text)
    return text


def truncate(text: str, limit: int = 700) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def format_list(items: Any, limit: int = 5) -> str:
    if not isinstance(items, list) or not items:
        return ""
    rendered: list[str] = []
    for item in items[:limit]:
        if isinstance(item, dict):
            label = str(item.get("title") or item.get("path") or item.get("url") or item)
        else:
            label = str(item)
        rendered.append(f"- {html.escape(truncate(redact_text(label), 180))}")
    return "\n".join(rendered)


def format_message(event: dict[str, Any]) -> str:
    if secret_like(event):
        raise NotifyError("event contains secret-like content")
    title = html.escape(truncate(redact_text(str(event.get("title") or "Notification")), 120))
    kind = html.escape(str(event.get("kind") or "unknown"))
    severity = html.escape(str(event.get("severity") or "info"))
    status = html.escape(str(event.get("status") or ""))
    project = html.escape(str(event.get("project_id") or ""))
    contour = html.escape(str(event.get("project_contour") or ""))
    repo = html.escape(str(event.get("repo") or ""))
    summary = html.escape(truncate(redact_text(str(event.get("summary") or "")), 900))
    required_action = html.escape(truncate(redact_text(str(event.get("required_user_action") or "")), 500))
    recommendation = html.escape(truncate(redact_text(str(event.get("recommendation") or "")), 500))
    identifiers = []
    for key in ["task_id", "chat_id", "codex_work_id"]:
        value = str(event.get(key) or "").strip()
        if value:
            identifiers.append(f"{key}: {html.escape(value)}")
    message_parts = [
        f"<b>{title}</b>",
        f"<code>{kind}</code> | <code>{severity}</code> | <code>{status}</code>",
        f"<b>Project:</b> {project}",
        f"<b>Contour:</b> {contour}",
        f"<b>Repo:</b> {repo}",
    ]
    if identifiers:
        message_parts.append("<b>Refs:</b> " + html.escape(", ".join(identifiers)))
    if summary:
        message_parts.append(f"<b>Summary:</b>\n{summary}")
    if required_action:
        message_parts.append(f"<b>Required user action:</b>\n{required_action}")
    if recommendation:
        message_parts.append(f"<b>Recommendation:</b>\n{recommendation}")
    evidence = format_list(event.get("evidence"))
    if evidence:
        message_parts.append(f"<b>Evidence:</b>\n{evidence}")
    links = format_list(event.get("links"))
    if links:
        message_parts.append(f"<b>Links:</b>\n{links}")
    message_parts.append(f"<b>Dedupe:</b> <code>{html.escape(str(event.get('dedupe_key') or ''))}</code>")
    return "\n\n".join(message_parts)[:3900]


def topic_for_event(config: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    routing = config.get("routing") or {}
    contour_to_topic = routing.get("contour_to_topic") or {}
    kind_to_topic = routing.get("kind_to_topic") or {}
    topic_name = (
        contour_to_topic.get(event.get("project_contour"))
        or kind_to_topic.get(event.get("kind"))
        or routing.get("default_topic")
    )
    topics = config.get("topics") or {}
    topic = topics.get(topic_name)
    if not isinstance(topic, dict):
        raise NotifyError(f"topic not found for kind {event.get('kind')}: {topic_name}")
    return {"name": topic_name, **topic}


def is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("REPLACE_WITH_")


def outbox_path(root: Path, config: dict[str, Any], override: str | None) -> Path:
    value = override or ((config.get("paths") or {}).get("outbox_jsonl"))
    if not value:
        raise NotifyError("outbox path is not configured")
    path = Path(str(value))
    return path if path.is_absolute() else root / path


def audit_path(root: Path, config: dict[str, Any], override: str | None) -> Path:
    value = override or ((config.get("paths") or {}).get("inbound_audit_jsonl"))
    if not value:
        raise NotifyError("inbound audit path is not configured")
    path = Path(str(value))
    return path if path.is_absolute() else root / path


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            entries.append(item)
    return entries


def append_jsonl(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def is_duplicate(path: Path, dedupe_key: str, *, dry_run: bool) -> bool:
    blocking_statuses = {"sent"}
    if dry_run:
        blocking_statuses.add("dry_run")
    for entry in iter_jsonl(path):
        if entry.get("dedupe_key") == dedupe_key and entry.get("delivery_status") in blocking_statuses:
            return True
    return False


def send_to_telegram(token: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{urllib.parse.quote(token)}/sendMessage"
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise NotifyError(f"telegram send failed: {exc}") from exc
    result = json.loads(body)
    if not result.get("ok"):
        raise NotifyError(f"telegram send rejected: {result}")
    return result


def send_events(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(root, Path(args.config))
    outbox = outbox_path(root, config, args.outbox)
    events = normalize_events(load_data(Path(args.event)))
    telegram = config.get("telegram") or {}
    parse_mode = str(telegram.get("parse_mode") or "HTML")
    timeout = int(telegram.get("request_timeout_seconds") or 15)
    token_env = str(telegram.get("bot_token_env") or "TELEGRAM_BOT_TOKEN")
    token = os.environ.get(token_env, "")
    if not args.dry_run and not token:
        raise NotifyError(f"{token_env} is required for real Telegram delivery")

    sent = 0
    for event in events:
        dedupe_key = str(event.get("dedupe_key") or "")
        if not dedupe_key:
            raise NotifyError("event.dedupe_key is required")
        topic = topic_for_event(config, event)
        if is_duplicate(outbox, dedupe_key, dry_run=args.dry_run):
            append_jsonl(
                outbox,
                {
                    "created_utc": utc_now(),
                    "event_id": event.get("event_id"),
                    "dedupe_key": dedupe_key,
                    "kind": event.get("kind"),
                    "project_contour": event.get("project_contour"),
                    "topic": topic.get("name"),
                    "delivery_status": "duplicate_skipped",
                    "dry_run": args.dry_run,
                },
            )
            continue
        chat_id = topic.get("chat_id")
        if is_placeholder(chat_id):
            if not args.dry_run:
                raise NotifyError("real Telegram delivery cannot use placeholder chat_id")
        payload: dict[str, Any] = {
            "chat_id": str(chat_id),
            "text": format_message(event),
            "parse_mode": parse_mode,
            "disable_web_page_preview": "true",
        }
        thread_id = topic.get("message_thread_id")
        if thread_id not in (None, "", "null") and not is_placeholder(thread_id):
            payload["message_thread_id"] = str(thread_id)

        status = "dry_run"
        response_summary: dict[str, Any] = {}
        if not args.dry_run:
            response = send_to_telegram(token, payload, timeout)
            status = "sent"
            response_summary = {
                "message_id": (((response.get("result") or {}).get("message_id"))),
                "chat_id": ((((response.get("result") or {}).get("chat") or {}).get("id"))),
            }
        append_jsonl(
            outbox,
            {
                "created_utc": utc_now(),
                "event_id": event.get("event_id"),
                "dedupe_key": dedupe_key,
                "kind": event.get("kind"),
                "project_contour": event.get("project_contour"),
                "topic": topic.get("name"),
                "delivery_status": status,
                "dry_run": args.dry_run,
                "message_sha256": hashlib.sha256(payload["text"].encode("utf-8")).hexdigest(),
                "telegram_response": response_summary,
            },
        )
        sent += 1
        if args.print_messages:
            print(payload["text"])
            print("")
    print(f"telegram_notifications_processed={sent}")
    print(f"outbox={outbox}")
    return 0


def env_id_set(name: str) -> set[str]:
    return {item.strip() for item in os.environ.get(name, "").split(",") if item.strip()}


def command_name(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    first = text.split()[0]
    if first.startswith("/"):
        first = first[1:]
    return first.split("@", 1)[0]


def audit_inbound(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(root, Path(args.config))
    audit = audit_path(root, config, args.audit)
    payload = load_data(Path(args.payload))
    message = payload.get("message") or payload.get("edited_message") or {}
    chat = message.get("chat") or {}
    actor = message.get("from") or {}
    text = str(message.get("text") or "")
    command = command_name(text)
    telegram = config.get("telegram") or {}
    allowed_chat_ids = env_id_set(str(telegram.get("allowed_chat_ids_env") or "TELEGRAM_ALLOWED_CHAT_IDS"))
    allowed_user_ids = env_id_set(str(telegram.get("allowed_user_ids_env") or "TELEGRAM_ALLOWED_USER_IDS"))
    chat_id = str(chat.get("id") or "")
    user_id = str(actor.get("id") or "")
    allowed = command in SAFE_COMMANDS and command not in FORBIDDEN_COMMANDS
    if allowed_chat_ids and chat_id not in allowed_chat_ids:
        allowed = False
    if allowed_user_ids and user_id not in allowed_user_ids:
        allowed = False
    entry = {
        "created_utc": utc_now(),
        "update_id": payload.get("update_id"),
        "chat_id": chat_id,
        "user_id": user_id,
        "command": command,
        "allowed": allowed,
        "reason": "safe_command" if allowed else "blocked_by_command_or_allowlist",
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    append_jsonl(audit, entry)
    print(f"inbound_command_allowed={str(allowed).lower()}")
    print(f"audit={audit}")
    return 0 if allowed or args.allow_blocked_exit_zero else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send repo-native Telegram feedback notifications.")
    sub = parser.add_subparsers(dest="command")
    send = sub.add_parser("send", help="Send or dry-run outbound notification events.")
    send.add_argument("--root", default=".")
    send.add_argument("--config", default="template-repo/template/.chatgpt/telegram-feedback-channel.example.yaml")
    send.add_argument("--event", required=True)
    send.add_argument("--outbox")
    send.add_argument("--dry-run", action="store_true")
    send.add_argument("--print-messages", action="store_true")
    audit = sub.add_parser("audit-inbound", help="Audit a safe inbound Telegram command payload.")
    audit.add_argument("--root", default=".")
    audit.add_argument("--config", default="template-repo/template/.chatgpt/telegram-feedback-channel.example.yaml")
    audit.add_argument("--payload", required=True)
    audit.add_argument("--audit")
    audit.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "send":
            return send_events(args)
        if args.command == "audit-inbound":
            return audit_inbound(args)
        parser.print_help()
        return 2
    except NotifyError as exc:
        print(f"factory_notify_telegram: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
