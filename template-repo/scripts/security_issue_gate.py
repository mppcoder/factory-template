#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from permission_model import decide


def load(path: str | None) -> dict | None:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Private-only security issue autofix gate.")
    parser.add_argument("--channel", choices=["public-issue", "private"], default="public-issue")
    parser.add_argument("--labels", default="")
    parser.add_argument("--approval-file")
    parser.add_argument("--actor", default="local")
    parser.add_argument("--actor-permission", default="maintain")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    labels = {x.strip() for x in args.labels.split(",") if x.strip()}
    reasons: list[str] = []
    if args.channel != "private" or "security" in labels:
        reasons.append("public security issue autofix refused; use private report channel")
    approval = load(args.approval_file)
    decision = decide("security-fix", args.actor, args.actor_permission, "security/private", approval)
    if args.channel == "private" and not decision["allowed"]:
        reasons.append(decision["reason"])
    allowed = args.channel == "private" and not reasons
    print(json.dumps({"allowed": allowed, "reasons": reasons, "sanitized_private_handoff": allowed}, ensure_ascii=False, sort_keys=True))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
