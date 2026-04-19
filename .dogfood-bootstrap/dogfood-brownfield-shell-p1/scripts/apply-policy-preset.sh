#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml, pathlib
task_index = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".chatgpt/task-index.yaml")
presets_file = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "policy-presets.yaml")
out_file = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else ".chatgpt/policy-status.yaml")
task = yaml.safe_load(task_index.read_text(encoding="utf-8")) or {}
presets = yaml.safe_load(presets_file.read_text(encoding="utf-8")).get("policy_presets", {})
change = task.get("change", {})
change_class = change.get("class", "")
execution_mode = change.get("execution_mode", "")
if change_class not in presets:
    raise SystemExit(f"Неизвестный класс изменения: {change_class}")
preset = presets[change_class]
handoff = preset.get("codex_handoff", {}).get(execution_mode, "forbidden")
out = {
    "policy_preset": change_class,
    "change_class": change_class,
    "execution_mode": execution_mode,
    "handoff_policy": handoff,
    "minimum_evidence_required_all": preset.get("minimum_evidence", {}).get("required_all", []),
    "minimum_evidence_required_any": preset.get("minimum_evidence", {}).get("required_any", []),
    "active_default_scenarios": preset.get("default_scenarios", []),
    "notes": preset.get("notes", []),
    "applied": True,
    "validated": False,
}
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"Политика применена: класс={change_class}, режим={execution_mode}, handoff={handoff}")
