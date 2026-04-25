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

TIER_ORDER = ("safe", "advisory", "manual-only")


def render_materialized_clone(text: str) -> str:
    return f"{SYNC_HEADER}\n{text.strip()}\n"


def load_manifest() -> dict:
    manifest = Path(__file__).with_name("factory-sync-manifest.yaml")
    if not manifest.exists():
        return {}
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _normalize_zone_entry(entry: object) -> tuple[str, dict]:
    if isinstance(entry, str):
        return entry, {}
    if isinstance(entry, dict):
        path = str(entry.get("path", "")).strip()
        return path, entry
    return "", {}


def iter_tier_zones(manifest: dict) -> Iterable[tuple[str, str, dict]]:
    tiers = manifest.get("tiers")
    if isinstance(tiers, dict):
        for tier in TIER_ORDER:
            tier_data = tiers.get(tier, {}) or {}
            for entry in tier_data.get("zones", []) or []:
                path, meta = _normalize_zone_entry(entry)
                if path:
                    yield tier, path, meta
        return

    for entry in manifest.get("sync_zones", []) or []:
        path, meta = _normalize_zone_entry(entry)
        if path:
            yield "safe", path, meta
    for entry in manifest.get("advisory_only_zones", []) or []:
        path, meta = _normalize_zone_entry(entry)
        if path:
            yield "advisory", path, meta


def iter_materialized_files(manifest: dict) -> Iterable[tuple[str, dict]]:
    tiers = manifest.get("tiers")
    if isinstance(tiers, dict):
        for tier in TIER_ORDER:
            tier_data = tiers.get(tier, {}) or {}
            for mapping in tier_data.get("materialized_files", []) or []:
                if isinstance(mapping, dict):
                    yield tier, mapping
        return

    for mapping in manifest.get("materialized_files", []) or []:
        if isinstance(mapping, dict):
            yield "safe", mapping


def project_zone(project: Path, zone: str) -> Path:
    if zone.startswith("template-repo/template/"):
        return project / zone.replace("template-repo/template/", "", 1)
    return project / zone


def _join_rel(base: str, name: str) -> str:
    return f"{base}/{name}" if base else name


def _collect_dircmp(cmp: filecmp.dircmp, base: str, sink: dict[str, list[str]]) -> None:
    sink["factory_only"].extend(_join_rel(base, item) for item in cmp.left_only)
    sink["project_only"].extend(_join_rel(base, item) for item in cmp.right_only)
    sink["diff_files"].extend(_join_rel(base, item) for item in cmp.diff_files)
    sink["funny_files"].extend(_join_rel(base, item) for item in cmp.funny_files)
    for subdir_name, subcmp in cmp.subdirs.items():
        _collect_dircmp(subcmp, _join_rel(base, subdir_name), sink)


def classify_zone(status: str, buckets: dict[str, list[str]]) -> str:
    if status == "ok":
        return "no-drift"
    if status in {"missing-source", "missing-project", "optional-missing-project"}:
        return status
    signals = [key for key in ("factory_only", "project_only", "diff_files", "funny_files") if buckets.get(key)]
    if signals == ["diff_files"]:
        return "content-drift"
    if signals == ["factory_only"]:
        return "factory-only-new-files"
    if signals == ["project_only"]:
        return "project-only-extra-files"
    return "mixed-drift"


def compare_materialized_files(factory: Path, project: Path) -> list[dict]:
    report = []
    manifest = load_manifest()
    for tier, mapping in iter_materialized_files(manifest):
        source_rel = str(mapping.get("source", ""))
        target_rel = str(mapping.get("target", ""))
        source = factory / source_rel
        target = project / target_rel
        base = {
            "tier": tier,
            "source": source_rel,
            "target": target_rel,
            "mode": mapping.get("mode", "copy"),
            "note": mapping.get("note"),
            "apply_eligible": tier == "safe",
            "item_type": "materialized-file",
        }
        if not source.exists():
            report.append({**base, "status": "missing-source", "classification": "missing-source"})
            continue
        expected = source.read_text(encoding="utf-8")
        if mapping.get("mode") == "materialized-clone":
            expected = render_materialized_clone(expected)
        if not target.exists():
            report.append({**base, "status": "missing-target", "classification": "missing-target"})
            continue
        actual = target.read_text(encoding="utf-8")
        status = "ok" if actual == expected else "drift"
        report.append(
            {
                **base,
                "status": status,
                "classification": "no-drift" if status == "ok" else "content-drift",
            }
        )
    return report


