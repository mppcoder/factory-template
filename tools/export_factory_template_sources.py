#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import tarfile
from pathlib import Path
import yaml

from factory_template_phase_detection import detect_phase
from sources_profiles import get_profiles
ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "_sources-export" / "factory-template"
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"


def load_policy() -> dict:
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}


def build_flat_export_names(rel_paths: list[str]) -> dict[str, str]:
    basename_counts: dict[str, int] = {}
    for rel in rel_paths:
        basename = Path(rel).name
        basename_counts[basename] = basename_counts.get(basename, 0) + 1

    result: dict[str, str] = {}
    used_names: set[str] = set()
    for rel in rel_paths:
        basename = Path(rel).name
        if basename_counts[basename] == 1:
            candidate = basename
        else:
            candidate = rel.replace("/", "__")
        if candidate in used_names:
            raise ValueError(f"Duplicate export filename for flat layout: {candidate}")
        used_names.add(candidate)
        result[rel] = candidate
    return result


def render_readme(profile_name: str, export_name: str, profile: dict, profiles: dict[str, dict]) -> str:
    rel_paths = list(profile.get("files", []))
    kind = str(profile.get("kind", "")).strip()
    purpose = str(profile.get("purpose", "")).strip()
    export_layout = str(profile.get("export_layout", "nested")).strip()
    lines = [
        f"# {export_name}",
        "",
        f"- Profile name: `{profile_name}`",
        f"- Source repo: `factory-template`",
        f"- Kind: `{kind}`",
        f"- Export layout: `{export_layout}`",
        f"- Files: {len(rel_paths)} content files",
        f"- Purpose: {purpose or 'factory-template Sources export profile'}",
        "",
    ]
    if kind == "archive_pack":
        if profile_name == "core_cold_archive":
            direct_profile_name = profile.get("direct_profile")
            direct_profile = profiles.get(direct_profile_name, {}) if isinstance(direct_profile_name, str) else {}
            direct_export = direct_profile.get("export_name", "не указан")
            canonical_profile_name = profile.get("canonical_archive_profile")
            canonical_profile = profiles.get(canonical_profile_name, {}) if isinstance(canonical_profile_name, str) else {}
            canonical_export = canonical_profile.get("export_name", "не указан")
            lines.extend(
                [
                    "## Role",
                    "",
                    "Это cold/reference remainder archive для hybrid-модели ChatGPT Project Sources.",
                    "",
                    "## Recommended Workflow",
                    "",
                    f"- Для ежедневной работы держите direct hot-set `{direct_export}`.",
                    f"- Этот archive загружайте как remainder без дублей hot-set.",
                    f"- Полный canonical snapshot `{canonical_export}` храните как reference bundle и резервный снимок состава.",
                    "",
                ]
            )
            return "\n".join(lines)
        direct_profile_name = profile.get("direct_profile")
        direct_profile = profiles.get(direct_profile_name, {}) if isinstance(direct_profile_name, str) else {}
        direct_export = direct_profile.get("export_name", "не указан")
        lines.extend(
            [
                "## Role",
                "",
                "Это canonical archive pack для полного steady-work snapshot по `factory-template`.",
                "",
                "## Daily Use",
                "",
                f"Для ежедневной работы в ChatGPT Project рекомендуется direct profile `{direct_export}`.",
                "Archive pack нужен как полный reference bundle и резервный снимок состава.",
                "",
            ]
        )
        cold_files = profile.get("cold_reference_files", [])
        if isinstance(cold_files, list) and cold_files:
            lines.extend(["## Cold / Reference Files", ""])
            for rel in cold_files:
                lines.append(f"- `{rel}`")
            lines.extend(["", "Эти файлы остаются частью archive snapshot и нужны для release audit, regression и post-mortem.", ""])
    elif kind == "direct_sources":
        archive_profile_name = profile.get("archive_profile")
        archive_profile = profiles.get(archive_profile_name, {}) if isinstance(archive_profile_name, str) else {}
        archive_export = archive_profile.get("export_name", "не указан")
        cold_archive_profile_name = profile.get("cold_archive_profile")
        cold_archive_profile = profiles.get(cold_archive_profile_name, {}) if isinstance(cold_archive_profile_name, str) else {}
        cold_archive_export = cold_archive_profile.get("export_name", "не указан")
        naming_strategy = str(profile.get("naming_strategy", "")).strip()
        lines.extend(
            [
                "## Role",
                "",
                "Это direct Sources profile для ежедневной загрузки в ChatGPT Project.",
                "",
                "## Recommended Workflow",
                "",
                "- Загружайте эти файлы напрямую в Sources проекта из одной flat-папки без подпапок.",
                f"- Cold/archive remainder `{cold_archive_export}` загружайте как отдельный архив без дублей hot-set.",
                f"- Canonical archive `{archive_export}` храните как полный steady-work snapshot и reference bundle.",
                "- Hot-set не заменяет archive pack и не живет как ручная копия: он генерируется из декларативного manifest.",
                "",
            ]
        )
        if export_layout == "flat":
            lines.extend(
                [
                    "## Flat Folder Rule",
                    "",
                    "- Все source-файлы для direct hot-set лежат в одной папке без вложенных директорий.",
                    "- По умолчанию имя файла совпадает с базовым именем исходника.",
                    f"- При конфликте базовых имён используется deterministic naming strategy: `{naming_strategy}`.",
                    "- Silent overwrite запрещён: конфликт должен быть разрешён на этапе генерации export.",
                    "",
                ]
            )
    return "\n".join(lines)


