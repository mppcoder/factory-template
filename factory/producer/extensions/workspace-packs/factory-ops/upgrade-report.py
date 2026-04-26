#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_TIER_ORDER = ("safe-generated", "safe-clone", "advisory-review", "manual-project-owned")


def run_drift(factory_root: Path, project_root: Path, script_dir: Path) -> dict:
    drift_script = script_dir / "check-template-drift.py"
    cmd = [
        sys.executable,
        str(drift_script),
        str(factory_root),
        str(project_root),
        "--format",
        "json",
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "check-template-drift.py завершился с ошибкой: "
            + (proc.stderr.strip() or proc.stdout.strip() or f"exit={proc.returncode}")
        )
    return json.loads(proc.stdout)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_bundle(bundle: Path) -> dict:
    changed_files_file = bundle / "changed-files.txt"
    changed_files = [line.strip() for line in read_text(changed_files_file).splitlines() if line.strip()]
    safe_changed_files_file = bundle / "safe-changed-files.txt"
    safe_changed_files = [line.strip() for line in read_text(safe_changed_files_file).splitlines() if line.strip()]
    generated_root = bundle / "generated-files"
    generated_files: list[str] = []
    if generated_root.exists():
        for file in sorted(generated_root.rglob("*")):
            if file.is_file():
                generated_files.append(str(file.relative_to(generated_root)).replace("\\", "/"))

    metadata_file = bundle / "bundle-metadata.json"
    preview_file = bundle / "preview-changes.json"
    metadata = json.loads(read_text(metadata_file)) if metadata_file.exists() else {}
    preview_changes = json.loads(read_text(preview_file)) if preview_file.exists() else []

    rollback_state_file = bundle / "applied-safe-zones" / "rollback-state.json"
    rollback_state = {}
    if rollback_state_file.exists():
        rollback_state = json.loads(read_text(rollback_state_file))

    return {
        "exists": bundle.exists(),
        "path": str(bundle),
        "changed_files": changed_files,
        "safe_changed_files": safe_changed_files,
        "generated_files": generated_files,
        "metadata": metadata,
        "tier_order": metadata.get("tier_order") or list(DEFAULT_TIER_ORDER),
        "preview_changes": preview_changes,
        "tier_preview": metadata.get("tiers", {}),
        "patch_summary_md": read_text(bundle / "patch-summary.md"),
        "rollback_state_exists": rollback_state_file.exists(),
        "rollback_state_path": str(rollback_state_file),
        "rollback_files_count": len(rollback_state.get("files", [])) if isinstance(rollback_state, dict) else 0,
        "applied_at": rollback_state.get("applied_at") if isinstance(rollback_state, dict) else None,
    }


def tier_order(patch: dict) -> list[str]:
    return list(patch.get("tier_order") or DEFAULT_TIER_ORDER)


def tier_group(tier: str) -> str:
    if tier in {"safe-generated", "safe-clone", "safe"}:
        return "safe"
    if tier in {"advisory-review", "advisory"}:
        return "advisory"
    return "manual-only"


def build_report(factory_root: Path, project_root: Path, patch_bundle: Path, script_dir: Path) -> dict:
    drift = run_drift(factory_root, project_root, script_dir)
    summary = drift.get("summary", {})
    bundle = load_bundle(patch_bundle)

    apply_script = script_dir / "apply-template-patch.sh"
    rollback_script = script_dir / "rollback-template-patch.sh"
    export_script = script_dir / "export-template-patch.sh"

    commands = {
        "export_dry_run": f"{export_script} {factory_root} {project_root} --dry-run",
        "apply_check": f"{apply_script} {patch_bundle} --check",
        "apply_safe_zones": f"{apply_script} {patch_bundle} --apply-safe-zones",
        "apply_safe_zones_with_snapshot": f"{apply_script} {patch_bundle} --apply-safe-zones --with-project-snapshot",
        "rollback_check": f"{rollback_script} {patch_bundle} --check",
        "rollback_apply": f"{rollback_script} {patch_bundle} --rollback",
        "rollback_apply_with_snapshot_restore": (
            f"{rollback_script} {patch_bundle} --rollback --restore-project-snapshot"
        ),
    }

    verdict = "no-changes"
    if summary.get("has_drift"):
        verdict = "drift-detected"
    if bundle.get("changed_files") or bundle.get("generated_files"):
        verdict = "patch-ready"
    if bundle.get("preview_changes") and not (bundle.get("changed_files") or bundle.get("generated_files")):
        verdict = "manual-review"

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "factory_root": str(factory_root),
        "project_root": str(project_root),
        "patch_bundle": bundle,
        "drift": drift,
        "commands": commands,
        "safe_upgrade_verdict": verdict,
        "rollback_ready": bundle.get("rollback_state_exists", False),
    }


