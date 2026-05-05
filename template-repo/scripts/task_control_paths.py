#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


FACTORY_REGISTRY = "template-repo/template/.chatgpt/task-registry.yaml"
GENERATED_REGISTRY = ".chatgpt/task-registry.yaml"
FACTORY_DASHBOARD = "template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml"
GENERATED_DASHBOARD = ".chatgpt/project-lifecycle-dashboard.yaml"


def default_registry() -> str:
    if Path(FACTORY_REGISTRY).exists():
        return FACTORY_REGISTRY
    return GENERATED_REGISTRY


def default_dashboard() -> str:
    if Path(FACTORY_DASHBOARD).exists():
        return FACTORY_DASHBOARD
    return GENERATED_DASHBOARD


def script_path(name: str) -> str:
    factory_path = Path("template-repo") / "scripts" / name
    if factory_path.exists():
        return factory_path.as_posix()
    return (Path("scripts") / name).as_posix()


def python_script_command(name: str) -> str:
    return f"python3 {script_path(name)}"


def verify_all_command() -> str:
    factory_path = Path("template-repo") / "scripts" / "verify-all.sh"
    if factory_path.exists():
        return "bash template-repo/scripts/verify-all.sh quick"
    return "bash scripts/verify-all.sh quick"