def export_profile(profile_name: str, profile: dict, profiles: dict[str, dict]) -> None:
    export_name = str(profile.get("export_name", "")).strip()
    rel_paths = list(profile.get("files", []))
    purpose = str(profile.get("purpose", "")).strip()
    kind = str(profile.get("kind", "")).strip()
    export_layout = str(profile.get("export_layout", "nested")).strip()
    naming_strategy = str(profile.get("naming_strategy", "")).strip()
    pack_dir = OUT_ROOT / export_name
    if pack_dir.exists():
        shutil.rmtree(pack_dir)
    pack_dir.mkdir(parents=True)

    exported_files: list[dict[str, str]] = []
    bundled_artifacts: list[dict[str, str]] = []
    flat_names = build_flat_export_names(rel_paths) if kind == "direct_sources" and export_layout == "flat" else {}

    manifest = {
        "profile_name": profile_name,
        "export_name": export_name,
        "repo": "factory-template",
        "kind": kind,
        "export_layout": export_layout,
        "file_count": len(rel_paths),
        "purpose": purpose,
        "files": rel_paths,
    }
    for extra_key in [
        "direct_profile",
        "archive_profile",
        "cold_archive_profile",
        "canonical_archive_profile",
        "cold_reference_files",
        "naming_strategy",
    ]:
        if extra_key in profile:
            manifest[extra_key] = profile[extra_key]
    for rel in rel_paths:
        src = ROOT / rel
        if not src.exists():
            raise FileNotFoundError(f"Missing source for profile {profile_name}: {rel}")
        if kind == "direct_sources" and export_layout == "flat":
            export_filename = flat_names[rel]
            dest = pack_dir / export_filename
        else:
            export_filename = rel
            dest = pack_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        exported_files.append({"source": rel, "export_filename": export_filename})

    if exported_files:
        manifest["exported_files"] = exported_files

    (pack_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack_dir / "README.md").write_text(
        render_readme(profile_name, export_name, profile, profiles),
        encoding="utf-8",
    )

    if kind == "archive_pack":
        tar_path = OUT_ROOT / f"{export_name}.tar.gz"
        if tar_path.exists():
            tar_path.unlink()
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(pack_dir, arcname=export_name)
    elif kind == "direct_sources":
        cold_archive_profile_name = profile.get("cold_archive_profile")
        cold_archive_profile = profiles.get(cold_archive_profile_name, {}) if isinstance(cold_archive_profile_name, str) else {}
        cold_archive_export = str(cold_archive_profile.get("export_name", "")).strip()
        if cold_archive_export:
            cold_tar_name = f"{cold_archive_export}.tar.gz"
            cold_tar_path = OUT_ROOT / cold_tar_name
            if cold_tar_path.exists():
                bundled_dest = pack_dir / cold_tar_name
                shutil.copy2(cold_tar_path, bundled_dest)
                bundled_artifacts.append(
                    {
                        "type": "archive_remainder",
                        "source": str(cold_tar_path.relative_to(ROOT)),
                        "export_filename": cold_tar_name,
                    }
                )
        if bundled_artifacts:
            manifest["bundled_artifacts"] = bundled_artifacts
            (pack_dir / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )


