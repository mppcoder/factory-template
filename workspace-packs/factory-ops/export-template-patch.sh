#!/usr/bin/env bash
set -euo pipefail

TEMPLATE_ROOT="${1:-}"
PROJECT_ROOT="${2:-}"
MODE="${3:---dry-run}"

if [ -z "$TEMPLATE_ROOT" ] || [ -z "$PROJECT_ROOT" ]; then
  echo "Использование: export-template-patch.sh <template-root> <working-project-root> [--dry-run|--advisory]"
  exit 1
fi
case "$MODE" in
  --dry-run|--advisory) ;;
  *)
    echo "ОШИБКА: поддерживаются только режимы --dry-run и --advisory"
    exit 1
    ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/factory-sync-manifest.yaml"
BUNDLE_VERSION="$SCRIPT_DIR/sync-bundle-version.json"
OUT="$PROJECT_ROOT/_factory-sync-export"
mkdir -p "$OUT"

python3 - <<PYCODE
from __future__ import annotations

import datetime as dt
import difflib
import json
import shutil
from pathlib import Path

import yaml

SYNC_HEADER = """<!--
SYNCED FILE - DO NOT EDIT MANUALLY
Source of truth: template-repo/AGENTS.md
This root AGENTS.md is a materialized clone for the downstream repo.
Manual edits in this clone will be overwritten by the canonical template sync flow.
-->
"""
TIER_ORDER = ("safe-generated", "safe-clone", "advisory-review", "manual-project-owned")
LEGACY_TIER_ALIASES = {
    "safe": "safe-generated",
    "advisory": "advisory-review",
    "manual-only": "manual-project-owned",
}


def render_materialized_clone(text: str) -> str:
    return f"{SYNC_HEADER}\\n{text.strip()}\\n"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_version(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped[0].isdigit():
            return stripped
    return None


def project_zone(zone: str) -> Path:
    if zone.startswith("template-repo/template/"):
        return project / zone.replace("template-repo/template/", "", 1)
    return project / zone


def normalize_zone_entry(entry):
    if isinstance(entry, str):
        return entry, {}
    if isinstance(entry, dict):
        return str(entry.get("path", "")).strip(), entry
    return "", {}


def tier_name(raw: str) -> str:
    return LEGACY_TIER_ALIASES.get(raw, raw)


def tier_config(manifest: dict, tier: str) -> dict:
    tiers = manifest.get("tiers")
    if not isinstance(tiers, dict):
        return {}
    return tiers.get(tier, {}) or {}


def tier_apply_eligible(manifest: dict, tier: str) -> bool:
    config = tier_config(manifest, tier)
    if "apply_eligible" in config:
        return bool(config.get("apply_eligible"))
    return tier in {"safe-generated", "safe-clone"}


def tier_generates_patch_files(manifest: dict, tier: str) -> bool:
    config = tier_config(manifest, tier)
    if "generate_patch_files" in config:
        return bool(config.get("generate_patch_files"))
    return tier != "manual-project-owned"


def tier_operator_action(manifest: dict, tier: str) -> str:
    config = tier_config(manifest, tier)
    return str(config.get("operator_action") or "")


def tier_safety_reason(manifest: dict, tier: str) -> str:
    config = tier_config(manifest, tier)
    return str(config.get("safety_reason") or "")


def should_materialize(manifest: dict, tier: str, mode: str) -> bool:
    if mode == "--advisory":
        return False
    return tier_apply_eligible(manifest, tier)


def iter_tier_zones(manifest: dict):
    tiers = manifest.get("tiers")
    if isinstance(tiers, dict):
        for tier in TIER_ORDER:
            tier_data = tiers.get(tier, {}) or {}
            for entry in tier_data.get("zones", []) or []:
                zone, meta = normalize_zone_entry(entry)
                if zone:
                    yield tier, zone, meta
        for raw_tier, tier_data in tiers.items():
            tier = tier_name(raw_tier)
            if tier in TIER_ORDER:
                continue
            for entry in (tier_data or {}).get("zones", []) or []:
                zone, meta = normalize_zone_entry(entry)
                if zone:
                    yield tier, zone, meta
        return
    for entry in manifest.get("sync_zones", []) or []:
        zone, meta = normalize_zone_entry(entry)
        if zone:
            yield "safe-generated", zone, meta
    for entry in manifest.get("advisory_only_zones", []) or []:
        zone, meta = normalize_zone_entry(entry)
        if zone:
            yield "advisory-review", zone, meta


def iter_materialized_files(manifest: dict):
    tiers = manifest.get("tiers")
    if isinstance(tiers, dict):
        for tier in TIER_ORDER:
            tier_data = tiers.get(tier, {}) or {}
            for mapping in tier_data.get("materialized_files", []) or []:
                if isinstance(mapping, dict):
                    yield tier, mapping
        for raw_tier, tier_data in tiers.items():
            tier = tier_name(raw_tier)
            if tier in TIER_ORDER:
                continue
            for mapping in (tier_data or {}).get("materialized_files", []) or []:
                if isinstance(mapping, dict):
                    yield tier, mapping
        return
    for mapping in manifest.get("materialized_files", []) or []:
        if isinstance(mapping, dict):
            yield "safe-clone", mapping


def clean_output(out: Path) -> None:
    for file in out.glob("*.patch"):
        file.unlink()
    for name in (
        "changed-files.txt",
        "safe-changed-files.txt",
        "template-sync.patch",
        "patch-summary.md",
        "preview-changes.json",
        "bundle-metadata.json",
    ):
        target = out / name
        if target.exists():
            target.unlink()
    generated_dir = out / "generated-files"
    if generated_dir.exists():
        shutil.rmtree(generated_dir)


def write_patch(name: str, before: str, after: str, before_label: str, after_label: str) -> None:
    patch = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=before_label,
            tofile=after_label,
        )
    )
    (out / name).write_text(patch, encoding="utf-8")


