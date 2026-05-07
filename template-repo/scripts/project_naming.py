#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - validators handle the missing dependency path.
    yaml = None


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
PROJECT_CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}$")
RESERVED_SLUGS = {
    "new-project",
    "project",
    "test",
    "demo",
    "example",
    "factory-template",
    "template-repo",
}

RUSSIAN_STOPWORDS = {"dlya"}

TRANSLITERATION = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


@dataclass(frozen=True)
class SlugValidation:
    slug: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors


def transliterate_ru(value: str) -> str:
    result: list[str] = []
    for char in value.lower():
        result.append(TRANSLITERATION.get(char, char))
    return "".join(result)


def project_slug_from_name(project_name: str) -> str:
    """Create a deterministic lowercase Latin slug from a human project name."""
    latin = transliterate_ru(project_name)
    latin = re.sub(r"[^a-z0-9]+", "-", latin)
    parts = [part for part in latin.split("-") if part and part not in RUSSIAN_STOPWORDS]
    slug = "-".join(parts)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) > 63:
        slug = slug[:63].strip("-")
    return slug


def project_code_from_slug(slug: str) -> str:
    parts = [part for part in re.split(r"[^a-z0-9]+", slug.lower()) if part]
    if not parts:
        return "PRJ"
    code = "".join(part[0] for part in parts if part and part[0].isalnum()).upper()
    if not code or not code[0].isalpha():
        code = f"P{code}"
    return code[:12]


def validate_project_code(project_code: str, *, allow_ft: bool = False) -> tuple[str, ...]:
    if not project_code:
        return ("PROJECT_CODE is empty",)
    if not PROJECT_CODE_RE.fullmatch(project_code):
        return ("PROJECT_CODE must match ^[A-Z][A-Z0-9]{1,11}$",)
    if project_code == "FT" and not allow_ft:
        return ("PROJECT_CODE `FT` is reserved for factory-template; use it only for factory-template itself",)
    return ()


def is_reserved_slug(slug: str) -> bool:
    return slug in RESERVED_SLUGS


def validate_project_slug(slug: str, *, allow_reserved: bool = False) -> SlugValidation:
    errors: list[str] = []
    warnings: list[str] = []
    if not slug:
        errors.append("project_slug is empty; enter a meaningful lowercase Latin slug")
        return SlugValidation(slug=slug, errors=tuple(errors))
    if slug != slug.lower():
        errors.append("project_slug must be lowercase")
    if not SLUG_RE.fullmatch(slug):
        errors.append("project_slug must match ^[a-z0-9][a-z0-9-]{1,62}$")
    if slug.startswith("-") or slug.endswith("-"):
        errors.append("project_slug must not start or end with hyphen")
    if "--" in slug:
        errors.append("project_slug must not contain repeated hyphens")
    if is_reserved_slug(slug):
        message = f"project_slug `{slug}` is reserved/generic"
        if allow_reserved:
            warnings.append(f"{message}; explicit override marker required")
        else:
            errors.append(f"{message}; pass an explicit override only if this is intentional")
    return SlugValidation(slug=slug, errors=tuple(errors), warnings=tuple(warnings))


def validate_or_exit(slug: str, *, allow_reserved: bool = False) -> None:
    result = validate_project_slug(slug, allow_reserved=allow_reserved)
    if result.ok:
        return
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)


def remote_repo_name(remote_url: str) -> str:
    cleaned = remote_url.strip().rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    if ":" in cleaned and "/" in cleaned and not cleaned.startswith(("http://", "https://")):
        cleaned = cleaned.rsplit(":", 1)[-1]
    return cleaned.rsplit("/", 1)[-1]


def git_origin_url(root: Path) -> str | None:
    top = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root.resolve():
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None or not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _stage_slug(root: Path) -> str:
    stage = _load_yaml(root / ".chatgpt" / "stage-state.yaml")
    project = stage.get("project", {}) if isinstance(stage.get("project"), dict) else {}
    return str(project.get("slug") or "").strip()