def main() -> int:
    policy = load_policy()
    profiles = get_profiles(policy)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for profile_name, profile in profiles.items():
        if not isinstance(profile, dict):
            continue
        export_profile(profile_name, profile, profiles)
    summary = OUT_ROOT / "SUMMARY.md"
    boundary = policy.get("boundary_actions", {})
    detected = detect_phase(policy)
    current_phase = str(detected.get("phase", boundary.get("default_phase", "controlled-fixes")))
    current_pack = str(detected.get("recommended_sources_pack", boundary.get("recommended_sources_pack", "sources-pack-core-20.tar.gz")))
    detection_reason = "; ".join(detected.get("reasons", [])) if isinstance(detected.get("reasons"), list) else "phase detection reason unavailable"
    core_archive = profiles.get("core_archive", {})
    canonical_archive_export = str(core_archive.get("export_name", "sources-pack-core-20"))
    direct_profile_name = core_archive.get("direct_profile") if isinstance(core_archive, dict) else None
    direct_profile = profiles.get(direct_profile_name, {}) if isinstance(direct_profile_name, str) else {}
    direct_export = str(direct_profile.get("export_name", "core-hot-15"))
    cold_archive_name = direct_profile.get("cold_archive_profile") if isinstance(direct_profile, dict) else None
    cold_archive = profiles.get(cold_archive_name, {}) if isinstance(cold_archive_name, str) else {}
    cold_archive_export = str(cold_archive.get("export_name", "core-cold-5"))
    lines = [
        "# Factory Template Sources Packs",
        "",
        f"Текущая phase recommendation для archive pack: `{current_phase}` -> `{current_pack}`.",
        f"Причина: {detection_reason}",
        "",
        f"Постоянная схема работы: direct hot-set `{direct_export}` в одной flat-папке + archive remainder `{cold_archive_export}.tar.gz` без дублей + canonical archive `{canonical_archive_export}.tar.gz` как reference snapshot.",
        "",
        "Собраны declarative profiles:",
        "",
    ]
    for profile_name, profile in profiles.items():
        export_name = profile.get("export_name", profile_name)
        files = list(profile.get("files", []))
        purpose = str(profile.get("purpose", "")).strip()
        kind = profile.get("kind", "unknown")
        suffix = f" — {purpose}" if purpose else ""
        lines.append(f"- `{export_name}` ({kind}): {len(files)} файлов{suffix}")
    lines.extend(
        [
            "",
            "Рекомендуемая стратегия Sources:",
            "",
            f"- для ежедневной работы загружать напрямую файлы из flat-папки `{direct_export}/` без подпапок",
            f"- `{cold_archive_export}.tar.gz` загружать как cold/reference archive remainder без дублей hot-set",
            f"- `{canonical_archive_export}.tar.gz` держать как canonical archive snapshot и полный reference bundle",
            "- phase-specific archive packs использовать только как operator override, а не как постоянный Sources set",
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
            "Архивы и direct profiles находятся рядом в `_sources-export/factory-template/`.",
            "",
        ]
    )
    summary.write_text("\n".join(lines), encoding="utf-8")
    print(f"Curated sources packs exported to: {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
