#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import yaml
import json

from sources_profiles import get_profiles, profiles_path_from_policy

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"
TEMPLATE_PATH = ROOT / "factory_template_only_pack" / "templates" / "factory-template-boundary-actions.template.md"
EXPORT_ROOT = ROOT / "_sources-export" / "factory-template"


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def require_paths(name: str, files: set[str], required: list[str], errors: list[str]) -> None:
    for rel in required:
        if rel not in files:
            fail(f"{name}: отсутствует обязательный semantic-файл {rel}", errors)


def require_prefix_count(name: str, items: list[str], prefix: str, min_count: int, errors: list[str]) -> None:
    count = sum(1 for rel in items if rel.startswith(prefix))
    if count < min_count:
        fail(f"{name}: ожидается минимум {min_count} файлов с префиксом {prefix}, сейчас {count}", errors)


def validate_pack_semantics(name: str, files: list[str], errors: list[str]) -> None:
    file_set = set(files)
    if name == "sources-pack-core-20":
        require_paths(
            name,
            file_set,
            [
                "template-repo/scenario-pack/00-master-router.md",
                "template-repo/scenario-pack/01-global-rules.md",
                "template-repo/scenario-pack/15-handoff-to-codex.md",
                "factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md",
                "factory_template_only_pack/02-runbook-dlya-codex-factory-template.md",
                "README.md",
                "CHANGELOG.md",
                "CURRENT_FUNCTIONAL_STATE.md",
                "template-repo/project-presets.yaml",
                "template-repo/policy-presets.yaml",
                "template-repo/change-classes.yaml",
                "TEST_REPORT.md",
            ],
            errors,
        )
        require_prefix_count(name, files, "template-repo/scenario-pack/", 6, errors)
        require_prefix_count(name, files, "factory_template_only_pack/", 4, errors)

    elif name == "sources-pack-release-20":
        require_paths(
            name,
            file_set,
            [
                "FACTORY_MANIFEST.yaml",
                "RELEASE_BUILD.sh",
                "PRE_RELEASE_AUDIT.sh",
                "VERSION_SYNC_CHECK.sh",
                "CLEAN_VERIFY_ARTIFACTS.sh",
                "RELEASE_CHECKLIST.md",
                "VERIFY_SUMMARY.md",
                "RELEASE_NOTE_TEMPLATE.md",
                "meta-template-project/RELEASE_NOTES.md",
                "template-repo/TEMPLATE_MANIFEST.yaml",
            ],
            errors,
        )
        if "factory_template_only_pack/05-backlog-dorabotok-factory-template.md" in file_set:
            fail(f"{name}: backlog-файл не должен занимать место в release-oriented pack", errors)
        if "CONTROLLED_FIXES_AUDIT_2026-04-19.md" in file_set:
            fail(f"{name}: audit snapshot не должен заменять release-facing docs", errors)

    elif name == "sources-pack-bugfix-20":
        require_paths(
            name,
            file_set,
            [
                "template-repo/launcher.sh",
                "template-repo/scripts/validate-project-preset.py",
                "template-repo/scripts/validate-policy-preset.py",
                "template-repo/scripts/validate-quality.py",
                "template-repo/scripts/validate-handoff.py",
                "template-repo/scripts/validate-codex-task-pack.py",
                "template-repo/scripts/validate-codex-routing.py",
                "template-repo/scripts/validate-handoff-response-format.py",
                "template-repo/scripts/validate-defect-capture.py",
                "template-repo/scripts/create-codex-task-pack.py",
                "template-repo/codex-routing.yaml",
                "VALIDATE_FACTORY_FEEDBACK.sh",
            ],
            errors,
        )
        validator_count = sum(
            1 for rel in files
            if rel.startswith("template-repo/scripts/validate-")
        )
        if validator_count < 10:
            fail(f"{name}: ожидается минимум 10 validator scripts, сейчас {validator_count}", errors)


