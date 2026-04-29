#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def bullet(items: Any, empty: str = "- нет") -> str:
    if not isinstance(items, list) or not items:
        return empty
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            item_id = item.get("id") or item.get("name") or item.get("layer") or "item"
            summary = item.get("summary") or item.get("action") or item.get("url") or item.get("reason") or ""
            lines.append(f"- `{item_id}`: {summary}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def render(root: Path) -> str:
    inventory = load_yaml(root / ".chatgpt/software-inventory.yaml")
    watchlist = load_yaml(root / ".chatgpt/software-update-watchlist.yaml")
    readiness = load_yaml(root / ".chatgpt/software-update-readiness.yaml")

    baseline = inventory.get("baseline", {}) if isinstance(inventory.get("baseline"), dict) else {}
    os_data = baseline.get("os", {}) if isinstance(baseline.get("os"), dict) else {}
    package_manager = baseline.get("package_manager", {}) if isinstance(baseline.get("package_manager"), dict) else {}
    unattended = package_manager.get("unattended_upgrades", {}) if isinstance(package_manager.get("unattended_upgrades"), dict) else {}
    runtime = baseline.get("runtime_stack", {}) if isinstance(baseline.get("runtime_stack"), dict) else {}
    proposal = readiness.get("upgrade_proposal", {}) if isinstance(readiness.get("upgrade_proposal"), dict) else {}

    lines = [
        "# Software Update Readiness",
        "",
        f"Generated UTC: `{datetime.now(timezone.utc).replace(microsecond=0).isoformat()}`",
        "",
        "## Policy",
        "",
        f"- auto-update policy: `{readiness.get('auto_update_policy') or inventory.get('auto_update_policy', '')}`",
        f"- auto-upgrade allowed: `{text(readiness.get('auto_upgrade_allowed'), 'false')}`",
        f"- user approval required: `{text(readiness.get('user_approval_required'), 'true')}`",
        "",
        "## Current Baseline",
        "",
        f"- status: `{baseline.get('status', readiness.get('baseline_status', ''))}`",
        f"- recorded at: `{baseline.get('recorded_at', '') or 'not recorded'}`",
        f"- OS: `{os_data.get('distro_name', '')}` `{os_data.get('version', '')}` `{os_data.get('codename', '')}`",
        f"- selected Ubuntu LTS release: `{os_data.get('selected_ubuntu_lts_release', '') or 'not recorded'}`",
        f"- provider image id: `{os_data.get('provider_image_id', '') or 'not recorded'}`",
        f"- kernel: `{os_data.get('kernel', '') or 'not recorded'}`",
        f"- later package update state: `{os_data.get('later_package_update_state', '') or 'not recorded'}`",
        f"- package sources: `{len(package_manager.get('sources', []) or [])}`",
        f"- unattended-upgrades installed/enabled: `{unattended.get('installed', 'unknown')}` / `{unattended.get('enabled', 'unknown')}`",
        f"- Docker/Compose: `{runtime.get('docker_version', '')}` / `{runtime.get('docker_compose_version', '')}`",
        f"- Node/Python: `{runtime.get('node_version', '')}` / `{runtime.get('python_version', '')}`",
        "",
        "## Update Intelligence",
        "",
        f"- cadence: `{watchlist.get('check_cadence', '')}`",
        f"- last checked: `{watchlist.get('last_checked_at', '') or readiness.get('last_update_intelligence_check', '') or 'not recorded'}`",
        f"- relevant findings: `{watchlist.get('relevant_findings_count', readiness.get('relevant_findings_count', 0))}`",
        "",
        "## Watched Components",
        "",
        bullet(watchlist.get("watched_components", [])),
        "",
        "## Upgrade Proposal",
        "",
        f"- status: `{readiness.get('upgrade_proposal_status', '')}`",
        f"- current -> target: `{proposal.get('current_version', '')}` -> `{proposal.get('target_version', '')}`",
        f"- reason: {proposal.get('reason', '') or 'not proposed'}",
        f"- affected layers: `{', '.join(map(str, proposal.get('affected_layers', []) or [])) or 'none'}`",
        f"- required backups: `{', '.join(map(str, proposal.get('required_backups', []) or [])) or 'none'}`",
        f"- rollback plan: {proposal.get('restore_rollback_plan', '') or 'not proposed'}",
        f"- fallback decision: {proposal.get('fallback_decision', '') or 'not proposed'}",
        "",
        "## Next Safe Action",
        "",
        f"- {((readiness.get('next_safe_action') or {}) if isinstance(readiness.get('next_safe_action'), dict) else {}).get('action', '')}",
        "",
        "## Fallback Action",
        "",
        f"- {((readiness.get('fallback_action') or {}) if isinstance(readiness.get('fallback_action'), dict) else {}).get('action', '')}",
        "",
        "## Boundary",
        "",
        "- Report-only. Этот файл не выполняет upgrade и не является background monitoring.",
        "- Auto-upgrade/remediation без explicit approval пользователя запрещены.",
        "- Переход на новую Ubuntu LTS является отдельным migration/upgrade project.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Рендерит report-only software update readiness Markdown.")
    parser.add_argument("--root", default=".", help="Factory root или generated project root.")
    parser.add_argument("--output", default="reports/software-updates/readiness-latest.md")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    rendered = render(root)
    if args.stdout:
        print(rendered, end="")
    else:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"software_update_readiness={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
