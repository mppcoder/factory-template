#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


REQUIRED_SOURCE_URLS = [
    "https://developers.openai.com/api/docs/guides/latest-model",
    "https://developers.openai.com/api/docs/guides/prompt-guidance",
    "https://developers.openai.com/api/docs/guides/prompt-optimizer",
]

REQUIRED_REVIEW_MARKERS = [
    "drop-in replacement",
    "fresh prompt baseline",
    "success criteria",
    "evidence requirements",
    "output shape",
    "stop rules",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет связку model promotion и prompt policy.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    routing = read_yaml(root / "template-repo" / "codex-model-routing.yaml")
    if not routing:
        routing = read_yaml(root / "codex-model-routing.yaml")
    policy = routing.get("prompt_migration_policy", {}) if isinstance(routing, dict) else {}
    if not isinstance(policy, dict) or not policy:
        errors.append("codex-model-routing.yaml: отсутствует prompt_migration_policy")
    else:
        if policy.get("default_action") != "proposal-required":
            errors.append("prompt_migration_policy.default_action должен быть proposal-required")
        sources = "\n".join(str(item) for item in policy.get("official_source_baseline", []))
        for url in REQUIRED_SOURCE_URLS:
            if url not in sources:
                errors.append(f"prompt_migration_policy.official_source_baseline: missing `{url}`")
        review = "\n".join(str(item) for item in policy.get("required_prompt_review", []))
        for marker in REQUIRED_REVIEW_MARKERS:
            if marker not in review:
                errors.append(f"prompt_migration_policy.required_prompt_review: missing `{marker}`")
        artifacts = "\n".join(str(item) for item in policy.get("required_artifacts", []))
        for marker in ["reports/prompt-migration/", "tests/artifact-eval/specs/*prompt-contract*.yaml"]:
            if marker not in artifacts:
                errors.append(f"prompt_migration_policy.required_artifacts: missing `{marker}`")

    checker = read_text(root / "template-repo" / "scripts" / "check-codex-model-catalog.py")
    for marker in [
        "Политика prompt migration",
        "prompt_review_required",
        "Official OpenAI source baseline",
        "Required prompt review",
        "drop-in replacement",
    ]:
        if marker not in checker:
            errors.append(f"check-codex-model-catalog.py: missing `{marker}`")

    proposal = read_text(root / "reports" / "model-routing" / "model-routing-proposal.md")
    if proposal:
        for marker in [
            "## Политика prompt migration",
            "prompt_review_required:",
            "Official OpenAI source baseline:",
            "Required prompt artifacts:",
        ]:
            if marker not in proposal:
                errors.append(f"reports/model-routing/model-routing-proposal.md: missing `{marker}`")

    docs = "\n".join(
        [
            read_text(root / "template-repo" / "README.md"),
            read_text(root / "template-repo" / "template" / "docs" / "codex-workflow.md"),
            read_text(root / "template-repo" / "template" / "docs" / "integrations.md"),
        ]
    )
    for marker in ["prompt_migration_policy", "reports/prompt-migration/", "official OpenAI"]:
        if marker not in docs:
            errors.append(f"docs: missing `{marker}`")

    if errors:
        print("MODEL PROMPT POLICY НЕ ПРОЙДЕНА")
        for error in errors:
            print(f"- {error}")
        return 1

    print("MODEL PROMPT POLICY ВАЛИДНА")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
