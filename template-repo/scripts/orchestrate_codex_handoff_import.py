#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load_orchestrator():
    path = Path(__file__).resolve().parent / "orchestrate-codex-handoff.py"
    spec = importlib.util.spec_from_file_location("orchestrate_codex_handoff", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить orchestrate-codex-handoff.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
