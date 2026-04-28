#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load_validator():
    path = Path(__file__).with_name("validate-orchestration-cockpit.py")
    spec = importlib.util.spec_from_file_location("validate_orchestration_cockpit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
