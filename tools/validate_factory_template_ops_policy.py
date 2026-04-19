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
