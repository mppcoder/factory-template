#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise AssertionError(f"command failed ({result.returncode}): {' '.join(cmd)}\n{result.stdout}")
    return result.stdout


def copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def assert_contains(path: Path, needle: str) -> None:
    if needle not in read(path):
        raise AssertionError(f"{path} does not contain {needle!r}")


def assert_not_contains(path: Path, needle: str) -> None:
    if not path.exists():
        return
    if needle in read(path):
        raise AssertionError(f"{path} unexpectedly contains {needle!r}")


def load_json(path: Path) -> dict | list:
    return json.loads(read(path))


def materialized_agents(source_text: str) -> str:
    return (
        "<!--\n"
        "SYNCED FILE - DO NOT EDIT MANUALLY\n"
        "Source of truth: template-repo/AGENTS.md\n"
        "This root AGENTS.md is a materialized clone for the downstream repo.\n"
        "Manual edits in this clone will be overwritten by the canonical template sync flow.\n"
        "-->\n\n"
        f"{source_text.strip()}\n"
    )


def prepare_template_copy(factory_root: Path, template_root: Path) -> None:
    for rel in [
        "VERSION.md",
        "template-repo/AGENTS.md",
        "template-repo/scenario-pack",
        "template-repo/template",
        "deploy/.env.example",
        "deploy/compose.yaml",
        "deploy/compose.production.yaml",
        "deploy/presets",
        "template-repo/scripts/deploy-dry-run.sh",
        "template-repo/scripts/deploy-local-vps.sh",
        "template-repo/scripts/operator-dashboard.py",
        "template-repo/scripts/validate-operator-env.py",
        "template-repo/scripts/preflight-vps-check.py",
        "docs/deploy-on-vps.md",
        "docs/production-vps-field-pilot.md",
        "reports/release/production-vps-field-pilot-report.md",
    ]:
        copy_path(factory_root / rel, template_root / rel)


def prepare_downstream_project(template_root: Path, project_root: Path) -> None:
    shutil.copytree(template_root / "template-repo" / "template", project_root, dirs_exist_ok=True)
    copy_path(template_root / "template-repo" / "scenario-pack", project_root / "template-repo" / "scenario-pack")
    write(project_root / "AGENTS.md", materialized_agents(read(template_root / "template-repo" / "AGENTS.md")))
    write(project_root / "README.md", "# Synthetic downstream\n")
    write(project_root / "deploy" / ".env", "DB_PASSWORD=project-secret\nAPP_IMAGE=project/app:manual\n")
    write(project_root / ".factory-runtime" / "reports" / "deploy-last-run.txt", "manual runtime transcript\n")
    write(project_root / "reports" / "release" / "field-pilot-local-transcript.md", "manual field pilot transcript\n")


def set_lifecycle(project_root: Path, *, converted: bool) -> None:
    profile_path = project_root / ".chatgpt" / "project-profile.yaml"
    stage_path = project_root / ".chatgpt" / "stage-state.yaml"
    profile = yaml.safe_load(read(profile_path)) or {}
    stage = yaml.safe_load(read(stage_path)) or {}
    if converted:
        profile.update(
            {
                "project_preset": "greenfield-product",
                "recommended_mode": "greenfield",
                "lifecycle_state": "greenfield-converted",
                "target_lifecycle_state": "greenfield-converted",
                "conversion_required": False,
            }
        )
        stage.setdefault("project", {})["mode"] = "greenfield"
        stage.setdefault("lifecycle", {}).update(
            {
                "previous_lifecycle_state": "brownfield-with-repo-adoption",
                "lifecycle_state": "greenfield-converted",
                "target_lifecycle_state": "greenfield-converted",
                "conversion_required": False,
                "conversion_gate_status": "passed",
            }
        )
    else:
        profile.update(
            {
                "project_preset": "brownfield-with-repo-modernization",
                "recommended_mode": "brownfield",
                "lifecycle_state": "brownfield-with-repo-adoption",
                "target_lifecycle_state": "greenfield-converted",
                "conversion_required": True,
            }
        )
        stage.setdefault("project", {})["mode"] = "brownfield"
        stage.setdefault("lifecycle", {}).update(
            {
                "lifecycle_state": "brownfield-with-repo-adoption",
                "target_lifecycle_state": "greenfield-converted",
                "conversion_required": True,
            }
        )
    write(profile_path, yaml.safe_dump(profile, allow_unicode=True, sort_keys=False))
    write(stage_path, yaml.safe_dump(stage, allow_unicode=True, sort_keys=False))


