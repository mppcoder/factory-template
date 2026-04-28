#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_naming import validate_root_naming


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical project naming invariants.")
    parser.add_argument("root", nargs="?", default=".", help="Generated project root or factory root.")
    args = parser.parse_args()

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


if __name__ == "__main__":
    sys.exit(main())
