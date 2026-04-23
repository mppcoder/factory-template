#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import json
from pathlib import Path
from typing import Iterable

import yaml

SYNC_HEADER = """<!--
SYNCED FILE - DO NOT EDIT MANUALLY
Source of truth: template-repo/AGENTS.md
This root AGENTS.md is a materialized clone for the downstream repo.
Manual edits in this clone will be overwritten by the canonical template sync flow.
-->
"""


def render_materialized_clone(text: str) -> str:
    return f"{SYNC_HEADER}\n{text.strip()}\n"


def load_manifest() -> dict:
    manifest = Path(__file__).with_name("factory-sync-manifest.yaml")
    if not manifest.exists():
        return {}
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def project_zone(project: Path, zone: str) -> Path:
    if zone.startswith("template-repo/template/"):
        return project / zone.replace("template-repo/template/", "", 1)
    return project / zone


def _normalize_zone_entry(entry: object) -> tuple[str, dict]:
    if isinstance(entry, str):
        return entry, {}
    if isinstance(entry, dict):
        path = str(entry.get("path", "")).strip()
        return path, entry
    return "", {}


def compare_materialized_files(factory: Path, project: Path) -> list[dict]:
    report = []
    manifest = load_manifest()
    for mapping in manifest.get("materialized_files", []):
        source = factory / mapping["source"]
        target = project / mapping["target"]
        if not source.exists():
            report.append({"source": mapping["source"], "target": mapping["target"], "status": "missing-source"})
            continue
        expected = source.read_text(encoding="utf-8")
        if mapping.get("mode") == "materialized-clone":
            expected = render_materialized_clone(expected)
        if not target.exists():
            report.append({"source": mapping["source"], "target": mapping["target"], "status": "missing-target"})
            continue
        actual = target.read_text(encoding="utf-8")
        if actual != expected:
            report.append({"source": mapping["source"], "target": mapping["target"], "status": "drift"})
        else:
            report.append({"source": mapping["source"], "target": mapping["target"], "status": "ok"})
    return report


def _join_rel(base: str, name: str) -> str:
    return f"{base}/{name}" if base else name


def _collect_dircmp(cmp: filecmp.dircmp, base: str, sink: dict[str, list[str]]) -> None:
    sink["left_only"].extend(_join_rel(base, item) for item in cmp.left_only)
    sink["right_only"].extend(_join_rel(base, item) for item in cmp.right_only)
    sink["diff_files"].extend(_join_rel(base, item) for item in cmp.diff_files)
    sink["funny_files"].extend(_join_rel(base, item) for item in cmp.funny_files)
    for subdir_name, subcmp in cmp.subdirs.items():
        _collect_dircmp(subcmp, _join_rel(base, subdir_name), sink)


def compare_dirs(factory: Path, project: Path) -> list[dict]:
    report = []
    manifest = load_manifest()
    for zone_entry in manifest.get("sync_zones", []):
        rel, zone_meta = _normalize_zone_entry(zone_entry)
        if not rel:
            continue
        a = factory / rel
        b = project_zone(project, rel)
        optional_in_project = bool(zone_meta.get("optional_in_project", False))
        if not a.exists() or not b.exists():
            if a.exists() and not b.exists() and optional_in_project:
                report.append(
                    {
                        "path": rel,
                        "status": "optional-missing-project",
                        "factory_exists": True,
                        "project_exists": False,
                        "left_only": [],
                        "right_only": [],
                        "diff_files": [],
                        "funny_files": [],
                        "optional_in_project": True,
                    }
                )
                continue
            report.append(
                {
                    "path": rel,
                    "status": "missing-source" if not a.exists() else "missing-project",
                    "factory_exists": a.exists(),
                    "project_exists": b.exists(),
                    "left_only": [],
                    "right_only": [],
                    "diff_files": [],
                    "funny_files": [],
                    "optional_in_project": optional_in_project,
                }
            )
            continue
        cmp = filecmp.dircmp(a, b)
        buckets: dict[str, list[str]] = {
            "left_only": [],
            "right_only": [],
            "diff_files": [],
            "funny_files": [],
        }
        _collect_dircmp(cmp, "", buckets)
        has_diff = any(buckets[key] for key in ("left_only", "right_only", "diff_files", "funny_files"))
        report.append(
            {
                "path": rel,
                "status": "drift" if has_diff else "ok",
                "factory_exists": True,
                "project_exists": True,
                "optional_in_project": optional_in_project,
                **buckets,
            }
        )
    return report


