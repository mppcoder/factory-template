#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import tarfile
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "_sources-export" / "factory-template"
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"


def load_policy() -> dict:
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}


def copy_pack(pack_name: str, pack_data: dict) -> None:
    rel_paths = list(pack_data.get("files", []))
    purpose = pack_data.get("purpose", "").strip()
    pack_dir = OUT_ROOT / pack_name
    if pack_dir.exists():
        shutil.rmtree(pack_dir)
    pack_dir.mkdir(parents=True)

    manifest = {
        "pack_name": pack_name,
        "repo": "factory-template",
        "file_count": len(rel_paths),
        "purpose": purpose,
        "files": rel_paths,
    }
    for rel in rel_paths:
        src = ROOT / rel
        if not src.exists():
            raise FileNotFoundError(f"Missing source for pack {pack_name}: {rel}")
        dest = pack_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    (pack_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack_dir / "README.md").write_text(
        (
            f"# {pack_name}\n\n"
            f"- Source repo: `factory-template`\n"
            f"- Files: {len(rel_paths)}\n"
            f"- Purpose: {purpose or 'curated ChatGPT Project Sources pack for the current factory-template workflow.'}\n"
        ),
        encoding="utf-8",
    )

    tar_path = OUT_ROOT / f"{pack_name}.tar.gz"
    if tar_path.exists():
        tar_path.unlink()
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(pack_dir, arcname=pack_name)


def main() -> int:
    policy = load_policy()
    packs = policy.get("sources_packs", {})
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for name, pack_data in packs.items():
        copy_pack(name, pack_data)
    summary = OUT_ROOT / "SUMMARY.md"
    boundary = policy.get("boundary_actions", {})
    current_phase = boundary.get("current_phase", "controlled-fixes")
    current_pack = boundary.get("recommended_sources_pack", "sources-pack-core-20.tar.gz")
    lines = [
        "# Factory Template Sources Packs",
        "",
        f"Текущая phase recommendation: `{current_phase}` -> `{current_pack}`.",
        "",
        "Собраны curated packs:",
        "",
    ]
    for name, pack_data in packs.items():
        files = list(pack_data.get("files", []))
        purpose = pack_data.get("purpose", "").strip()
        suffix = f" — {purpose}" if purpose else ""
        lines.append(f"- `{name}`: {len(files)} файлов{suffix}")
    lines.extend(
        [
            "",
            "Phase-aware рекомендации:",
            "",
        ]
    )
    for phase_name, phase_cfg in boundary.get("phase_recommendations", {}).items():
        if not isinstance(phase_cfg, dict):
            continue
        pack_name = phase_cfg.get("recommended_sources_pack", "не указано")
        rationale = phase_cfg.get("rationale", "без пояснения")
        marker = " (current)" if phase_name == current_phase else ""
        lines.append(f"- `{phase_name}`{marker}: `{pack_name}` — {rationale}")
    lines.extend(
        [
            "",
            "Архивы находятся рядом с каталогами pack'ов в `_sources-export/factory-template/`.",
            "",
        ]
    )
    summary.write_text("\n".join(lines), encoding="utf-8")
    print(f"Curated sources packs exported to: {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
