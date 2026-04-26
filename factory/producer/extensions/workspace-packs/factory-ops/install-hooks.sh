#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-$(pwd)}"
mkdir -p "$PROJECT_ROOT/.git/hooks"
cp "$ROOT/.githooks/pre-commit" "$PROJECT_ROOT/.git/hooks/pre-commit"
chmod +x "$PROJECT_ROOT/.git/hooks/pre-commit"
echo "Git hooks установлены в $PROJECT_ROOT/.git/hooks"