def copy_generated(rel_target: Path, source: Path) -> None:
    generated_target = generated_dir / rel_target
    generated_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, generated_target)


def add_preview(entry: dict) -> None:
    preview.append(entry)
    tier = entry["tier"]
    tier_counts.setdefault(
        tier,
        {
            "total": 0,
            "generated": 0,
            "missing": 0,
            "apply_eligible": tier_apply_eligible(manifest, tier),
            "patch_files": 0,
        },
    )
    tier_counts[tier]["total"] += 1
    if entry.get("will_generate"):
        tier_counts[tier]["generated"] += 1
    if entry.get("patch"):
        tier_counts[tier]["patch_files"] += 1
    if entry.get("status", "").startswith("missing"):
        tier_counts[tier]["missing"] += 1


manifest = yaml.safe_load(Path(r"$MANIFEST").read_text(encoding="utf-8")) or {}
template = Path(r"$TEMPLATE_ROOT").resolve()
project = Path(r"$PROJECT_ROOT").resolve()
out = Path(r"$OUT").resolve()
generated_dir = out / "generated-files"
mode = r"$MODE"
clean_output(out)

version_meta = json.loads(read_text(Path(r"$BUNDLE_VERSION"))) if Path(r"$BUNDLE_VERSION").exists() else {}
template_version = parse_version(read_text(template / "VERSION.md")) or version_meta.get("template_version") or "unknown"
summary: list[str] = []
changed: list[str] = []
safe_changed: list[str] = []
preview: list[dict] = []
tier_counts = {
    tier: {
        "total": 0,
        "generated": 0,
        "missing": 0,
        "apply_eligible": tier_apply_eligible(manifest, tier),
        "patch_files": 0,
    }
    for tier in TIER_ORDER
}

for tier, zone, meta in iter_tier_zones(manifest):
    t_zone = template / zone
    p_zone = project_zone(zone)
    target_zone_rel = p_zone.relative_to(project) if p_zone.is_relative_to(project) else Path(zone)
    if not t_zone.exists() or not p_zone.exists():
        status = "missing-source" if not t_zone.exists() else "missing-project"
        if t_zone.exists() and not p_zone.exists() and bool(meta.get("optional_in_project", False)):
            status = "optional-missing-project"
        add_preview(
            {
                "tier": tier,
                "kind": "zone",
                "source": zone,
                "target": target_zone_rel.as_posix(),
                "status": status,
                "will_generate": False,
                "apply_eligible": False,
                "preview_mode": mode,
                "operator_action": tier_operator_action(manifest, tier),
                "safety_reason": tier_safety_reason(manifest, tier),
                "note": meta.get("note"),
            }
        )
        summary.append(
            f"- [{tier}] зона: {zone}\\n"
            f"  статус: {status}\\n"
            f"  generated: no\\n"
            f"  why: {tier_safety_reason(manifest, tier)}\\n"
            f"  action: {tier_operator_action(manifest, tier)}"
        )
        continue

    for t_file in sorted(t_zone.rglob("*")):
        if not t_file.is_file():
            continue
        rel = t_file.relative_to(t_zone)
        p_file = p_zone / rel
        if p_file.exists() and not p_file.is_file():
            continue
        before = read_text(p_file)
        after = read_text(t_file)
        status = "missing-target" if not p_file.exists() else "drift"
        if p_file.exists() and before == after:
            continue
        rel_target = target_zone_rel / rel
        patch_name = f"{tier}__{zone.replace('/', '__')}__{str(rel).replace('/', '__')}.patch"
        patch_file = patch_name if tier_generates_patch_files(manifest, tier) else None
        if patch_file:
            write_patch(patch_file, before, after, str(p_file), str(p_file))
        will_generate = should_materialize(manifest, tier, mode)
        if will_generate:
            copy_generated(rel_target, t_file)
            changed.append(f"{zone}/{rel}")
            safe_changed.append(rel_target.as_posix())
        add_preview(
            {
                "tier": tier,
                "kind": "zone-file",
                "source": f"{zone}/{rel.as_posix()}",
                "target": rel_target.as_posix(),
                "status": status,
                "patch": patch_file,
                "will_generate": will_generate,
                "apply_eligible": tier_apply_eligible(manifest, tier),
                "preview_mode": mode,
                "operator_action": tier_operator_action(manifest, tier),
                "safety_reason": tier_safety_reason(manifest, tier),
                "note": meta.get("note"),
            }
        )
        summary.append(
            f"- [{tier}] зона: {zone}\\n"
            f"  файл: {rel.as_posix()}\\n"
            f"  статус: {status}\\n"
            f"  generated: {'yes' if will_generate else 'no'}\\n"
            f"  why: {tier_safety_reason(manifest, tier)}\\n"
            f"  action: {tier_operator_action(manifest, tier)}"
        )