def export_bundle(factory_root: Path, template_root: Path, project_root: Path) -> Path:
    script = factory_root / "factory" / "producer" / "extensions" / "workspace-packs" / "factory-ops" / "export-template-patch.sh"
    run(["bash", str(script), str(template_root), str(project_root), "--dry-run"], cwd=factory_root)
    return project_root / "_factory-sync-export"


def apply_safe(factory_root: Path, bundle: Path) -> None:
    script = factory_root / "factory" / "producer" / "extensions" / "workspace-packs" / "factory-ops" / "apply-template-patch.sh"
    run(["bash", str(script), str(bundle), "--check"], cwd=factory_root)
    run(["bash", str(script), str(bundle), "--apply-safe-zones", "--with-project-snapshot"], cwd=factory_root)


def rollback(factory_root: Path, bundle: Path) -> None:
    script = factory_root / "factory" / "producer" / "extensions" / "workspace-packs" / "factory-ops" / "rollback-template-patch.sh"
    run(["bash", str(script), str(bundle), "--check"], cwd=factory_root)
    run(["bash", str(script), str(bundle), "--rollback", "--restore-project-snapshot"], cwd=factory_root)


def preview_items(bundle: Path) -> list[dict]:
    data = load_json(bundle / "preview-changes.json")
    if not isinstance(data, list):
        raise AssertionError("preview-changes.json must be a list")
    return data


def safe_targets(bundle: Path) -> set[str]:
    generated = bundle / "generated-files"
    if not generated.exists():
        return set()
    return {path.relative_to(generated).as_posix() for path in generated.rglob("*") if path.is_file()}


def assert_no_unsafe_generated(bundle: Path) -> None:
    generated = safe_targets(bundle)
    forbidden_prefixes = ("project-knowledge/", "work/", "brownfield/", ".factory-runtime/")
    forbidden_exact = {"deploy/.env", "reports/release/field-pilot-local-transcript.md"}
    for target in generated:
        if target in forbidden_exact or target.startswith(forbidden_prefixes):
            raise AssertionError(f"unsafe generated target: {target}")
    for item in preview_items(bundle):
        if item.get("will_generate") and item.get("tier") not in {"safe-generated", "safe-clone"}:
            raise AssertionError(f"non-safe preview item marked generated: {item}")


