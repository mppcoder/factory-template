#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = ROOT / "tools" / "sync_factory_template_sources_to_gdrive_api.py"


def sha256_hex(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def md5_hex(data: bytes) -> str:
    import hashlib

    return hashlib.md5(data).hexdigest()


def make_export_pack(root: Path) -> Path:
    export_dir = root / "core-hot-15"
    upload_dir = export_dir / "upload-to-sources"
    upload_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "alpha.md": b"alpha-new\n",
        "beta.md": b"beta-updated\n",
        "same.md": b"same-content\n",
    }
    for name, content in files.items():
        (upload_dir / name).write_bytes(content)
    (export_dir / "manifest.json").write_text(
        json.dumps(
            {
                "kind": "direct_sources",
                "export_name": "core-hot-15",
                "upload_subdir": "upload-to-sources",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return export_dir


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="factory-gdrive-sync-plan-") as tmp:
        temp_root = Path(tmp)
        export_dir = make_export_pack(temp_root)
        remote_snapshot = temp_root / "remote.json"
        remote_snapshot.write_text(
            json.dumps(
                {
                    "files": [
                        {"name": "beta.md", "md5Checksum": md5_hex(b"beta-old\n"), "size": 9},
                        {"name": "same.md", "md5Checksum": md5_hex(b"same-content\n"), "size": len(b"same-content\n")},
                        {"name": "stale.md", "md5Checksum": md5_hex(b"stale\n"), "size": 6},
                    ]
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        config_dir = temp_root / ".chatgpt"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "google-drive-sources.yaml").write_text(
            "\n".join(
                [
                    "google_drive_sources:",
                    "  folder_url: https://drive.google.com/drive/folders/example-folder-id",
                    "  delete_stale: true",
                    "  dry_run: true",
                    "  supports_all_drives: false",
                    f"  report_dir: {temp_root / 'reports'}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        env_file = temp_root / ".env"
        env_file.write_text(
            "\n".join(
                [
                    f"FACTORY_TEMPLATE_SYNC_REPORT_DIR={temp_root / 'reports'}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                "python3",
                str(SYNC_SCRIPT),
                str(export_dir),
                "--config",
                str(config_dir / "google-drive-sources.yaml"),
                "--env-file",
                str(env_file),
                "--remote-snapshot",
                str(remote_snapshot),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        report = json.loads(result.stdout)
        assert report["sync_mode"] == "codex_google_drive_connector_boundary"
        assert report["repo_can_execute_sync"] is False
        assert report["compare_status"] == "planned_from_remote_snapshot"
        assert report["create_count"] == 1
        assert report["update_count"] == 1
        assert report["delete_count"] == 1
        assert report["skip_count"] == 1
        assert any(item["action"] == "create" and item["name"] == "alpha.md" for item in report["detailed_actions"])
        assert any(item["action"] == "update" and item["name"] == "beta.md" for item in report["detailed_actions"])
        assert any(item["action"] == "delete" and item["name"] == "stale.md" for item in report["detailed_actions"])
        assert any(item["action"] == "skip" and item["name"] == "same.md" for item in report["detailed_actions"])

        pending = subprocess.run(
            [
                "python3",
                str(SYNC_SCRIPT),
                str(export_dir),
                "--config",
                str(config_dir / "google-drive-sources.yaml"),
                "--env-file",
                str(env_file),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        pending_report = json.loads(pending.stdout)
        assert pending_report["compare_status"] == "awaiting_codex_connector_remote_snapshot"
        assert pending_report["detailed_actions"] == [{"action": "pending", "reason": "remote_snapshot_required_for_compare"}]

    print("Google Drive connector sync plan verify passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