for tier, mapping in iter_materialized_files(manifest):
    source_rel = str(mapping.get("source", ""))
    target_rel = str(mapping.get("target", ""))
    source = template / source_rel
    target = project / target_rel
    if not source.exists():
        add_preview(
            {
                "tier": tier,
                "kind": "materialized-file",
                "source": source_rel,
                "target": target_rel,
                "status": "missing-source",
                "will_generate": False,
                "apply_eligible": False,
                "preview_mode": mode,
                "operator_action": tier_operator_action(manifest, tier),
                "safety_reason": tier_safety_reason(manifest, tier),
            }
        )
        continue
    rendered = source.read_text(encoding="utf-8")
    if mapping.get("mode") == "materialized-clone":
        rendered = render_materialized_clone(rendered)
    current = read_text(target)
    if current == rendered:
        continue
    patch_name = target_rel.replace("/", "__") + ".patch"
    patch_file = patch_name if tier_generates_patch_files(manifest, tier) else None
    if patch_file:
        write_patch(patch_file, current, rendered, str(target), str(target))
    will_generate = should_materialize(manifest, tier, mode)
    if will_generate:
        generated_target = generated_dir / target_rel
        generated_target.parent.mkdir(parents=True, exist_ok=True)
        generated_target.write_text(rendered, encoding="utf-8")
        changed.append(f"{source_rel} => {target_rel}")
        safe_changed.append(target_rel)
    add_preview(
        {
            "tier": tier,
            "kind": "materialized-file",
            "source": source_rel,
            "target": target_rel,
            "status": "missing-target" if not target.exists() else "drift",
            "patch": patch_file,
            "will_generate": will_generate,
            "apply_eligible": tier_apply_eligible(manifest, tier),
            "preview_mode": mode,
            "operator_action": tier_operator_action(manifest, tier),
            "safety_reason": tier_safety_reason(manifest, tier),
            "mode": mapping.get("mode", "copy"),
            "note": mapping.get("note"),
        }
    )
    summary.append(
        f"- [{tier}] materialized: {source_rel}\\n"
        f"  target: {target_rel}\\n"
        f"  режим: {'generated-sync' if will_generate else 'preview-only'}\\n"
        f"  why: {tier_safety_reason(manifest, tier)}\\n"
        f"  action: {tier_operator_action(manifest, tier)}"
    )

metadata = {
    **version_meta,
    "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "template_root": str(template),
    "project_root": str(project),
    "template_version": template_version,
    "sync_contract_version": manifest.get("sync_contract_version", version_meta.get("sync_contract_version")),
    "mode": mode,
    "tiers": tier_counts,
    "tier_order": TIER_ORDER,
    "safe_generated_files": len(safe_changed),
    "preview_items": len(preview),
}

(out / "changed-files.txt").write_text("\\n".join(changed) + ("\\n" if changed else ""), encoding="utf-8")
(out / "safe-changed-files.txt").write_text("\\n".join(safe_changed) + ("\\n" if safe_changed else ""), encoding="utf-8")
(out / "template-sync.patch").write_text(
    "".join(p.read_text(encoding="utf-8") + "\\n" for p in sorted(out.glob("*.patch"))),
    encoding="utf-8",
)
(out / "preview-changes.json").write_text(json.dumps(preview, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
(out / "bundle-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
(out / "patch-summary.md").write_text(
    "# Сводка patch bundle\\n\\n"
    f"- template_version: {template_version}\\n"
    f"- sync_contract_version: {metadata.get('sync_contract_version')}\\n"
    f"- mode: {mode}\\n\\n"
    "## Tiered preview\\n\\n"
    + "\\n".join(
        f"- {tier}: preview={tier_counts[tier]['total']}, "
        f"generated={tier_counts[tier]['generated']}, patches={tier_counts[tier]['patch_files']}, "
        f"missing={tier_counts[tier]['missing']}, "
        f"apply_eligible={tier_counts[tier]['apply_eligible']}"
        for tier in TIER_ORDER
    )
    + "\\n\\n## Changes\\n\\n"
    + ("\\n".join(summary) if summary else "Изменений не обнаружено.")
    + "\\n",
    encoding="utf-8",
)
print(f"Patch bundle собран в {out}")
print(
    "Tiered preview: "
    + ", ".join(f"{tier}=preview:{tier_counts[tier]['total']}/generated:{tier_counts[tier]['generated']}" for tier in TIER_ORDER)
)
PYCODE

if [ "$MODE" = "--dry-run" ]; then
  echo 'Режим dry-run: patch bundle подготовлен без применения.'
fi