def validate_multi_cycle(factory_root: Path, tmp_root: Path) -> dict[str, object]:
    template_root = tmp_root / "template"
    project_root = tmp_root / "downstream"
    prepare_template_copy(factory_root, template_root)
    prepare_downstream_project(template_root, project_root)
    set_lifecycle(project_root, converted=False)

    append(project_root / ".chatgpt" / "examples" / "done-report.example.md", "\nOLD_SAFE_DRIFT\n")
    append(project_root / "tasks" / "codex" / "codex-task-mandatory-bug-capture.block.md", "\nOLD_TASK_BLOCK_DRIFT\n")
    append(project_root / "work-templates" / "user-spec.md.template", "\nOLD_WORK_TEMPLATE_DRIFT\n")
    append(project_root / "AGENTS.md", "\nOLD_ROOT_AGENTS_DRIFT\n")

    cycle1 = export_bundle(factory_root, template_root, project_root)
    apply_safe(factory_root, cycle1)
    assert_not_contains(project_root / ".chatgpt" / "examples" / "done-report.example.md", "OLD_SAFE_DRIFT")
    assert_not_contains(project_root / "AGENTS.md", "OLD_ROOT_AGENTS_DRIFT")
    assert_no_unsafe_generated(cycle1)

    append(project_root / "work" / "_task-template.md", "\nPROJECT_OWNED_MANUAL_EDIT\n")
    append(project_root / "project-knowledge" / "project.md", "\nADVISORY_LOCAL_PROJECT_INTENT\n")
    append(project_root / "deploy" / ".env", "MANUAL_SECRET_BOUNDARY=keep\n")
    append(project_root / ".factory-runtime" / "reports" / "deploy-last-run.txt", "manual rollback transcript keep\n")
    append(project_root / "reports" / "release" / "field-pilot-local-transcript.md", "local field pilot evidence keep\n")
    write(project_root / "docs" / "production-vps-field-pilot.md", "local downstream field pilot runbook\n")

    append(template_root / ".factory-sync-cycle-marker", "cycle3\n")
    append(template_root / "template-repo" / "template" / ".chatgpt" / "examples" / "done-report.example.md", "\nTEMPLATE_SAFE_CYCLE3\n")
    append(template_root / "template-repo" / "template" / "work-templates" / "user-spec.md.template", "\nTEMPLATE_WORK_TEMPLATE_CYCLE3\n")
    append(template_root / "template-repo" / "AGENTS.md", "\nTEMPLATE_AGENTS_CYCLE3\n")
    append(template_root / "deploy" / "presets" / "starter.yaml", "\n# TEMPLATE_DEPLOY_PRESET_CYCLE3\n")
    append(template_root / "template-repo" / "scripts" / "deploy-dry-run.sh", "\n# TEMPLATE_DEPLOY_SCRIPT_CYCLE3\n")
    append(template_root / "docs" / "production-vps-field-pilot.md", "\nTEMPLATE_FIELD_PILOT_DOC_CYCLE3\n")
    append(template_root / "reports" / "release" / "production-vps-field-pilot-report.md", "\nTEMPLATE_FIELD_PILOT_REPORT_CYCLE3\n")
    append(template_root / "template-repo" / "template" / "project-knowledge" / "project.md", "\nTEMPLATE_ADVISORY_PROJECT_KNOWLEDGE_CYCLE3\n")

    cycle3 = export_bundle(factory_root, template_root, project_root)
    metadata = load_json(cycle3 / "bundle-metadata.json")
    if not isinstance(metadata, dict):
        raise AssertionError("bundle metadata must be an object")
    if metadata.get("sync_contract_version") != 3:
        raise AssertionError("sync contract version must be 3")
    if metadata.get("project_lifecycle_status") != "conversion_ready":
        raise AssertionError(f"expected conversion_ready, got {metadata.get('project_lifecycle_status')}")
    assert_no_unsafe_generated(cycle3)
    generated = safe_targets(cycle3)
    for required in {
        ".chatgpt/examples/done-report.example.md",
        "work-templates/user-spec.md.template",
        "AGENTS.md",
        "deploy/presets/starter.yaml",
        "scripts/deploy-dry-run.sh",
    }:
        if required not in generated:
            raise AssertionError(f"expected generated safe target missing: {required}")

    advisory_targets = {
        item.get("target")
        for item in preview_items(cycle3)
        if item.get("tier") == "advisory-review" and not item.get("will_generate")
    }
    for required in {
        "docs/production-vps-field-pilot.md",
        "reports/release/production-vps-field-pilot-report.md",
        "project-knowledge/project.md",
    }:
        if required not in advisory_targets:
            raise AssertionError(f"expected advisory target missing: {required}")

    apply_safe(factory_root, cycle3)
    assert_contains(project_root / ".chatgpt" / "examples" / "done-report.example.md", "TEMPLATE_SAFE_CYCLE3")
    assert_contains(project_root / "AGENTS.md", "TEMPLATE_AGENTS_CYCLE3")
    assert_contains(project_root / "deploy" / "presets" / "starter.yaml", "TEMPLATE_DEPLOY_PRESET_CYCLE3")
    assert_contains(project_root / "scripts" / "deploy-dry-run.sh", "TEMPLATE_DEPLOY_SCRIPT_CYCLE3")
    assert_not_contains(project_root / "docs" / "production-vps-field-pilot.md", "TEMPLATE_FIELD_PILOT_DOC_CYCLE3")
    assert_not_contains(project_root / "reports" / "release" / "production-vps-field-pilot-report.md", "TEMPLATE_FIELD_PILOT_REPORT_CYCLE3")
    assert_not_contains(project_root / "project-knowledge" / "project.md", "TEMPLATE_ADVISORY_PROJECT_KNOWLEDGE_CYCLE3")
    for path, marker in [
        (project_root / "work" / "_task-template.md", "PROJECT_OWNED_MANUAL_EDIT"),
        (project_root / "project-knowledge" / "project.md", "ADVISORY_LOCAL_PROJECT_INTENT"),
        (project_root / "deploy" / ".env", "MANUAL_SECRET_BOUNDARY=keep"),
        (project_root / ".factory-runtime" / "reports" / "deploy-last-run.txt", "manual rollback transcript keep"),
        (project_root / "reports" / "release" / "field-pilot-local-transcript.md", "local field pilot evidence keep"),
    ]:
        assert_contains(path, marker)

    state = load_json(cycle3 / "applied-safe-zones" / "rollback-state.json")
    if not isinstance(state, dict) or state.get("version") != 3 or state.get("status") != "applied":
        raise AssertionError("rollback state metadata is invalid")
    tracked = {item.get("relative_path") for item in state.get("files", [])}
    if not {".chatgpt/examples/done-report.example.md", "AGENTS.md", "deploy/presets/starter.yaml"}.issubset(tracked):
        raise AssertionError("rollback state does not track expected safe files")
    if tracked.intersection({"deploy/.env", "docs/production-vps-field-pilot.md", "project-knowledge/project.md"}):
        raise AssertionError("rollback state tracks non-safe files")

    append(project_root / "README.md", "\nPOST_APPLY_MANUAL_MARKER\n")
    rollback(factory_root, cycle3)
    assert_not_contains(project_root / ".chatgpt" / "examples" / "done-report.example.md", "TEMPLATE_SAFE_CYCLE3")
    assert_not_contains(project_root / "deploy" / "presets" / "starter.yaml", "TEMPLATE_DEPLOY_PRESET_CYCLE3")
    assert_not_contains(project_root / "README.md", "POST_APPLY_MANUAL_MARKER")
    assert_contains(project_root / "work" / "_task-template.md", "PROJECT_OWNED_MANUAL_EDIT")
    assert_contains(project_root / "deploy" / ".env", "MANUAL_SECRET_BOUNDARY=keep")
    rollback_result = load_json(cycle3 / "applied-safe-zones" / "rollback-result.json")
    if not isinstance(rollback_result, dict) or not rollback_result.get("project_snapshot_restored"):
        raise AssertionError("rollback result must confirm project snapshot restore")

    return {
        "cycle1_generated": len(safe_targets(cycle1)),
        "cycle3_generated": len(safe_targets(cycle3)),
        "cycle3_advisory_targets": sorted(str(item) for item in advisory_targets),
        "cycle3_tracked_rollback_files": sorted(str(item) for item in tracked),
        "project_root": str(project_root),
    }


