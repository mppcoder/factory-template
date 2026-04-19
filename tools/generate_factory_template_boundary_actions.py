#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "_boundary-actions"
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"
TEMPLATE_PATH = ROOT / "factory_template_only_pack" / "templates" / "factory-template-boundary-actions.template.md"


def render(template: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = OUT_DIR / "factory-template-boundary-actions.md"
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    cfg = policy.get("boundary_actions", {})
    packs = cfg.get("available_sources_packs", [])
    available_bullets = "\n".join(f"   - `{name}`" for name in packs)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    text = render(
        template,
        {
            "repo_name": cfg.get("repo_name", "factory-template"),
            "project_name": cfg.get("project_name", "Factory Template"),
            "root_path": str(ROOT),
            "sources_export_dir": str(ROOT / "_sources-export" / "factory-template"),
            "recommended_sources_pack": cfg.get("recommended_sources_pack", "sources-pack-core-20.tar.gz"),
            "available_sources_packs_bullets": available_bullets,
            "uploads_dir": cfg.get("uploads_dir", "/projects/_incoming"),
        },
    )
    doc.write_text(text, encoding="utf-8")
    print(f"Boundary actions guide generated: {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