def render_text(report: dict) -> str:
    patch = report["patch_bundle"]
    summary = report["drift"]["summary"]
    tier_preview = patch.get("tier_preview") or {}
    lines = [
        "Сводка безопасного downstream upgrade",
        f"сгенерировано_utc: {report['generated_at_utc']}",
        f"factory_root: {report['factory_root']}",
        f"downstream_project_root: {report['project_root']}",
        "",
        "Сводка drift:",
        (
            f"- зоны: ok={summary.get('zones_ok', 0)}, "
            f"drift={summary.get('zones_with_drift', 0)}, missing={summary.get('zones_missing', 0)}"
        ),
        (
            f"- materialized files: ok={summary.get('materialized_ok', 0)}, "
            f"issues={summary.get('materialized_with_issues', 0)}"
        ),
        f"- has_drift: {summary.get('has_drift', False)}",
        "",
        "Предпросмотр по уровням:",
    ]
    for tier in tier_order(patch):
        bucket = tier_preview.get(tier, {})
        drift_bucket = (summary.get("tiers") or {}).get(tier, {})
        lines.append(
            f"- {tier}: manifest_total={drift_bucket.get('total', 0)}, "
            f"preview={bucket.get('total', 0)}, generated={bucket.get('generated', 0)}, "
            f"apply_eligible={bucket.get('apply_eligible', tier in {'safe-generated', 'safe-clone'})}"
        )
    lines.extend(
        [
        "",
        "Patch bundle:",
        f"- путь: {patch['path']}",
        f"- template_version: {patch.get('metadata', {}).get('template_version', 'unknown')}",
        f"- changed_files: {len(patch['changed_files'])}",
        f"- safe_changed_files: {len(patch['safe_changed_files'])}",
        f"- generated_files: {len(patch['generated_files'])}",
        f"- rollback_state_exists: {patch['rollback_state_exists']}",
        f"- rollback_files_count: {patch['rollback_files_count']}",
        "",
        "Команды:",
        f"- export dry-run: {report['commands']['export_dry_run']}",
        f"- apply check: {report['commands']['apply_check']}",
        f"- применить safe zones: {report['commands']['apply_safe_zones']}",
        f"- применить safe zones со snapshot: {report['commands']['apply_safe_zones_with_snapshot']}",
        f"- проверить rollback: {report['commands']['rollback_check']}",
        f"- выполнить rollback: {report['commands']['rollback_apply']}",
        f"- выполнить rollback с восстановлением snapshot: {report['commands']['rollback_apply_with_snapshot_restore']}",
        "",
        f"safe_upgrade_verdict: {report['safe_upgrade_verdict']}",
        f"rollback_ready: {report['rollback_ready']}",
        ]
    )
    return "\n".join(lines) + "\n"


