#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".toml", ".example"}

ENGLISH_HEADING_RE = re.compile(r"^(#{1,6})\s+([A-Za-z][A-Za-z0-9 /()'`.+:-]*)$")

ALLOWED_HEADING_TERMS = {
    "README",
    "ADR",
    "API",
    "CLI",
    "CI",
    "CD",
    "DoD",
    "KPI",
    "MVP",
    "RC",
    "GA",
    "VPS",
    "YAML",
    "JSON",
    "TOML",
    "GPT",
}


def load_policy(root: Path) -> dict:
    path = root / "template-repo" / "language-archive-exceptions.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def normalized_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def path_matches(rel: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        clean = pattern.strip("/")
        if not clean:
            continue
        if pattern.endswith("/") and rel.startswith(clean + "/"):
            return True
        if rel == clean or rel.startswith(clean + "/"):
            return True
    return False


def iter_candidate_files(root: Path, exclusions: list[str]) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = normalized_rel(path, root)
        if path_matches(rel, exclusions):
            continue
        if path.name in {"CODEOWNERS"}:
            continue
        if path.suffix in TEXT_SUFFIXES or path.name.endswith(".env.example"):
            result.append(path)
    return sorted(result)


def has_cyrillic(text: str) -> bool:
    return bool(re.search(r"[А-Яа-яЁё]", text))


def is_allowed_heading(text: str) -> bool:
    stripped = text.strip().strip("`")
    if not stripped:
        return True
    if any(ch.isdigit() for ch in stripped) and not re.search(r"[A-Za-z]{4,}", stripped):
        return True
    words = re.findall(r"[A-Za-z][A-Za-z0-9.+-]*", stripped)
    if not words:
        return True
    if all(word.upper() in ALLOWED_HEADING_TERMS for word in words):
        return True
    if has_cyrillic(stripped):
        return True
    return False


def scan_file(path: Path, root: Path, archive_patterns: list[str]) -> list[dict]:
    rel = normalized_rel(path, root)
    archive = path_matches(rel, archive_patterns)
    findings: list[dict] = []
    in_fence = False
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return findings
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ENGLISH_HEADING_RE.match(line)
        if not match:
            continue
        heading = match.group(2).strip()
        if is_allowed_heading(heading):
            continue
        findings.append(
            {
                "path": rel,
                "line": lineno,
                "heading": heading,
                "archival_exception": archive,
            }
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет русский человекочитаемый слой factory-template.")
    parser.add_argument("root", nargs="?", default=".", help="Путь к корню repo")
    parser.add_argument("--json", action="store_true", help="Вывести JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    policy = load_policy(root)
    archive_patterns = [item["path"] for item in policy.get("archival_exceptions", []) if isinstance(item, dict)]
    exclusions = list(policy.get("generated_or_technical_exclusions", []))

    findings: list[dict] = []
    for path in iter_candidate_files(root, exclusions):
        findings.extend(scan_file(path, root, archive_patterns))

    active = [item for item in findings if not item["archival_exception"]]
    archived = [item for item in findings if item["archival_exception"]]

    payload = {
        "status": "pass" if not active else "fail",
        "active_findings": active,
        "archival_findings_count": len(archived),
        "archival_exception_paths": archive_patterns,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Проверка человекочитаемого языкового слоя")
        print(f"- active findings: {len(active)}")
        print(f"- archival exception findings: {len(archived)}")
        if active:
            print("\nНужно исправить active source-facing headings:")
            for item in active[:100]:
                print(f"- {item['path']}:{item['line']}: {item['heading']}")
            if len(active) > 100:
                print(f"- ... еще {len(active) - 100}")

    return 1 if active else 0


if __name__ == "__main__":
    sys.exit(main())
