#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATHS = [ROOT / ".env", ROOT / ".env.local"]
DEFAULT_REPORTS_DIR = ROOT / "_sources-export" / "factory-template" / "_sync-reports"
DEFAULT_CONFIG_PATHS = [ROOT / ".chatgpt" / "google-drive-sources.yaml"]


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def load_env_files(paths: list[Path]) -> dict[str, str]:
    values: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in values:
                values[key] = value
    return values


def env_get(name: str, env_file_values: dict[str, str], default: str | None = None) -> str | None:
    return os.environ.get(name, env_file_values.get(name, default))


def load_yaml_config(paths: list[Path]) -> dict:
    merged: dict = {}
    for path in paths:
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict):
            merged.update(data)
    return merged


def config_get(config: dict, key: str, default=None):
    sources = config.get("google_drive_sources", config)
    if not isinstance(sources, dict):
        return default
    return sources.get(key, default)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def resolve_export_dir(export_dir: Path) -> tuple[Path, str]:
    manifest_path = export_dir / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        upload_subdir = str(manifest.get("upload_subdir", "upload-to-sources")).strip()
        if manifest.get("kind") == "direct_sources":
            candidate = export_dir / upload_subdir
            if candidate.exists():
                return candidate.resolve(), str(manifest.get("export_name", export_dir.name))
    if export_dir.name == "upload-to-sources":
        return export_dir.resolve(), export_dir.parent.name
    return export_dir.resolve(), export_dir.name


def collect_local_files(export_dir: Path) -> dict[str, dict[str, object]]:
    files: dict[str, dict[str, object]] = {}
    nested_dirs = [path for path in export_dir.iterdir() if path.is_dir()]
    if nested_dirs:
        names = ", ".join(sorted(path.name for path in nested_dirs))
        raise RuntimeError(
            f"Flat-folder semantics violated in {export_dir}: nested directories found: {names}"
        )
    for path in sorted(export_dir.iterdir()):
        if not path.is_file():
            continue
        files[path.name] = {
            "name": path.name,
            "size": path.stat().st_size,
            "sha256": file_sha256(path),
            "md5": file_md5(path),
            "path": str(path),
        }
    return files