def validate_profile(name: str, profile: dict, errors: list[str]) -> None:
    export_name = profile.get("export_name")
    kind = profile.get("kind")
    files = profile.get("files")
    purpose = profile.get("purpose")
    if not isinstance(export_name, str) or not export_name.strip():
        fail(f"{name}: export_name должен быть непустой строкой", errors)
    if kind not in {"archive_pack", "direct_sources"}:
        fail(f"{name}: kind должен быть archive_pack или direct_sources", errors)
    if not isinstance(purpose, str) or not purpose.strip():
        fail(f"{name}: purpose должен быть непустой строкой", errors)
    if not isinstance(files, list):
        fail(f"{name}: files должен быть списком", errors)
        return
    expected_count = 20 if kind == "archive_pack" else 15
    if name == "core_cold_archive":
        expected_count = 5
    if len(files) != expected_count:
        fail(f"{name}: ожидается ровно {expected_count} файлов, сейчас {len(files)}", errors)
    seen: set[str] = set()
    for rel in files:
        if not isinstance(rel, str) or not rel.strip():
            fail(f"{name}: найден пустой или нестроковый путь", errors)
            continue
        if rel in seen:
            fail(f"{name}: дублируется путь {rel}", errors)
            continue
        seen.add(rel)
        if not (ROOT / rel).exists():
            fail(f"{name}: отсутствует файл {rel}", errors)
    if isinstance(export_name, str) and export_name.startswith("sources-pack-"):
        validate_pack_semantics(export_name, files, errors)


def validate_profiles_manifest(policy: dict, errors: list[str]) -> tuple[dict[str, dict], Path]:
    profiles_path = profiles_path_from_policy(policy)
    if not profiles_path.exists():
        fail(f"sources_profiles_manifest отсутствует: {profiles_path.relative_to(ROOT)}", errors)
        return {}, profiles_path
    data = yaml.safe_load(profiles_path.read_text(encoding="utf-8")) or {}
    version = data.get("profiles_manifest_version")
    if version != 1:
        fail("profiles_manifest_version должен быть равен 1", errors)
    profiles = get_profiles(policy)
    if not profiles:
        fail("profiles manifest должен содержать непустой mapping profiles", errors)
        return {}, profiles_path
    for profile_name, profile in profiles.items():
        if not isinstance(profile, dict):
            fail(f"{profile_name}: описание profile должно быть mapping", errors)
            continue
        validate_profile(profile_name, profile, errors)

    required_hot = [
        "template-repo/scenario-pack/00-master-router.md",
        "template-repo/scenario-pack/01-global-rules.md",
        "template-repo/scenario-pack/02-decision-policy.md",
        "template-repo/scenario-pack/03-stage-gates.md",
        "template-repo/scenario-pack/15-handoff-to-codex.md",
        "template-repo/scenario-pack/16-done-closeout.md",
        "factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md",
        "factory_template_only_pack/02-runbook-dlya-codex-factory-template.md",
        "factory_template_only_pack/03-mode-routing-factory-template.md",
        "factory_template_only_pack/07-AGENTS-factory-template.md",
        "CURRENT_FUNCTIONAL_STATE.md",
        "VERSION.md",
        "template-repo/change-classes.yaml",
        "template-repo/policy-presets.yaml",
        "template-repo/project-presets.yaml",
    ]
    required_cold = [
        "README.md",
        "CHANGELOG.md",
        "TEST_REPORT.md",
        "CONTROLLED_FIXES_AUDIT_2026-04-19.md",
        "meta-template-project/RELEASE_NOTES.md",
    ]
    core_archive = profiles.get("core_archive", {})
    core_hot = profiles.get("core_hot_direct", {})
    core_cold = profiles.get("core_cold_archive", {})
    archive_files = core_archive.get("files", []) if isinstance(core_archive, dict) else []
    hot_files = core_hot.get("files", []) if isinstance(core_hot, dict) else []
    cold_archive_files = core_cold.get("files", []) if isinstance(core_cold, dict) else []
    if core_archive.get("export_name") != "sources-pack-core-20":
        fail("core_archive.export_name должен быть sources-pack-core-20", errors)
    if core_hot.get("export_name") != "core-hot-15":
        fail("core_hot_direct.export_name должен быть core-hot-15", errors)
    if core_cold.get("export_name") != "core-cold-5":
        fail("core_cold_archive.export_name должен быть core-cold-5", errors)
    if archive_files and set(required_hot).difference(set(archive_files)):
        fail("core_archive должен включать весь hot-set как подмножество archive set", errors)
    if hot_files and list(hot_files) != required_hot:
        fail("core_hot_direct должен содержать ровно заданный список hot-файлов в фиксированном порядке", errors)
    cold_files = core_archive.get("cold_reference_files", []) if isinstance(core_archive, dict) else []
    if cold_files and list(cold_files) != required_cold:
        fail("core_archive.cold_reference_files должен совпадать с зафиксированным cold-set", errors)
    if cold_archive_files and list(cold_archive_files) != required_cold:
        fail("core_cold_archive должен содержать ровно зафиксированный cold-set", errors)
    if hot_files and archive_files and not set(hot_files).issubset(set(archive_files)):
        fail("core_hot_direct должен быть подмножеством core_archive", errors)
    if cold_archive_files and archive_files and not set(cold_archive_files).issubset(set(archive_files)):
        fail("core_cold_archive должен быть подмножеством core_archive", errors)
    if hot_files and cold_archive_files and set(hot_files).intersection(set(cold_archive_files)):
        fail("core_hot_direct и core_cold_archive не должны пересекаться", errors)
    if hot_files and cold_archive_files and archive_files:
        if set(hot_files).union(set(cold_archive_files)) != set(archive_files):
            fail("core_hot_direct + core_cold_archive должны в точности восстанавливать core_archive", errors)
    if any(rel in set(required_cold) for rel in hot_files):
        fail("core_hot_direct не должен содержать cold/reference/release-support файлы", errors)
    return profiles, profiles_path


