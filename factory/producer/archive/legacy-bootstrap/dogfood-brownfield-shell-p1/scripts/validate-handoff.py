#!/usr/bin/env python3
from __future__ import annotations
import sys, pathlib, yaml
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
stage = yaml.safe_load((root/".chatgpt/stage-state.yaml").read_text(encoding="utf-8")) or {}
policy = yaml.safe_load((root/".chatgpt/policy-status.yaml").read_text(encoding="utf-8")) or {}
handoff = policy.get("handoff_policy", "forbidden")
allowed = (stage.get("gates", {}) or {}).get("codex_handoff_allowed", False)
if handoff == "forbidden":
    print("HANDOFF НЕ ТРЕБУЕТСЯ ДЛЯ ТЕКУЩЕГО ПРОФИЛЯ")
    raise SystemExit(0)
if handoff == "optional" and not allowed and not (root/".chatgpt/codex-input.md").exists():
    print("HANDOFF ПОКА НЕ ОБЯЗАТЕЛЕН ДЛЯ ТЕКУЩЕГО ПРОФИЛЯ")
    raise SystemExit(0)
errs = []
if handoff == "required" and not allowed:
    errs.append("Handoff обязателен, но gate codex_handoff_allowed закрыт")
if not (root/".chatgpt/codex-input.md").exists():
    errs.append("Не найден файл codex-input.md")
if not (root/".chatgpt/evidence-register.md").exists():
    errs.append("Не найден файл evidence-register.md")
if not policy.get("validated", False):
    errs.append("Политика не прошла валидацию")
if errs:
    print("HANDOFF НЕКОРРЕКТЕН")
    for err in errs:
        print("-", err)
    raise SystemExit(1)
print("HANDOFF КОРРЕКТЕН")