def load_remote_snapshot(path: Path | None) -> dict[str, dict[str, object]]:
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("files", payload)
    if not isinstance(items, list):
        raise RuntimeError("Remote snapshot must contain a top-level `files` list or be a list itself.")
    result: dict[str, dict[str, object]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        result[name] = item
    return result


def compare(local_files: dict[str, dict[str, object]], remote_files: dict[str, dict[str, object]], delete_stale: bool) -> list[dict[str, object]]:
    actions: list[dict[str, object]] = []
    for name, local in local_files.items():
        remote = remote_files.get(name)
        if remote is None:
            actions.append({"action": "create", "name": name, "reason": "missing_remote_file"})
            continue
        remote_sha = str(remote.get("sha256", "")).strip()
        remote_md5 = str(remote.get("md5", "") or remote.get("md5Checksum", "")).strip()
        remote_size = int(remote.get("size", 0) or 0)
        if remote_sha:
            same = remote_sha == local["sha256"]
            strategy = "sha256"
        elif remote_md5:
            same = remote_md5 == local["md5"]
            strategy = "md5"
        else:
            same = remote_size == local["size"]
            strategy = "size"
        if same:
            actions.append({"action": "skip", "name": name, "reason": "unchanged", "compare_strategy": strategy})
        else:
            actions.append({"action": "update", "name": name, "reason": "content_differs", "compare_strategy": strategy})
    for name, remote in remote_files.items():
        if name in local_files:
            continue
        if delete_stale:
            actions.append({"action": "delete", "name": name, "reason": "missing_local_file"})
        else:
            actions.append({"action": "skip", "name": name, "reason": "stale_cleanup_disabled"})
    return actions


def render_markdown(report: dict[str, object]) -> str:
    actions = report["detailed_actions"]
    assert isinstance(actions, list)
    lines = [
        "# Google Drive Connector Sync Request",
        "",
        f"- timestamp: `{report['timestamp']}`",
        f"- source export path: `{report['source_export_path']}`",
        f"- source export pack: `{report['source_export_pack']}`",
        f"- target folder url: `{report['target_folder_url']}`",
        f"- sync mode: `{report['sync_mode']}`",
        f"- dry run: `{str(report['dry_run']).lower()}`",
        f"- delete stale: `{str(report['delete_stale']).lower()}`",
        f"- files scanned local: `{report['files_scanned_local']}`",
        f"- files scanned remote: `{report['files_scanned_remote']}`",
        f"- compare status: `{report['compare_status']}`",
        f"- create count: `{report['create_count']}`",
        f"- update count: `{report['update_count']}`",
        f"- delete count: `{report['delete_count']}`",
        f"- skip count: `{report['skip_count']}`",
        "",
        "## Summary",
        "",
        f"- created: {[item['name'] for item in actions if item.get('action') == 'create']}",
        f"- updated: {[item['name'] for item in actions if item.get('action') == 'update']}",
        f"- deleted: {[item['name'] for item in actions if item.get('action') == 'delete']}",
        f"- skipped: {[item['name'] for item in actions if item.get('action') == 'skip']}",
        f"- warnings: {report['warnings']}",
        f"- errors: {report['errors']}",
        "",
        "## Connector Boundary",
        "",
        "- This repo script does not invoke Google Drive mutations itself.",
        "- The active Codex Google Drive connector in this environment is the external execution boundary.",
        "- Raw-file create/update/delete must be treated as a Codex-managed connector step, not a shell-driven repo automation promise.",
        "",
        "## Detailed Actions",
        "",
    ]
    for item in actions:
        lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a Codex Google Drive connector sync request for a flat factory-template Sources export."
    )
    parser.add_argument("export_dir", nargs="?", help="Path to the already-built local flat export folder.")
    parser.add_argument("--reports-dir", help="Where to store sync request reports.")
    parser.add_argument("--report-dir", help="Alias for --reports-dir.")
    parser.add_argument("--env-file", action="append", default=[], help="Additional env file to read before process env.")
    parser.add_argument("--config", action="append", default=[], help="Additional YAML config file to read before env fallback.")
    parser.add_argument("--folder-url", help="Override GOOGLE_DRIVE_FOLDER_URL for this run.")
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run mode.")
    parser.add_argument("--delete-stale", action="store_true", help="Mark stale remote files for deletion in the request plan.")
    parser.add_argument("--remote-snapshot", help="Optional JSON snapshot of the remote Drive folder inventory produced outside this script.")
    args = parser.parse_args(argv)

    env_paths = DEFAULT_ENV_PATHS + [Path(path).resolve() for path in args.env_file]
    config_paths = DEFAULT_CONFIG_PATHS + [Path(path).resolve() for path in args.config]
    env_file_values = load_env_files(env_paths)
    yaml_config = load_yaml_config(config_paths)
    export_dir_raw = args.export_dir or env_get("FACTORY_TEMPLATE_GDRIVE_EXPORT_PATH", env_file_values)
    if not export_dir_raw:
        raise RuntimeError("Export folder is required as CLI argument or FACTORY_TEMPLATE_GDRIVE_EXPORT_PATH")
    reports_dir_raw = (
        args.reports_dir
        or args.report_dir
        or env_get("FACTORY_TEMPLATE_SYNC_REPORT_DIR", env_file_values, None)
        or config_get(yaml_config, "report_dir", str(DEFAULT_REPORTS_DIR))
        or str(DEFAULT_REPORTS_DIR)
    )
    target_folder_url = (
        args.folder_url
        or env_get("GOOGLE_DRIVE_FOLDER_URL", env_file_values, None)
        or config_get(yaml_config, "folder_url", "")
        or ""
    )
    if not target_folder_url.strip():
        raise RuntimeError("GOOGLE_DRIVE_FOLDER_URL or .chatgpt/google-drive-sources.yaml:folder_url is required for Codex-managed Google Drive connector sync.")

    export_dir, export_pack_name = resolve_export_dir(Path(export_dir_raw))
    local_files = collect_local_files(export_dir)
    remote_snapshot_path = Path(args.remote_snapshot).resolve() if args.remote_snapshot else None
    remote_files = load_remote_snapshot(remote_snapshot_path)
    delete_stale = args.delete_stale or parse_bool(
        env_get("GOOGLE_DRIVE_DELETE_STALE", env_file_values, None),
        default=parse_bool(str(config_get(yaml_config, "delete_stale", "0")), default=False),
    )
    dry_run = args.dry_run or parse_bool(
        env_get("GOOGLE_DRIVE_DRY_RUN", env_file_values, None),
        default=parse_bool(str(config_get(yaml_config, "dry_run", "1")), default=True),
    )
    actions = compare(local_files, remote_files, delete_stale) if remote_files else []
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_export_path": str(export_dir),
        "source_export_pack": export_pack_name,
        "target_folder_url": target_folder_url,
        "sync_mode": "codex_google_drive_connector_boundary",
        "repo_can_execute_sync": False,
        "connector_execution_required": True,
        "dry_run": dry_run,
        "delete_stale": delete_stale,
        "supports_all_drives": parse_bool(
            env_get("GOOGLE_DRIVE_SUPPORTS_ALL_DRIVES", env_file_values, None),
            default=parse_bool(str(config_get(yaml_config, "supports_all_drives", "0")), default=False),
        ),
        "files_scanned_local": len(local_files),
        "files_scanned_remote": len(remote_files),
        "compare_status": "planned_from_remote_snapshot" if remote_files else "awaiting_codex_connector_remote_snapshot",
        "create_count": sum(1 for item in actions if item["action"] == "create"),
        "update_count": sum(1 for item in actions if item["action"] == "update"),
        "delete_count": sum(1 for item in actions if item["action"] == "delete"),
        "skip_count": sum(1 for item in actions if item["action"] == "skip"),
        "warnings": [] if remote_files else ["Remote folder snapshot not provided; create/update/delete plan is pending Codex connector scan."],
        "errors": [],
        "detailed_actions": actions if remote_files else [{"action": "pending", "reason": "remote_snapshot_required_for_compare"}],
    }

    reports_dir = Path(reports_dir_raw).resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    base = reports_dir / f"gdrive-sync-report-{export_pack_name}-{stamp}"
    json_path = base.with_suffix(".json")
    md_path = base.with_suffix(".md")
    latest_json_path = reports_dir / f"gdrive-sync-report-{export_pack_name}-latest.json"
    latest_md_path = reports_dir / f"gdrive-sync-report-{export_pack_name}-latest.md"
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    markdown = render_markdown(report)
    json_path.write_text(payload, encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    latest_json_path.write_text(payload, encoding="utf-8")
    latest_md_path.write_text(markdown, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
