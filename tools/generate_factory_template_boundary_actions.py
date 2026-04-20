#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml

from factory_template_phase_detection import detect_phase, load_policy
from sources_profiles import get_profiles, find_profile_by_export_name
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
    policy = load_policy()
    cfg = policy.get("boundary_actions", {})
    profiles = get_profiles(policy)
    packs = cfg.get("available_sources_packs", [])
    available_bullets = "\n".join(f"   - `{name}`" for name in packs)
    detected = detect_phase(policy)
    current_phase = str(detected.get("phase", cfg.get("default_phase", "controlled-fixes")))
    current_pack = str(detected.get("recommended_sources_pack", cfg.get("recommended_sources_pack", "sources-pack-core-20.tar.gz")))
    detection_reason = "; ".join(detected.get("reasons", [])) if isinstance(detected.get("reasons"), list) else "phase detection reason unavailable"
    _, archive_profile = find_profile_by_export_name(profiles, current_pack.removesuffix(".tar.gz"))
    direct_profile_name = archive_profile.get("direct_profile") if isinstance(archive_profile, dict) else None
    direct_profile = profiles.get(direct_profile_name, {}) if isinstance(direct_profile_name, str) else {}
    direct_export = str(direct_profile.get("export_name", "core-hot-15"))
    phase_cfg = cfg.get("phase_recommendations", {})
    phase_lines: list[str] = []
    for phase_name, phase_data in phase_cfg.items():
        if not isinstance(phase_data, dict):
            continue
        marker = " (current)" if phase_name == current_phase else ""
        pack_name = phase_data.get("recommended_sources_pack", "не указано")
        rationale = phase_data.get("rationale", "без пояснения")
        phase_lines.append(
            f"   - `{phase_name}`{marker}: `{pack_name}` — {rationale}"
        )
    phase_bullets = "\n".join(phase_lines)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    text = render(
        template,
        {
            "repo_name": cfg.get("repo_name", "factory-template"),
            "project_name": cfg.get("project_name", "Factory Template"),
            "current_phase": current_phase,
            "phase_detection_reason": detection_reason,
            "root_path": str(ROOT),
            "sources_export_dir": str(ROOT / "_sources-export" / "factory-template"),
            "canonical_archive_pack": current_pack,
            "canonical_direct_profile": direct_export,
            "direct_sources_dir": str(ROOT / "_sources-export" / "factory-template" / direct_export),
            "recommended_sources_pack": current_pack,
            "available_sources_packs_bullets": available_bullets,
            "phase_recommendations_bullets": phase_bullets,
            "uploads_dir": cfg.get("uploads_dir", "/projects/_incoming"),
        },
    )
    doc.write_text(text, encoding="utf-8")
    print(f"Boundary actions guide generated: {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
