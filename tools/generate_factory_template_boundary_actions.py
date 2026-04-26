#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml

from factory_template_phase_detection import detect_phase, load_policy
from sources_profiles import get_profiles, find_profile_by_export_name
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "_boundary-actions"
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"
TEMPLATE_PATH = ROOT / "factory" / "producer" / "ops" / "templates" / "factory-template-boundary-actions.template.md"


def render(template: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = OUT_DIR / "factory-template-boundary-actions.md"
    policy = load_policy()
    cfg = policy.get("boundary_actions", {})
    impact_cfg = cfg.get("completion_impacts", {}) if isinstance(cfg, dict) else {}
    profiles = get_profiles(policy)
    detected = detect_phase(policy)
    current_phase = str(detected.get("phase", cfg.get("default_phase", "controlled-fixes")))
    current_pack = str(detected.get("recommended_sources_pack", cfg.get("recommended_sources_pack", "sources-pack-core-20.tar.gz")))
    detection_reason = "; ".join(detected.get("reasons", [])) if isinstance(detected.get("reasons"), list) else "phase detection reason unavailable"
    core_archive = profiles.get("core_archive", {})
    canonical_archive_export = str(core_archive.get("export_name", "sources-pack-core-20"))
    direct_profile_name = core_archive.get("direct_profile") if isinstance(core_archive, dict) else None
    direct_profile = profiles.get(direct_profile_name, {}) if isinstance(direct_profile_name, str) else {}
    direct_export = str(direct_profile.get("export_name", "core-hot-15"))
    cold_archive_name = direct_profile.get("cold_archive_profile") if isinstance(direct_profile, dict) else None
    cold_archive = profiles.get(cold_archive_name, {}) if isinstance(cold_archive_name, str) else {}
    cold_archive_export = str(cold_archive.get("export_name", "core-cold-5"))
    phase_cfg = cfg.get("phase_recommendations", {})
    phase_lines: list[str] = []
    phase_override_packs: list[str] = []
    for phase_name, phase_data in phase_cfg.items():
        if not isinstance(phase_data, dict):
            continue
        marker = " (current)" if phase_name == current_phase else ""
        pack_name = phase_data.get("recommended_sources_pack", "не указано")
        rationale = phase_data.get("rationale", "без пояснения")
        if isinstance(pack_name, str) and pack_name not in phase_override_packs:
            phase_override_packs.append(pack_name)
        phase_lines.append(
            f"   - `{phase_name}`{marker}: `{pack_name}` — {rationale}"
        )
    phase_bullets = "\n".join(phase_lines)
    phase_override_bullets = "\n".join(f"   - `{name}`" for name in phase_override_packs)
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
            "sources_sync_reports_dir": str(ROOT / "_sources-export" / "factory-template" / "_sync-reports"),
            "canonical_archive_pack": f"{canonical_archive_export}.tar.gz",
            "canonical_cold_archive_pack": f"{cold_archive_export}.tar.gz",
            "canonical_direct_profile": direct_export,
            "direct_sources_dir": str(ROOT / "_sources-export" / "factory-template" / direct_export),
            "recommended_sources_pack": current_pack,
            "phase_override_packs_bullets": phase_override_bullets,
            "phase_recommendations_bullets": phase_bullets,
            "uploads_dir": cfg.get("uploads_dir", "/projects/factory-template/_incoming"),
            "impact_factory_sources": impact_cfg.get("factory_sources", "Обновление repo-first инструкции проекта шаблона в ChatGPT"),
            "impact_downstream_template_sync": impact_cfg.get("downstream_template_sync", "Обновление шаблона в боевых repo"),
            "impact_downstream_project_sources": impact_cfg.get("downstream_project_sources", "Обновление repo-first инструкции боевых ChatGPT Projects"),
            "impact_manual_archive_required": impact_cfg.get("manual_archive_required", "Нужен готовый архив или каталог для ручной загрузки"),
            "impact_delete_before_replace": impact_cfg.get("delete_before_replace", "Перед заменой нужно удалить старую conflicting instruction"),
            "repo_patch_export_script": str(ROOT / "factory/producer/extensions/workspace-packs" / "factory-ops" / "export-template-patch.sh"),
            "repo_patch_apply_script": str(ROOT / "factory/producer/extensions/workspace-packs" / "factory-ops" / "apply-template-patch.sh"),
        },
    )
    doc.write_text(text, encoding="utf-8")
    print(f"Boundary actions guide generated: {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