def compare_dirs(factory: Path, project: Path) -> list[dict]:
    report = []
    manifest = load_manifest()
    for tier, rel, zone_meta in iter_tier_zones(manifest):
        source = factory / rel
        target = project_zone(project, rel)
        optional_in_project = bool(zone_meta.get("optional_in_project", False))
        base = {
            "tier": tier,
            "path": rel,
            "target_path": str(target.relative_to(project)) if target.is_relative_to(project) else str(target),
            "apply_eligible": tier == "safe",
            "optional_in_project": optional_in_project,
            "note": zone_meta.get("note"),
            "item_type": "zone",
        }
        if not source.exists() or not target.exists():
            if source.exists() and not target.exists() and optional_in_project:
                status = "optional-missing-project"
            else:
                status = "missing-source" if not source.exists() else "missing-project"
            buckets = {"factory_only": [], "project_only": [], "diff_files": [], "funny_files": []}
            report.append(
                {
                    **base,
                    "status": status,
                    "classification": classify_zone(status, buckets),
                    "factory_exists": source.exists(),
                    "project_exists": target.exists(),
                    **buckets,
                }
            )
            continue
        cmp = filecmp.dircmp(source, target)
        buckets = {"factory_only": [], "project_only": [], "diff_files": [], "funny_files": []}
        _collect_dircmp(cmp, "", buckets)
        has_diff = any(buckets[key] for key in ("factory_only", "project_only", "diff_files", "funny_files"))
        status = "drift" if has_diff else "ok"
        report.append(
            {
                **base,
                "status": status,
                "classification": classify_zone(status, buckets),
                "factory_exists": True,
                "project_exists": True,
                **buckets,
            }
        )
    return report


def summarize_by_tier(items: Iterable[dict]) -> dict:
    summary = {
        tier: {
            "total": 0,
            "ok": 0,
            "drift": 0,
            "missing": 0,
            "optional_missing": 0,
            "apply_eligible": tier == "safe",
        }
        for tier in TIER_ORDER
    }
    for item in items:
        tier = item.get("tier", "safe")
        bucket = summary.setdefault(
            tier,
            {"total": 0, "ok": 0, "drift": 0, "missing": 0, "optional_missing": 0, "apply_eligible": tier == "safe"},
        )
        status = item.get("status")
        bucket["total"] += 1
        if status in {"ok", "optional-missing-project"}:
            bucket["ok"] += 1
        if status in {"drift", "missing-target"}:
            bucket["drift"] += 1
        if status in {"missing-source", "missing-project"}:
            bucket["missing"] += 1
        if status == "optional-missing-project":
            bucket["optional_missing"] += 1
    return summary


def summarize(drift: Iterable[dict], materialized_files: Iterable[dict]) -> dict:
    drift = list(drift)
    materialized_files = list(materialized_files)
    all_items = drift + materialized_files
    zones_optional_missing = sum(1 for item in drift if item.get("status") == "optional-missing-project")
    zones_missing = sum(1 for item in drift if item.get("status") in {"missing-source", "missing-project"})
    zones_with_drift = sum(1 for item in drift if item.get("status") == "drift")
    materialized_with_issues = sum(1 for item in materialized_files if item.get("status") != "ok")
    tier_summary = summarize_by_tier(all_items)
    return {
        "zones_total": len(drift),
        "zones_ok": sum(1 for item in drift if item.get("status") in {"ok", "optional-missing-project"}),
        "zones_missing": zones_missing,
        "zones_optional_missing": zones_optional_missing,
        "zones_with_drift": zones_with_drift,
        "materialized_total": len(materialized_files),
        "materialized_ok": sum(1 for item in materialized_files if item.get("status") == "ok"),
        "materialized_with_issues": materialized_with_issues,
        "tiers": tier_summary,
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
        "",
        "Tiered impact:",
    ]
    for tier in TIER_ORDER:
        tier_summary = (summary.get("tiers") or {}).get(tier, {})
        lines.append(
            f"- {tier}: ok={tier_summary.get('ok', 0)}, drift={tier_summary.get('drift', 0)}, "
            f"missing={tier_summary.get('missing', 0)}, total={tier_summary.get('total', 0)}, "
            f"apply_eligible={tier_summary.get('apply_eligible', tier == 'safe')}"
        )

    lines.extend(["", "Детали zones:"])
    for zone in payload.get("drift", []):
        status = zone.get("status", "unknown")
        lines.append(f"- [{zone.get('tier')}] {zone.get('path')}: {status} / {zone.get('classification')}")
        if status in {"missing-source", "missing-project", "optional-missing-project"}:
            lines.append(f"  factory_exists={zone.get('factory_exists')}, project_exists={zone.get('project_exists')}")
            continue
        for key in ("factory_only", "project_only", "diff_files", "funny_files"):
            values = zone.get(key) or []
            if values:
                lines.append(f"  {key}: {', '.join(values)}")

    lines.extend(["", "Детали materialized files:"])
    for item in payload.get("materialized_files", []):
        lines.append(
            f"- [{item.get('tier')}] {item.get('target')}: {item.get('status')} "
            f"/ {item.get('classification')} (source: {item.get('source')})"
        )

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