def validate_brownfield_conversion(factory_root: Path, tmp_root: Path) -> dict[str, object]:
    template_root = tmp_root / "template-brownfield"
    project_root = tmp_root / "converted-greenfield"
    prepare_template_copy(factory_root, template_root)
    prepare_downstream_project(template_root, project_root)
    set_lifecycle(project_root, converted=True)
    write(project_root / "brownfield" / "system-inventory.md", "REAL BROWNFIELD HISTORY KEEP\n")
    append(template_root / "template-repo" / "template" / "brownfield" / "system-inventory.md", "\nTEMPLATE_BROWNFIELD_STARTER_UPDATE\n")
    append(template_root / "template-repo" / "template" / ".chatgpt" / "examples" / "done-report.example.md", "\nTEMPLATE_SAFE_CONVERTED_UPDATE\n")

    bundle = export_bundle(factory_root, template_root, project_root)
    metadata = load_json(bundle / "bundle-metadata.json")
    if not isinstance(metadata, dict) or metadata.get("project_lifecycle_status") != "converted_greenfield":
        raise AssertionError("converted brownfield project must be detected as converted_greenfield")
    brownfield_items = [item for item in preview_items(bundle) if item.get("target", "").startswith("brownfield/")]
    if not brownfield_items:
        raise AssertionError("brownfield history must appear in preview")
    if any(item.get("will_generate") for item in brownfield_items):
        raise AssertionError("brownfield history must never be generated")
    apply_safe(factory_root, bundle)
    assert_contains(project_root / "brownfield" / "system-inventory.md", "REAL BROWNFIELD HISTORY KEEP")
    assert_not_contains(project_root / "brownfield" / "system-inventory.md", "TEMPLATE_BROWNFIELD_STARTER_UPDATE")
    assert_contains(project_root / ".chatgpt" / "examples" / "done-report.example.md", "TEMPLATE_SAFE_CONVERTED_UPDATE")
    return {
        "project_lifecycle_status": metadata.get("project_lifecycle_status"),
        "brownfield_preview_items": len(brownfield_items),
        "project_root": str(project_root),
    }


