#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path


FORBIDDEN_PARTS = {
    ".git",
    ".release-stage",
    ".smoke-test",
    ".matrix-test",
    ".pytest_cache",
    "__pycache__",
    "_artifacts",
    "_boundary-actions",
    "_factory-sync-export",
    "_sources-export",
}

REQUIRED_FILES = {
    "VERSION.md",
    "README.md",
    "POST_UNZIP_SETUP.sh",
    "RELEASE_BUILD.sh",
    "RELEASE_CHECKLIST.md",
    "RELEASE_NOTES.md",
    "FACTORY_MANIFEST.yaml",
    "template-repo/scenario-pack/00-master-router.md",
    "template-repo/scripts/verify-all.sh",
    "factory/producer/packaging/release-package-manifest.yaml",
}

MANIFEST_MARKERS = {
    "schema: factory-release-package/v1",
    "archive_root:",
    "source_commit:",
    "build_timestamp_utc:",
    "npm_path_supported: false",
    "required_first_run_commands:",
    "verification_status:",
}


def fail(message: str) -> int:
    print("RELEASE PACKAGE НЕВАЛИДЕН")
    print(f"- {message}")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет собранный factory release zip, checksum и manifest."
    )
    parser.add_argument("archive", help="Путь к factory-v<VERSION>.zip")
    parser.add_argument("--checksum", help="Путь к .sha256 файлу")
    parser.add_argument("--manifest", help="Путь к sidecar manifest YAML")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_checksum(archive: Path, checksum_path: Path) -> None:
    if not checksum_path.exists():
        raise ValueError(f"checksum file отсутствует: {checksum_path}")
    line = checksum_path.read_text(encoding="utf-8").strip().splitlines()[0]
    expected = line.split()[0]
    actual = sha256(archive)
    if expected != actual:
        raise ValueError("SHA256 checksum не совпадает с archive")
    referenced_name = line.split()[-1].lstrip("*")
    if Path(referenced_name).name != archive.name:
        raise ValueError("checksum должен ссылаться на имя archive, а не на другой файл")


def validate_manifest_text(text: str, label: str) -> None:
    missing = [marker for marker in sorted(MANIFEST_MARKERS) if marker not in text]
    if missing:
        raise ValueError(f"{label} не содержит markers: {', '.join(missing)}")


def validate_zip(archive: Path) -> tuple[str, str]:
    if not archive.exists():
        raise ValueError(f"archive отсутствует: {archive}")
    if archive.suffix != ".zip":
        raise ValueError("archive должен быть .zip")

    with zipfile.ZipFile(archive) as zf:
        names = [name for name in zf.namelist() if name and not name.endswith("/")]
        if not names:
            raise ValueError("archive пуст")
        roots = {name.split("/", 1)[0] for name in names}
        if len(roots) != 1:
            raise ValueError(f"archive должен содержать один root folder, найдено: {sorted(roots)}")
        root = next(iter(roots))
        if not root.startswith("factory-v"):
            raise ValueError(f"archive root должен начинаться с factory-v, найдено: {root}")

        for name in names:
            parts = set(Path(name).parts)
            forbidden = sorted(parts & FORBIDDEN_PARTS)
            if forbidden:
                raise ValueError(f"archive содержит forbidden path `{name}`: {', '.join(forbidden)}")
            rel_name = name.split("/", 1)[1] if "/" in name else name
            if name.endswith(".log") or rel_name.startswith("logs/"):
                raise ValueError(f"archive содержит log artifact: {name}")
            if ".env" in Path(name).name and not Path(name).name.endswith(".example"):
                raise ValueError(f"archive содержит secret-like env file: {name}")

        normalized = {name.split("/", 1)[1] for name in names if "/" in name}
        missing = sorted(REQUIRED_FILES - normalized)
        if missing:
            raise ValueError(f"archive не содержит required files: {', '.join(missing)}")

        manifest_name = f"{root}/factory/producer/packaging/release-package-manifest.yaml"
        manifest_text = zf.read(manifest_name).decode("utf-8")
        validate_manifest_text(manifest_text, "embedded manifest")
        if f'archive_root: "{root}/"' not in manifest_text and f"archive_root: {root}/" not in manifest_text:
            raise ValueError("embedded manifest archive_root не совпадает с zip root")
        return root, manifest_text


def main() -> int:
    args = parse_args()
    archive = Path(args.archive).resolve()
    try:
        root, embedded_manifest = validate_zip(archive)
        if args.checksum:
            validate_checksum(archive, Path(args.checksum).resolve())
        if args.manifest:
            manifest_path = Path(args.manifest).resolve()
            if not manifest_path.exists():
                raise ValueError(f"sidecar manifest отсутствует: {manifest_path}")
            sidecar = manifest_path.read_text(encoding="utf-8")
            validate_manifest_text(sidecar, "sidecar manifest")
            if sidecar.strip() != embedded_manifest.strip():
                raise ValueError("sidecar manifest не совпадает с embedded manifest")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        return fail(str(exc))

    print("RELEASE PACKAGE ВАЛИДЕН")
    print(f"- archive: {archive}")
    print(f"- archive_root: {root}/")
    if args.checksum:
        print(f"- checksum: {Path(args.checksum).resolve()}")
    if args.manifest:
        print(f"- manifest: {Path(args.manifest).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