def render_markdown(report: dict) -> str:
    patch = report["patch_bundle"]
    summary = report["drift"]["summary"]
    cmd = report["commands"]
    tier_preview = patch.get("tier_preview") or {}
    preview_changes = patch.get("preview_changes") or []
    safe_items = [item for item in preview_changes if tier_group(str(item.get("tier"))) == "safe"]
    advisory_items = [item for item in preview_changes if tier_group(str(item.get("tier"))) == "advisory"]
    manual_items = [item for item in preview_changes if tier_group(str(item.get("tier"))) == "manual-only"]
    review_items = advisory_items + manual_items
    lines = [
        "# Сводка безопасного downstream upgrade",
        "",
        f"- Сгенерировано (UTC): `{report['generated_at_utc']}`",
        f"- Корень factory: `{report['factory_root']}`",
        f"- Корень downstream project: `{report['project_root']}`",
        f"- Версия template: `{patch.get('metadata', {}).get('template_version', 'unknown')}`",
        f"- Версия sync contract: `{patch.get('metadata', {}).get('sync_contract_version', 'unknown')}`",
        f"- Вердикт: `{report['safe_upgrade_verdict']}`",
        "",
        "## Снимок drift",
        "",
        (
            "- Sync zones / зоны синхронизации: "
            f"`ok={summary.get('zones_ok', 0)}` / "
            f"`drift={summary.get('zones_with_drift', 0)}` / "
            f"`missing={summary.get('zones_missing', 0)}` / "
            f"`total={summary.get('zones_total', 0)}`"
        ),
        (
            "- Materialized files / materialized-файлы: "
            f"`ok={summary.get('materialized_ok', 0)}` / "
            f"`issues={summary.get('materialized_with_issues', 0)}` / "
            f"`total={summary.get('materialized_total', 0)}`"
        ),
        "",
        "## Предпросмотр по уровням",
        "",
        "| Уровень | Пункты manifest | Пункты preview | Сгенерировано для apply | Можно применять |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for tier in tier_order(patch):
        bucket = tier_preview.get(tier, {})
        drift_bucket = (summary.get("tiers") or {}).get(tier, {})
        lines.append(
            f"| `{tier}` | `{drift_bucket.get('total', 0)}` | `{bucket.get('total', 0)}` | "
            f"`{bucket.get('generated', 0)}` | `{bucket.get('apply_eligible', tier in {'safe-generated', 'safe-clone'})}` |"
        )

    lines.extend(["", "## Что изменится", ""])
    if safe_items:
        lines.append("Безопасное применение переносит только сгенерированные файлы из уровней `safe-generated` и `safe-clone`:")
        lines.extend(
            f"- `{item.get('target')}` из `{item.get('source')}`"
            for item in safe_items
            if item.get("will_generate")
        )
    else:
        lines.append("Безопасные сгенерированные файлы для apply отсутствуют.")
    if advisory_items:
        lines.append("")
        lines.append("Файлы `advisory-review` содержат только подсказки для patch/diff и требуют ручного merge:")
        lines.extend(f"- `{item.get('target')}` статус=`{item.get('status')}`" for item in advisory_items[:20])
    if manual_items:
        lines.append("")
        lines.append("Файлы `manual-project-owned` являются только сигналом влияния и никогда не генерируются для apply:")
        lines.extend(f"- `{item.get('target')}` статус=`{item.get('status')}`" for item in manual_items[:20])

    lines.extend(["", "## Почему уровни безопасные или ручные", ""])
    for tier in tier_order(patch):
        tier_items = [item for item in preview_changes if item.get("tier") == tier]
        if not tier_items:
            continue
        sample = next((item for item in tier_items if item.get("operator_action") or item.get("safety_reason")), tier_items[0])
        tier_bucket = tier_preview.get(tier, {})
        lines.append(
            f"- `{tier}`: apply_eligible=`{tier_bucket.get('apply_eligible', sample.get('apply_eligible'))}`; "
            f"причина: {sample.get('safety_reason') or 'см. manifest'}; "
            f"действие оператора: {sample.get('operator_action') or 'см. manifest'}"
        )

    if preview_changes:
        lines.extend(["", "### Элементы preview", ""])
        for item in preview_changes[:40]:
            lines.append(
                f"- `[{item.get('tier')}]` `{item.get('target')}` "
                f"статус=`{item.get('status')}` generated=`{item.get('will_generate')}` "
                f"mode=`{item.get('preview_mode', patch.get('metadata', {}).get('mode', 'unknown'))}`"
            )
        if len(preview_changes) > 40:
            lines.append(f"- ...и еще `{len(preview_changes) - 40}` preview items")

    lines.extend(
        [
        "",
        "## Снимок upgrade bundle",
        "",
        f"- Путь bundle: `{patch['path']}`",
        f"- Измененных файлов в bundle: `{len(patch['changed_files'])}`",
        f"- Безопасных generated targets: `{len(patch['safe_changed_files'])}`",
        f"- Сгенерированных файлов для materialize: `{len(patch['generated_files'])}`",
        f"- Rollback state присутствует: `{patch['rollback_state_exists']}`",
        f"- Файлов под rollback tracking: `{patch['rollback_files_count']}`",
        ]
    )

    if patch["changed_files"]:
        lines.extend(["", "### Измененные файлы", ""])
        lines.extend([f"- `{item}`" for item in patch["changed_files"]])

    if patch["generated_files"]:
        lines.extend(["", "### Сгенерированные файлы для безопасного применения", ""])
        lines.extend([f"- `{item}`" for item in patch["generated_files"]])

    lines.extend(
        [
            "",
            "## Как откатить",
            "",
            "- Rollback metadata обязательна и записывается до копирования безопасных сгенерированных файлов.",
            "- `--rollback` восстанавливает отслеживаемые сгенерированные файлы или удаляет файлы, которых не было до apply.",
            "- `--rollback --restore-project-snapshot` восстанавливает полный project snapshot, если apply запускался с `--with-project-snapshot`.",
            "",
            "## Что пользователь должен проверить",
            "",
        ]
    )
    if review_items:
        lines.extend(
            f"- `{item.get('target')}` (`{item.get('tier')}`): {item.get('operator_action') or 'manual review'}"
            for item in review_items[:40]
        )
    else:
        lines.append("- В этом bundle нет advisory/manual пунктов для review.")
    lines.extend(
        [
            "",
            "## Канонические команды оператора",
            "",
            "1. Подготовить или обновить bundle (dry-run):",
            f"```bash\n{cmd['export_dry_run']}\n```",
            "2. Проверить bundle перед apply:",
            f"```bash\n{cmd['apply_check']}\n```",
            "3. Применить safe zones:",
            f"```bash\n{cmd['apply_safe_zones']}\n```",
            "4. Применить safe zones с full-project snapshot (optional, но безопаснее для смешанных ручных сессий):",
            f"```bash\n{cmd['apply_safe_zones_with_snapshot']}\n```",
            "5. Проверить rollback state:",
            f"```bash\n{cmd['rollback_check']}\n```",
            "6. Откатить safe-zone materialization при необходимости:",
            f"```bash\n{cmd['rollback_apply']}\n```",
            "7. Откатить и восстановить полный project snapshot, если использовался snapshot mode:",
            f"```bash\n{cmd['rollback_apply_with_snapshot_restore']}\n```",
            "",
            "## Заметки по безопасности UX",
            "",
            "- `--dry-run` и `--check` работают только на чтение.",
            "- `--apply-safe-zones` создает rollback metadata до overwrite generated targets.",
            "- `rollback-template-patch.sh --rollback` восстанавливает прежнее содержимое или удаляет файл, если до apply его не было.",
            "- Optional snapshot mode добавляет путь полного восстановления project для ручных изменений вне generated safe-zones.",
            "- Refresh ChatGPT Project Sources не входит в default downstream sync path, кроме legacy/hybrid проектов, где repo-first instructions все еще дублируются вне repo.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерирует человекочитаемый отчёт по downstream upgrade UX.")
    parser.add_argument("factory_root", help="Корень factory-template.")
    parser.add_argument("project_root", help="Корень downstream проекта.")
    parser.add_argument(
        "--patch-bundle",
        help="Путь к patch bundle (по умолчанию: <project_root>/_factory-sync-export).",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "text", "json"),
        default="markdown",
        help="Формат отчета (по умолчанию: markdown).",
    )
    parser.add_argument("--output", help="Куда сохранить отчет. Если не указан, печатает в stdout.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Вернуть exit code 2, если drift обнаружен и bundle не собран.",
    )
    args = parser.parse_args()

    factory_root = Path(args.factory_root).resolve()
    project_root = Path(args.project_root).resolve()
    patch_bundle = Path(args.patch_bundle).resolve() if args.patch_bundle else project_root / "_factory-sync-export"
    report = build_report(factory_root, project_root, patch_bundle, Path(__file__).resolve().parent)

    if args.format == "json":
        rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "text":
        rendered = render_text(report)
    else:
        rendered = render_markdown(report)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    should_fail = (
        args.strict
        and report["drift"]["summary"].get("has_drift")
        and not report["patch_bundle"].get("changed_files")
        and not report["patch_bundle"].get("generated_files")
    )
    return 2 if should_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
