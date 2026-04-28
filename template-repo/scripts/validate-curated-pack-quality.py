#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


VALID_KINDS = {"archive_pack", "direct_sources"}
ROUTING_CRITICAL = [
    "template-repo/scenario-pack/00-master-router.md",
    "template-repo/scenario-pack/15-handoff-to-codex.md",
    "template-repo/scenario-pack/16-done-closeout.md",
    "docs/operator/factory-template/03-mode-routing-factory-template.md",
    "docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md",
    "template-repo/codex-routing.yaml",
]
PROFILE_EXPECTATIONS = {
    "core_archive": ["00-master-router", "15-handoff", "CURRENT_FUNCTIONAL_STATE"],
    "core_hot_direct": ["00-master-router", "15-handoff", "03-mode-routing", "04-vps-remote"],
    "release_archive": ["RELEASE", "TEST_REPORT", "CHANGELOG"],
    "bugfix_archive": ["validate-", "codex-routing", "scripts/"],
}


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def resolve_manifest(root: Path, manifest: str | None) -> Path:
    if manifest:
        return Path(manifest).resolve()
    return root / "factory" / "producer" / "packaging" / "sources" / "sources-profiles.yaml"


def validate_manifest(root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    data = read_yaml(manifest_path)
    profiles = data.get("profiles", {})
    if not isinstance(profiles, dict) or not profiles:
        return ["sources profiles manifest должен содержать непустой `profiles` mapping"]

    all_refs: dict[str, list[str]] = {}
    for profile_name, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"profile `{profile_name}` должен быть mapping")
            continue
        export_name = str(profile.get("export_name") or "").strip()
        kind = str(profile.get("kind") or "").strip()
        purpose = str(profile.get("purpose") or "").strip()
        files = profile.get("files")
        if not export_name:
            errors.append(f"profile `{profile_name}` не содержит export_name")
        if kind not in VALID_KINDS:
            errors.append(f"profile `{profile_name}` содержит неизвестный kind `{kind}`")
        if len(purpose) < 24:
            errors.append(f"profile `{profile_name}` purpose слишком короткий для usefulness check")
        if not isinstance(files, list) or not files:
            errors.append(f"profile `{profile_name}` должен содержать непустой files list")
            continue
        file_list = [str(item) for item in files]
        if len(file_list) != len(set(file_list)):
            errors.append(f"profile `{profile_name}` содержит duplicate files")
        max_files = 25 if kind == "archive_pack" else 20
        if len(file_list) > max_files:
            errors.append(f"profile `{profile_name}` over-noisy: {len(file_list)} files > {max_files}")
        for rel in file_list:
            all_refs.setdefault(rel, []).append(str(profile_name))
            if not (root / rel).exists() and not manifest_path.parent.joinpath(rel).exists():
                errors.append(f"profile `{profile_name}` ссылается на отсутствующий файл `{rel}`")
        joined = "\n".join(file_list)
        for token in PROFILE_EXPECTATIONS.get(str(profile_name), []):
            if token not in joined:
                errors.append(f"profile `{profile_name}` не похож на свой phase/profile fit: missing `{token}`")

    core_hot = profiles.get("core_hot_direct", {}) if isinstance(profiles.get("core_hot_direct"), dict) else {}
    core_archive = profiles.get("core_archive", {}) if isinstance(profiles.get("core_archive"), dict) else {}
    core_files = set(str(item) for item in core_hot.get("files", []) if isinstance(item, str)) | set(
        str(item) for item in core_archive.get("files", []) if isinstance(item, str)
    )
    for rel in ROUTING_CRITICAL:
        if rel not in core_files:
            errors.append(f"routing-critical doc отсутствует в core curated packs: `{rel}`")

    cold = profiles.get("core_cold_archive", {}) if isinstance(profiles.get("core_cold_archive"), dict) else {}
    hot_files = set(str(item) for item in core_hot.get("files", []) if isinstance(item, str))
    cold_files = set(str(item) for item in cold.get("files", []) if isinstance(item, str))
    overlap = sorted(hot_files & cold_files)
    if overlap:
        errors.append("core_hot_direct и core_cold_archive содержат stale duplicates: " + ", ".join(overlap))

    noisy_refs = sorted(rel for rel, owners in all_refs.items() if len(owners) > 4)
    if noisy_refs:
        errors.append("слишком много pack duplicates для одного файла: " + ", ".join(noisy_refs))

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate curated/reference sources pack quality beyond structure.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--manifest", help="Path to sources-profiles.yaml fixture")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = resolve_manifest(root, args.manifest)
    errors = validate_manifest(root, manifest)
    if errors:
        print("CURATED PACK QUALITY НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("CURATED PACK QUALITY ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