def validate_exported_artifacts(profiles: dict[str, dict], errors: list[str]) -> None:
    if not EXPORT_ROOT.exists():
        return
    for profile_name, profile in profiles.items():
        export_name = str(profile.get("export_name", "")).strip()
        if not export_name:
            continue
        export_dir = EXPORT_ROOT / export_name
        manifest_path = export_dir / "manifest.json"
        readme_path = export_dir / "README.md"
        if not export_dir.exists():
            fail(f"exported profile отсутствует: _sources-export/factory-template/{export_name}", errors)
            continue
        if not manifest_path.exists():
            fail(f"{export_name}: отсутствует generated manifest.json", errors)
            continue
        if not readme_path.exists():
            fail(f"{export_name}: отсутствует generated README.md", errors)
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_files = manifest.get("files", [])
        if manifest.get("profile_name") != profile_name:
            fail(f"{export_name}: manifest.profile_name расходится с declarative profile", errors)
        if manifest.get("file_count") != len(manifest_files):
            fail(f"{export_name}: manifest.file_count расходится со списком files", errors)
        if manifest_files != profile.get("files", []):
            fail(f"{export_name}: manifest.files расходится с declarative profile", errors)
        if manifest.get("file_count") != len(profile.get("files", [])):
            fail(f"{export_name}: manifest.file_count расходится с declarative profile", errors)
        if manifest.get("export_layout") != profile.get("export_layout", "nested"):
            fail(f"{export_name}: manifest.export_layout расходится с declarative profile", errors)
        readme = readme_path.read_text(encoding="utf-8")
        if profile.get("kind") == "archive_pack":
            if export_name == "core-cold-5":
                if "cold/reference remainder archive" not in readme:
                    fail(f"{export_name}: README должен явно помечать cold/reference remainder archive", errors)
            elif "canonical archive pack" not in readme:
                fail(f"{export_name}: README должен явно помечать canonical archive pack", errors)
        if profile.get("kind") == "direct_sources":
            if "direct reference profile" not in readme:
                fail(f"{export_name}: README должен явно помечать direct reference profile", errors)
            if profile.get("export_layout") == "flat":
                if "flat-подпапке" not in readme:
                    fail(f"{export_name}: README должен явно описывать flat upload subdir", errors)
                exported_files = manifest.get("exported_files", [])
                if len(exported_files) != len(manifest_files):
                    fail(f"{export_name}: manifest.exported_files должен покрывать все source files", errors)
                export_names = [item.get("export_filename") for item in exported_files if isinstance(item, dict)]
                if len(export_names) != len(set(export_names)):
                    fail(f"{export_name}: manifest.exported_files содержит конфликтующие export_filename", errors)
                for item in exported_files:
                    if not isinstance(item, dict):
                        fail(f"{export_name}: manifest.exported_files должен содержать только mapping items", errors)
                        continue
                    for key in ["sha256", "md5", "size", "mtime_epoch"]:
                        if key not in item:
                            fail(f"{export_name}: export item `{item.get('export_filename', 'unknown')}` не содержит `{key}`", errors)
                bundled_artifacts = manifest.get("bundled_artifacts", [])
                bundled_names = [item.get("export_filename") for item in bundled_artifacts if isinstance(item, dict)]
                if len(bundled_names) != len(set(bundled_names)):
                    fail(f"{export_name}: manifest.bundled_artifacts содержит конфликтующие export_filename", errors)
                for item in bundled_artifacts:
                    if not isinstance(item, dict):
                        fail(f"{export_name}: manifest.bundled_artifacts должен содержать только mapping items", errors)
                        continue
                    for key in ["sha256", "md5", "size", "mtime_epoch"]:
                        if key not in item:
                            fail(f"{export_name}: bundled artifact `{item.get('export_filename', 'unknown')}` не содержит `{key}`", errors)
                upload_subdir = str(manifest.get("upload_subdir", profile.get("upload_subdir", "upload-to-sources")))
                upload_dir = export_dir / upload_subdir
                if not upload_dir.exists() or not upload_dir.is_dir():
                    fail(f"{export_name}: отсутствует upload subdir `{upload_subdir}`", errors)
                upload_subdir_files = manifest.get("upload_subdir_files", [])
                if sorted(upload_subdir_files) != sorted(export_names + bundled_names):
                    fail(f"{export_name}: manifest.upload_subdir_files должен совпадать с export filenames", errors)
                nested_upload_files = [p for p in upload_dir.rglob("*") if p.is_file() and p.parent != upload_dir]
                if nested_upload_files:
                    fail(f"{export_name}: upload subdir должен оставаться flat без вложенных файлов", errors)
                actual_upload_names = sorted(p.name for p in upload_dir.iterdir() if p.is_file())
                if actual_upload_names != sorted(export_names + bundled_names):
                    fail(f"{export_name}: upload subdir не совпадает с declared export filenames", errors)
                root_files = sorted(p.name for p in export_dir.iterdir() if p.is_file())
                if root_files != ["README.md", "manifest.json"]:
                    fail(f"{export_name}: корень direct export должен содержать только README.md и manifest.json", errors)


