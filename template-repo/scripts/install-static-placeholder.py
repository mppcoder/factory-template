#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def prepare_static_dir(source_dir: Path, image_url: str, staging_dir: Path) -> None:
    staging_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        target = staging_dir / item.name
        if item.is_file():
            shutil.copy2(item, target)
    index = staging_dir / "index.html"
    html = index.read_text(encoding="utf-8")
    html = html.replace('src="/placeholder.svg"', f'src="{image_url}"')
    index.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the generated static placeholder page into the app Docker volume.",
    )
    parser.add_argument("--env-file", default="deploy/.env")
    parser.add_argument("--static-dir", default="deploy/static-placeholder")
    parser.add_argument("--image-url", default="/placeholder.svg")
    parser.add_argument("--runtime-image", default=None, help="Local image used to copy files into the Docker volume.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = parse_env(Path(args.env_file))
    app_volume = env.get("APP_DATA_VOLUME", "factory-template-app-data")
    runtime_image = args.runtime_image or env.get("APP_IMAGE", "nginx:1.27-alpine")
    source_dir = Path(args.static_dir).resolve()
    if not source_dir.exists():
        raise SystemExit(f"static dir not found: {source_dir}")

    print("static_placeholder_install=true")
    print(f"app_volume={app_volume}")
    print(f"image_url={args.image_url}")
    print(f"runtime_image={runtime_image}")
    if args.dry_run:
        return 0

    with tempfile.TemporaryDirectory(prefix="factory-placeholder-") as tmp:
        staging = Path(tmp) / "site"
        prepare_static_dir(source_dir, args.image_url, staging)
        cmd = [
            "docker",
            "run",
            "--rm",
            "--pull=never",
            "-v",
            f"{app_volume}:/site",
            "-v",
            f"{staging}:/placeholder:ro",
            runtime_image,
            "sh",
            "-c",
            "set -eu; cp -R /placeholder/. /site/; find /site -maxdepth 1 -type f -print",
        ]
        proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
        if proc.stdout:
            for line in proc.stdout.splitlines():
                print(f"installed={line}")
        if proc.returncode != 0:
            if proc.stderr:
                print(proc.stderr.strip())
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