def render_report(results: dict[str, object]) -> str:
    multi = results["multi_cycle"]
    brownfield = results["brownfield_conversion"]
    return f"""# Отчет downstream multi-cycle sync

Дата проверки: 2026-04-27.

## Вердикт

`passed`: downstream sync v3 выдержал synthetic multi-cycle proof без перезаписи project-owned зон.

## Проверенные циклы

1. Первичная template sync: safe-generated/safe-clone drift был обнаружен и применен controlled apply.
2. Ручные project-owned edits: live `work/`, advisory `project-knowledge/`, `deploy/.env`, `.factory-runtime/` и local field-pilot transcript получили ручные маркеры.
3. Safe-generated update: template-owned `.chatgpt/examples`, `work-templates`, root `AGENTS.md`, deploy preset и deploy script применились.
4. Advisory review: production VPS field pilot docs/report и `project-knowledge/project.md` появились только как review-only targets и не были применены автоматически.
5. Rollback: rollback metadata version 3 был создан после нескольких циклов, `--rollback --restore-project-snapshot` восстановил pre-apply snapshot.
6. Brownfield conversion: `converted_greenfield` сохранил real brownfield history, safe-зоны продолжили обновляться.

## Evidence / проверочные факты

- Cycle 1 generated safe targets: `{multi['cycle1_generated']}`.
- Cycle 3 generated safe targets: `{multi['cycle3_generated']}`.
- Cycle 3 advisory targets: `{', '.join(multi['cycle3_advisory_targets'])}`.
- Rollback tracked safe files: `{', '.join(multi['cycle3_tracked_rollback_files'])}`.
- Brownfield lifecycle status: `{brownfield['project_lifecycle_status']}`.
- Brownfield preview items protected: `{brownfield['brownfield_preview_items']}`.

## Production VPS field-pilot boundary / граница field pilot

- Safe/template-owned apply: `deploy/.env.example`, compose files, deploy presets, `scripts/deploy-dry-run.sh`, `scripts/deploy-local-vps.sh`, `scripts/operator-dashboard.py`, `scripts/validate-operator-env.py`, `scripts/preflight-vps-check.py`.
- Review-only: `docs/deploy-on-vps.md`, `docs/production-vps-field-pilot.md`, `reports/release/production-vps-field-pilot-report.md`.
- Manual-only/protected: `deploy/.env`, `.factory-runtime/`, local field-pilot transcripts, backup/rollback runtime transcripts, real VPS approval boundary and secrets.

## Честное ограничение

Это synthetic repo-controlled proof. Он не заменяет реальный production VPS deploy, backup restore test или rollback drill: эти действия требуют отдельного user approval, доступа к VPS и ручного secrets/runtime boundary.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверить downstream sync v3 через несколько safe/advisory/manual циклов.")
    parser.add_argument("factory_root", nargs="?", default=".", help="Path to factory-template root")
    parser.add_argument("--report-output", help="Optional markdown report output path")
    args = parser.parse_args()
    factory_root = Path(args.factory_root).resolve()
    with tempfile.TemporaryDirectory(prefix="downstream-multi-cycle-sync-") as tmp:
        tmp_root = Path(tmp)
        results = {
            "multi_cycle": validate_multi_cycle(factory_root, tmp_root / "multi-cycle"),
            "brownfield_conversion": validate_brownfield_conversion(factory_root, tmp_root / "brownfield"),
        }
        report = render_report(results)
        if args.report_output:
            output = Path(args.report_output).resolve()
            write(output, report)
        print("DOWNSTREAM MULTI-CYCLE SYNC PROOF ПРОЙДЕН")
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
