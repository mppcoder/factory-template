#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml, pathlib
preset_name = sys.argv[1] if len(sys.argv) > 1 else "product-dev"
presets_file = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "project-presets.yaml")
out_file = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else ".chatgpt/project-profile.yaml")
active_file = pathlib.Path(sys.argv[4] if len(sys.argv) > 4 else ".chatgpt/active-scenarios.yaml")
presets = yaml.safe_load(presets_file.read_text(encoding="utf-8")).get("project_presets", {})
if preset_name not in presets:
    raise SystemExit(f"Неизвестный профиль проекта: {preset_name}")
preset = presets[preset_name]
out = {
    "project_preset": preset_name,
    "project_title": preset.get("title", ""),
    "recommended_mode": preset.get("default_mode", ""),
    "recommended_change_class": preset.get("recommended_change_class", ""),
    "recommended_execution_mode": preset.get("recommended_execution_mode", ""),
    "active_default_scenarios": preset.get("default_scenarios", []),
    "required_artifacts": preset.get("required_artifacts", []),
    "notes": preset.get("notes", []),
    "applied": True,
    "validated": False,
}
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
active = yaml.safe_load(active_file.read_text(encoding="utf-8")) or {}
active["project_preset"] = preset_name
active["active"] = preset.get("default_scenarios", [])
active_file.write_text(yaml.safe_dump(active, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"Профиль проекта применен: {preset_name}")
