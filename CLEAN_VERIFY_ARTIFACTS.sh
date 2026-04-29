#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGETS=(
  ".smoke-test"
  ".matrix-test"
  ".bugflow-test"
  "audit-smoke-project"
  "_sources-export"
  "_factory-sync-export"
  "_boundary-actions"
  "_artifacts"
  ".release-stage"
  ".factory-runtime"
)

for rel in "${TARGETS[@]}"; do
  rm -rf "$ROOT/$rel"
  find "$ROOT" -type d -name "$rel" -prune -exec rm -rf {} +
done

find "$ROOT" -type f -name '*.log' -delete
find "$ROOT" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$ROOT" -type d -name '.pytest_cache' -prune -exec rm -rf {} +

echo "Временные verify/release артефакты очищены."
