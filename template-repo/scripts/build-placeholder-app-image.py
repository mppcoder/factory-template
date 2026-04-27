#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def parse_env(path: Path) -> tuple[list[str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    values: dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return lines, values


def write_env(path: Path, lines: list[str], updates: dict[str, str]) -> None:
    seen: set[str] = set()
    output: list[str] = []
    for line in lines:
        if "=" in line and not line.lstrip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in updates:
                output.append(f"{key}={updates[key]}")
                seen.add(key)
                continue
        output.append(line)
    if output and output[-1] != "":
        output.append("")
    for key, value in updates.items():
        if key not in seen:
            output.append(f"{key}={value}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    path.chmod(0o600)


def prepare_build_context(source_dir: Path, image_url: str, build_dir: Path, base_image: str) -> None:
    site_dir = build_dir / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, site_dir / item.name)
    index = site_dir / "index.html"
    html = index.read_text(encoding="utf-8")
    html = html.replace('src="/placeholder.svg"', f'src="{image_url}"')
    index.write_text(html, encoding="utf-8")
    (build_dir / "Dockerfile").write_text(
        "\n".join(
            [
                f"FROM {base_image}",
                "COPY site/ /usr/share/nginx/html/",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run(command: list[str], dry_run: bool) -> int:
    print("command=" + " ".join(command))
    if dry_run:
        return 0
    proc = subprocess.run(command, check=False, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a local placeholder application Docker image from repo-native static assets.",
    )
    parser.add_argument("--env-file", default="deploy/.env")
    parser.add_argument("--static-dir", default="deploy/static-placeholder")
    parser.add_argument("--image-tag", default="factory-template-placeholder-app:local")
    parser.add_argument("--base-image", default="nginx:1.27-alpine")
    parser.add_argument("--image-url", default="/placeholder.svg")
    parser.add_argument("--allow-pull", action="store_true", help="Allow Docker to pull the base image while building.")
    parser.add_argument("--no-env-update", action="store_true")
    parser.add_argument("--install-volume", action="store_true", help="Also copy placeholder files into APP_DATA_VOLUME for an already-created named volume.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env_path = Path(args.env_file)
    source_dir = Path(args.static_dir).resolve()
    if not source_dir.exists():
        raise SystemExit(f"static dir not found: {source_dir}")

    print("placeholder_app_image_build=true")
    print(f"image_tag={args.image_tag}")
    print(f"base_image={args.base_image}")
    print(f"image_url={args.image_url}")

    with tempfile.TemporaryDirectory(prefix="factory-placeholder-image-") as tmp:
        build_dir = Path(tmp)
        prepare_build_context(source_dir, args.image_url, build_dir, args.base_image)
        build_cmd = ["docker", "build", "--pull=" + ("true" if args.allow_pull else "false"), "-t", args.image_tag, str(build_dir)]
        rc = run(build_cmd, args.dry_run)
        if rc != 0:
            return rc

    if not args.no_env_update:
        lines, _ = parse_env(env_path)
        updates = {
            "APP_IMAGE": args.image_tag,
            "APP_PULL_POLICY": "never",
            "APP_PLACEHOLDER_MODE": "static",
            "APP_PLACEHOLDER_IMAGE_URL": args.image_url,
        }
        if not args.dry_run:
            write_env(env_path, lines, updates)
        print(f"env_file={env_path}")
        print("env_updated=APP_IMAGE,APP_PULL_POLICY,APP_PLACEHOLDER_MODE,APP_PLACEHOLDER_IMAGE_URL")

    if args.install_volume:
        install_cmd = [
            "python3",
            "template-repo/scripts/install-static-placeholder.py",
            "--env-file",
            str(env_path),
            "--static-dir",
            str(source_dir),
            "--image-url",
            args.image_url,
            "--runtime-image",
            args.image_tag,
        ]
        rc = run(install_cmd, args.dry_run)
        if rc != 0:
            return rc

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