def _origin_text(root: Path) -> str:
    path = root / ".chatgpt" / "project-origin.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _origin_slug(root: Path) -> str:
    text = _origin_text(root)
    match = re.search(r"##\s+(?:Slug|project_slug|Slug / slug проекта)\s*\n([^\n]+)", text, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip()


def _reserved_override_marker(root: Path) -> bool:
    text = _origin_text(root)
    if re.search(r"reserved[_ -]slug[_ -]override\s*:\s*true", text, re.IGNORECASE):
        return True
    if re.search(r"##\s+Reserved slug override\s*\n\s*true\b", text, re.IGNORECASE):
        return True
    return False


def _looks_like_project_root(root: Path) -> bool:
    if (root / "FACTORY_MANIFEST.yaml").exists() and (root / "template-repo").is_dir():
        return False
    return (root / ".chatgpt").is_dir() and (root / ".chatgpt" / "stage-state.yaml").exists()


def _is_projects_root(path: Path) -> bool:
    return path.as_posix().rstrip("/") == "/projects" or path.name == "projects"


def validate_root_naming(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    if not _looks_like_project_root(root):
        return errors

    stage_slug = _stage_slug(root)
    origin_slug = _origin_slug(root)
    project_slug = stage_slug or origin_slug
    if not project_slug:
        errors.append("project_slug missing from .chatgpt/stage-state.yaml and .chatgpt/project-origin.md")
        return errors

    if stage_slug and origin_slug and stage_slug != origin_slug:
        errors.append(f"project_slug mismatch: stage-state has `{stage_slug}`, project-origin has `{origin_slug}`")

    override = _reserved_override_marker(root)
    validation = validate_project_slug(project_slug, allow_reserved=override)
    errors.extend(validation.errors)
    if is_reserved_slug(project_slug) and not override:
        errors.append("reserved/generic project_slug requires explicit override marker in project-origin")

    if root.name != project_slug:
        errors.append(f"project path basename `{root.name}` must equal project_slug `{project_slug}`")

    origin = git_origin_url(root)
    if origin:
        repo_name = remote_repo_name(origin)
        if repo_name != project_slug:
            errors.append(f"git origin repo name `{repo_name}` must equal project_slug `{project_slug}`")

    parent = root.parent
    if _is_projects_root(parent):
        forbidden_terms = ("brownfield", "incoming", "reconstructed", "helper", "temporary", "transition")
        for sibling in parent.iterdir():
            if sibling == root or not sibling.is_dir():
                continue
            if not (sibling / ".git").exists():
                continue
            if any(term in sibling.name for term in forbidden_terms):
                errors.append(
                    "intermediate brownfield/helper repo must live inside "
                    f"`{root}` instead of sibling project root `{sibling}`"
                )
    return errors


def run_self_test() -> None:
    expected = {
        "Краб — CRM для ремонта": "krab-crm-remonta",
        "AI Factory": "ai-factory",
        "Мой первый проект!!!": "moy-pervyy-proekt",
        "CRM + склад 2.0": "crm-sklad-2-0",
    }
    for name, slug in expected.items():
        actual = project_slug_from_name(name)
        if actual != slug:
            raise AssertionError(f"{name!r}: expected {slug!r}, got {actual!r}")
        validate_or_exit(actual)
    if project_slug_from_name("!!!"):
        raise AssertionError("punctuation-only name must produce an empty slug")
    if validate_project_slug("new-project").ok:
        raise AssertionError("reserved slug must be blocked without override")
    if not validate_project_slug("new-project", allow_reserved=True).ok:
        raise AssertionError("reserved slug must be allowed with explicit override")
    if project_code_from_slug("novice-git-identity-smoke") != "NGIS":
        raise AssertionError("project code generation changed unexpectedly")
    if not validate_project_code("ft"):
        raise AssertionError("lowercase project code must fail")


def main() -> int:
    parser = argparse.ArgumentParser(description="Canonical project naming helpers.")
    sub = parser.add_subparsers(dest="command", required=True)
    slug_parser = sub.add_parser("slug", help="Generate project_slug from human project_name.")
    slug_parser.add_argument("project_name")
    code_parser = sub.add_parser("code-from-slug", help="Generate default PROJECT_CODE from project_slug.")
    code_parser.add_argument("project_slug")
    validate_code_parser = sub.add_parser("validate-code", help="Validate PROJECT_CODE.")
    validate_code_parser.add_argument("project_code")
    validate_code_parser.add_argument("--allow-ft", action="store_true", help="Allow reserved FT for factory-template.")
    validate_parser = sub.add_parser("validate", help="Validate a project_slug.")
    validate_parser.add_argument("project_slug")
    validate_parser.add_argument("--allow-reserved", action="store_true")
    reserved_parser = sub.add_parser("is-reserved", help="Exit 0 when slug is reserved/generic.")
    reserved_parser.add_argument("project_slug")
    root_parser = sub.add_parser("validate-root", help="Validate generated project naming invariants.")
    root_parser.add_argument("root", nargs="?", default=".")
    sub.add_parser("self-test", help="Run built-in slug generation smoke tests.")
    args = parser.parse_args()

    if args.command == "slug":
        print(project_slug_from_name(args.project_name))
        return 0
    if args.command == "code-from-slug":
        print(project_code_from_slug(args.project_slug))
        return 0
    if args.command == "validate-code":
        errors = validate_project_code(args.project_code, allow_ft=args.allow_ft)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        return 0
    if args.command == "validate":
        result = validate_project_slug(args.project_slug, allow_reserved=args.allow_reserved)
        for warning in result.warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        if not result.ok:
            for error in result.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        return 0
    if args.command == "is-reserved":
        return 0 if is_reserved_slug(args.project_slug) else 1
    if args.command == "validate-root":
        root = Path(args.root).expanduser().resolve()
        if not root.exists():
            print(f"PROJECT NAMING НЕ ПРОЙДЕН\n- root does not exist: {root}")
            return 1
        errors = validate_root_naming(root)
        if errors:
            print("PROJECT NAMING НЕ ПРОЙДЕН")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"PROJECT NAMING ПРОЙДЕН: {root}")
        return 0
    if args.command == "self-test":
        run_self_test()
        print("PROJECT NAMING SELF-TEST ПРОЙДЕН")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
