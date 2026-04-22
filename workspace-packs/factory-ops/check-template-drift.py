#!/usr/bin/env python3
from __future__ import annotations
import filecmp
import json
import sys
from pathlib import Path
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


def compare_materialized_files(factory: Path, project: Path):
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

def compare_dirs(factory: Path, project: Path):
    report = []
    manifest = load_manifest()
    for rel in manifest.get("sync_zones", []):
        a = factory / rel
        b = project_zone(project, rel)
        if not a.exists() or not b.exists():
            report.append({"path": rel, "status": "missing", "factory_exists": a.exists(), "project_exists": b.exists()})
            continue
        cmp = filecmp.dircmp(a, b)
        report.append({"path": rel, "left_only": cmp.left_only, "right_only": cmp.right_only, "diff_files": cmp.diff_files, "funny_files": cmp.funny_files})
    return report

def main() -> int:
    if len(sys.argv) != 3:
        print("Использование: check-template-drift.py <корень-фабрики> <корень-проекта>")
        return 1
    factory = Path(sys.argv[1]).resolve()
    project = Path(sys.argv[2]).resolve()
    print(
        json.dumps(
            {
                "factory": str(factory),
                "project": str(project),
                "drift": compare_dirs(factory, project),
                "materialized_files": compare_materialized_files(factory, project),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
