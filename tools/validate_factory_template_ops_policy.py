#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"
TEMPLATE_PATH = ROOT / "factory_template_only_pack" / "templates" / "factory-template-boundary-actions.template.md"


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
                "template-repo/scripts/validate-project-preset.sh",
                "template-repo/scripts/validate-policy-preset.sh",
                "template-repo/scripts/validate-quality.sh",
                "template-repo/scripts/validate-handoff.sh",
                "template-repo/scripts/validate-codex-task-pack.sh",
                "template-repo/scripts/validate-defect-capture.sh",
                "template-repo/scripts/create-codex-task-pack.sh",
                "VALIDATE_FACTORY_FEEDBACK.sh",
                "TEST_REPORT.md",
            ],
            errors,
        )
        validator_count = sum(
            1 for rel in files
            if rel.startswith("template-repo/scripts/validate-")
        )
        if validator_count < 9:
            fail(f"{name}: ожидается минимум 9 validator scripts, сейчас {validator_count}", errors)


def validate_pack(name: str, pack: dict, errors: list[str]) -> None:
    files = pack.get("files")
    purpose = pack.get("purpose")
    if not isinstance(purpose, str) or not purpose.strip():
        fail(f"{name}: purpose должен быть непустой строкой", errors)
    if not isinstance(files, list):
        fail(f"{name}: files должен быть списком", errors)
        return
    if len(files) != 20:
        fail(f"{name}: ожидается ровно 20 файлов, сейчас {len(files)}", errors)
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
    validate_pack_semantics(name, files, errors)


def main() -> int:
    errors: list[str] = []
    if not POLICY_PATH.exists():
        print(f"ОШИБКА: отсутствует {POLICY_PATH}")
        return 1
    if not TEMPLATE_PATH.exists():
        print(f"ОШИБКА: отсутствует {TEMPLATE_PATH}")
        return 1

    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    packs = policy.get("sources_packs")
    boundary = policy.get("boundary_actions")

    if not isinstance(packs, dict) or not packs:
        fail("sources_packs должен быть непустым mapping", errors)
    else:
        for name, pack in packs.items():
            if not isinstance(pack, dict):
                fail(f"{name}: описание pack должно быть mapping", errors)
                continue
            validate_pack(name, pack, errors)

    if not isinstance(boundary, dict):
        fail("boundary_actions должен быть mapping", errors)
    else:
        repo_name = boundary.get("repo_name")
        project_name = boundary.get("project_name")
        recommended = boundary.get("recommended_sources_pack")
        available = boundary.get("available_sources_packs")
        uploads_dir = boundary.get("uploads_dir")

        if not isinstance(repo_name, str) or not repo_name.strip():
            fail("boundary_actions.repo_name должен быть непустой строкой", errors)
        if not isinstance(project_name, str) or not project_name.strip():
            fail("boundary_actions.project_name должен быть непустой строкой", errors)
        if not isinstance(uploads_dir, str) or not uploads_dir.strip():
            fail("boundary_actions.uploads_dir должен быть непустой строкой", errors)
        if not isinstance(available, list) or not available:
            fail("boundary_actions.available_sources_packs должен быть непустым списком", errors)
        else:
            if len(set(available)) != len(available):
                fail("boundary_actions.available_sources_packs содержит дубли", errors)
            pack_names = set(packs.keys()) if isinstance(packs, dict) else set()
            expected_archives = {f"{name}.tar.gz" for name in pack_names}
            for item in available:
                if not isinstance(item, str) or not item.endswith(".tar.gz"):
                    fail(f"boundary_actions.available_sources_packs: некорректное имя архива {item}", errors)
                    continue
                if item not in expected_archives:
                    fail(f"boundary_actions.available_sources_packs: архив {item} не соответствует описанным sources_packs", errors)
        if not isinstance(recommended, str) or not recommended.strip():
            fail("boundary_actions.recommended_sources_pack должен быть непустой строкой", errors)
        else:
            if isinstance(available, list) and recommended not in available:
                fail("boundary_actions.recommended_sources_pack должен входить в available_sources_packs", errors)

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    for placeholder in [
        "{{repo_name}}",
        "{{project_name}}",
        "{{root_path}}",
        "{{sources_export_dir}}",
        "{{recommended_sources_pack}}",
        "{{available_sources_packs_bullets}}",
        "{{uploads_dir}}",
    ]:
        if placeholder not in template_text:
            fail(f"Шаблон boundary actions не содержит обязательный placeholder {placeholder}", errors)

    if errors:
        print("FACTORY TEMPLATE OPS POLICY НЕВАЛИДНА")
        for err in errors:
            print(f"- {err}")
        return 1
    print("FACTORY TEMPLATE OPS POLICY ВАЛИДНА")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