def summarize(drift: Iterable[dict], materialized_files: Iterable[dict]) -> dict:
    drift = list(drift)
    materialized_files = list(materialized_files)
    zones_optional_missing = sum(1 for item in drift if item.get("status") == "optional-missing-project")
    zones_missing = sum(1 for item in drift if item.get("status") in {"missing-source", "missing-project"})
    zones_with_drift = sum(1 for item in drift if item.get("status") == "drift")
    materialized_with_issues = sum(1 for item in materialized_files if item.get("status") != "ok")
    return {
        "zones_total": len(drift),
        "zones_ok": sum(1 for item in drift if item.get("status") in {"ok", "optional-missing-project"}),
        "zones_missing": zones_missing,
        "zones_optional_missing": zones_optional_missing,
        "zones_with_drift": zones_with_drift,
        "materialized_total": len(materialized_files),
        "materialized_ok": sum(1 for item in materialized_files if item.get("status") == "ok"),
        "materialized_with_issues": materialized_with_issues,
        "has_drift": (zones_missing + zones_with_drift + materialized_with_issues) > 0,
    }


def format_human(payload: dict) -> str:
    summary = payload.get("summary", {})
    lines = [
        "Проверка drift между factory-template и downstream project",
        f"- factory: {payload.get('factory')}",
        f"- project: {payload.get('project')}",
        "",
        "Сводка:",
        (
            "- sync zones: "
            f"ok={summary.get('zones_ok', 0)}, "
            f"drift={summary.get('zones_with_drift', 0)}, "
            f"missing={summary.get('zones_missing', 0)}, "
            f"optional-missing={summary.get('zones_optional_missing', 0)}, "
            f"total={summary.get('zones_total', 0)}"
        ),
        (
            "- materialized files: "
            f"ok={summary.get('materialized_ok', 0)}, "
            f"issues={summary.get('materialized_with_issues', 0)}, "
            f"total={summary.get('materialized_total', 0)}"
        ),
    ]

    lines.append("")
    lines.append("Детали sync zones:")
    for zone in payload.get("drift", []):
        status = zone.get("status", "unknown")
        lines.append(f"- {zone.get('path')}: {status}")
        if status in {"missing-source", "missing-project", "optional-missing-project"}:
            lines.append(
                "  "
                + f"factory_exists={zone.get('factory_exists')}, project_exists={zone.get('project_exists')}"
            )
            continue
        for key in ("left_only", "right_only", "diff_files", "funny_files"):
            values = zone.get(key) or []
            if values:
                lines.append(f"  {key}: {', '.join(values)}")

    lines.append("")
    lines.append("Детали materialized files:")
    for item in payload.get("materialized_files", []):
        lines.append(f"- {item.get('target')}: {item.get('status')} (source: {item.get('source')})")

    lines.append("")
    lines.append("Итог: drift detected." if summary.get("has_drift") else "Итог: drift не обнаружен.")
    return "\n".join(lines) + "\n"


def build_payload(factory: Path, project: Path) -> dict:
    drift = compare_dirs(factory, project)
    materialized = compare_materialized_files(factory, project)
    return {
        "factory": str(factory),
        "project": str(project),
        "drift": drift,
        "materialized_files": materialized,
        "summary": summarize(drift, materialized),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Проверяет расхождения между factory-template и downstream project по sync manifest.",
    )
    parser.add_argument("factory_root", help="Корень factory-template.")
    parser.add_argument("project_root", help="Корень downstream project.")
    parser.add_argument(
        "--format",
        choices=("json", "human"),
        default="json",
        help="Формат вывода (по умолчанию: json).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Вернуть exit code 2, если обнаружен drift/missing/issue.",
    )
    args = parser.parse_args()

    factory = Path(args.factory_root).resolve()
    project = Path(args.project_root).resolve()
    payload = build_payload(factory, project)

    if args.format == "human":
        print(format_human(payload), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.strict and payload.get("summary", {}).get("has_drift"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
