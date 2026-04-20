#!/usr/bin/env python3
from __future__ import annotations

import json

from factory_template_phase_detection import detect_phase, load_policy


def main() -> int:
    result = detect_phase(load_policy())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