def main() -> int:
    errors: list[str] = []
    if not POLICY_PATH.exists():
        print(f"ОШИБКА: отсутствует {POLICY_PATH}")
        return 1
    if not TEMPLATE_PATH.exists():
        print(f"ОШИБКА: отсутствует {TEMPLATE_PATH}")
        return 1

    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    boundary = policy.get("boundary_actions")
    profiles, profiles_path = validate_profiles_manifest(policy, errors)
    archive_profiles = {
        name: profile for name, profile in profiles.items()
        if isinstance(profile, dict) and profile.get("kind") == "archive_pack"
    }
    validate_exported_artifacts(profiles, errors)

    if not isinstance(boundary, dict):
        fail("boundary_actions должен быть mapping", errors)
    else:
        repo_name = boundary.get("repo_name")
        project_name = boundary.get("project_name")
        completion_impacts = boundary.get("completion_impacts")
        default_phase = boundary.get("default_phase")
        recommended = boundary.get("recommended_sources_pack")
        phase_recommendations = boundary.get("phase_recommendations")
        phase_detection = boundary.get("phase_detection")
        available = boundary.get("available_sources_packs")
        uploads_dir = boundary.get("uploads_dir")

        if not isinstance(repo_name, str) or not repo_name.strip():
            fail("boundary_actions.repo_name должен быть непустой строкой", errors)
        if not isinstance(project_name, str) or not project_name.strip():
            fail("boundary_actions.project_name должен быть непустой строкой", errors)
        if not isinstance(completion_impacts, dict) or not completion_impacts:
            fail("boundary_actions.completion_impacts должен быть непустым mapping", errors)
        else:
            for key in [
                "factory_sources",
                "downstream_template_sync",
                "downstream_project_sources",
                "manual_archive_required",
                "delete_before_replace",
            ]:
                value = completion_impacts.get(key)
                if not isinstance(value, str) or not value.strip():
                    fail(f"boundary_actions.completion_impacts.{key} должен быть непустой строкой", errors)
        if not isinstance(uploads_dir, str) or not uploads_dir.strip():
            fail("boundary_actions.uploads_dir должен быть непустой строкой", errors)
        if not isinstance(default_phase, str) or not default_phase.strip():
            fail("boundary_actions.default_phase должен быть непустой строкой", errors)
        if not isinstance(available, list) or not available:
            fail("boundary_actions.available_sources_packs должен быть непустым списком", errors)
        else:
            if len(set(available)) != len(available):
                fail("boundary_actions.available_sources_packs содержит дубли", errors)
            expected_archives = {
                f"{profile.get('export_name')}.tar.gz"
                for profile in archive_profiles.values()
                if isinstance(profile.get("export_name"), str)
            }
            for item in available:
                if not isinstance(item, str) or not item.endswith(".tar.gz"):
                    fail(f"boundary_actions.available_sources_packs: некорректное имя архива {item}", errors)
                    continue
                if item not in expected_archives:
                    fail(f"boundary_actions.available_sources_packs: архив {item} не соответствует archive profiles из declarative manifest", errors)
        if not isinstance(recommended, str) or not recommended.strip():
            fail("boundary_actions.recommended_sources_pack должен быть непустой строкой", errors)
        else:
            if isinstance(available, list) and recommended not in available:
                fail("boundary_actions.recommended_sources_pack должен входить в available_sources_packs", errors)
        if not isinstance(phase_recommendations, dict) or not phase_recommendations:
            fail("boundary_actions.phase_recommendations должен быть непустым mapping", errors)
        else:
            if isinstance(default_phase, str) and default_phase not in phase_recommendations:
                fail("boundary_actions.default_phase должен существовать в phase_recommendations", errors)
            for phase_name, phase_cfg in phase_recommendations.items():
                if not isinstance(phase_cfg, dict):
                    fail(f"boundary_actions.phase_recommendations.{phase_name} должен быть mapping", errors)
                    continue
                phase_pack = phase_cfg.get("recommended_sources_pack")
                rationale = phase_cfg.get("rationale")
                if not isinstance(phase_pack, str) or not phase_pack.strip():
                    fail(f"boundary_actions.phase_recommendations.{phase_name}.recommended_sources_pack должен быть непустой строкой", errors)
                elif isinstance(available, list) and phase_pack not in available:
                    fail(f"boundary_actions.phase_recommendations.{phase_name}.recommended_sources_pack должен входить в available_sources_packs", errors)
                if not isinstance(rationale, str) or not rationale.strip():
                    fail(f"boundary_actions.phase_recommendations.{phase_name}.rationale должен быть непустой строкой", errors)
            if isinstance(default_phase, str) and isinstance(phase_recommendations, dict):
                active_cfg = phase_recommendations.get(default_phase)
                if isinstance(active_cfg, dict):
                    active_pack = active_cfg.get("recommended_sources_pack")
                    if isinstance(recommended, str) and isinstance(active_pack, str) and recommended != active_pack:
                        fail("boundary_actions.recommended_sources_pack должен совпадать с рекомендацией default_phase", errors)
        if not isinstance(phase_detection, dict) or not phase_detection:
            fail("boundary_actions.phase_detection должен быть непустым mapping", errors)
        else:
            for phase_name, phase_cfg in phase_detection.items():
                if not isinstance(phase_cfg, dict):
                    fail(f"boundary_actions.phase_detection.{phase_name} должен быть mapping", errors)
                    continue
                min_matches = phase_cfg.get("min_matches")
                require_document_intent = phase_cfg.get("require_document_intent", False)
                min_document_signal_matches = phase_cfg.get("min_document_signal_matches", 1)
                exact_paths = phase_cfg.get("exact_paths", [])
                prefixes = phase_cfg.get("path_prefixes", [])
                document_signals = phase_cfg.get("document_signals", {})
                document_signal_prefixes = phase_cfg.get("document_signal_prefixes", {})
                if not isinstance(min_matches, int) or min_matches < 1:
                    fail(f"boundary_actions.phase_detection.{phase_name}.min_matches должен быть целым >= 1", errors)
                if not isinstance(require_document_intent, bool):
                    fail(f"boundary_actions.phase_detection.{phase_name}.require_document_intent должен быть bool", errors)
                if not isinstance(min_document_signal_matches, int) or min_document_signal_matches < 1:
                    fail(f"boundary_actions.phase_detection.{phase_name}.min_document_signal_matches должен быть целым >= 1", errors)
                if not isinstance(exact_paths, list):
                    fail(f"boundary_actions.phase_detection.{phase_name}.exact_paths должен быть списком", errors)
                if not isinstance(prefixes, list):
                    fail(f"boundary_actions.phase_detection.{phase_name}.path_prefixes должен быть списком", errors)
                if isinstance(exact_paths, list) and isinstance(prefixes, list) and not exact_paths and not prefixes:
                    fail(f"boundary_actions.phase_detection.{phase_name} должен содержать exact_paths или path_prefixes", errors)
                if isinstance(exact_paths, list):
                    for rel in exact_paths:
                        if not isinstance(rel, str) or not rel.strip():
                            fail(f"boundary_actions.phase_detection.{phase_name}.exact_paths содержит пустой путь", errors)
                if isinstance(prefixes, list):
                    for prefix in prefixes:
                        if not isinstance(prefix, str) or not prefix.strip():
                            fail(f"boundary_actions.phase_detection.{phase_name}.path_prefixes содержит пустой префикс", errors)
                if not isinstance(document_signals, dict):
                    fail(f"boundary_actions.phase_detection.{phase_name}.document_signals должен быть mapping", errors)
                else:
                    for rel_path, patterns in document_signals.items():
                        if not isinstance(rel_path, str) or not rel_path.strip():
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signals содержит пустой путь", errors)
                            continue
                        if not isinstance(patterns, list) or not patterns:
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signals.{rel_path} должен быть непустым списком", errors)
                            continue
                        if not (ROOT / rel_path).exists():
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signals ссылается на отсутствующий файл {rel_path}", errors)
                        for pattern in patterns:
                            if not isinstance(pattern, str) or not pattern.strip():
                                fail(f"boundary_actions.phase_detection.{phase_name}.document_signals.{rel_path} содержит пустой pattern", errors)
                if not isinstance(document_signal_prefixes, dict):
                    fail(f"boundary_actions.phase_detection.{phase_name}.document_signal_prefixes должен быть mapping", errors)
                else:
                    for rel_prefix, patterns in document_signal_prefixes.items():
                        if not isinstance(rel_prefix, str) or not rel_prefix.strip():
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signal_prefixes содержит пустой префикс", errors)
                            continue
                        if not isinstance(patterns, list) or not patterns:
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signal_prefixes.{rel_prefix} должен быть непустым списком", errors)
                            continue
                        prefix_path = ROOT / rel_prefix
                        if not prefix_path.exists():
                            fail(f"boundary_actions.phase_detection.{phase_name}.document_signal_prefixes ссылается на отсутствующий путь {rel_prefix}", errors)
                        for pattern in patterns:
                            if not isinstance(pattern, str) or not pattern.strip():
                                fail(f"boundary_actions.phase_detection.{phase_name}.document_signal_prefixes.{rel_prefix} содержит пустой pattern", errors)

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    for placeholder in [
        "{{repo_name}}",
        "{{project_name}}",
        "{{current_phase}}",
        "{{phase_detection_reason}}",
        "{{root_path}}",
        "{{sources_export_dir}}",
        "{{canonical_archive_pack}}",
        "{{canonical_cold_archive_pack}}",
        "{{canonical_direct_profile}}",
        "{{direct_sources_dir}}",
        "{{recommended_sources_pack}}",
        "{{phase_override_packs_bullets}}",
        "{{phase_recommendations_bullets}}",
        "{{uploads_dir}}",
        "{{impact_factory_sources}}",
        "{{impact_downstream_template_sync}}",
        "{{impact_downstream_project_sources}}",
        "{{impact_manual_archive_required}}",
        "{{impact_delete_before_replace}}",
        "{{repo_patch_export_script}}",
        "{{repo_patch_apply_script}}",
    ]:
        if placeholder not in template_text:
            fail(f"Шаблон boundary actions не содержит обязательный placeholder {placeholder}", errors)

    for needle in [
        "## Модель воздействия",
        "## Completion package для repo-first instruction changes",
        "Удалить перед заменой",
        "Пошаговая инструкция по окнам",
    ]:
        if needle not in template_text:
            fail(f"Шаблон boundary actions не содержит обязательный раздел {needle}", errors)

    if errors:
        print("FACTORY TEMPLATE OPS POLICY НЕВАЛИДНА")
        for err in errors:
            print(f"- {err}")
        return 1
    print("FACTORY TEMPLATE OPS POLICY ВАЛИДНА")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
