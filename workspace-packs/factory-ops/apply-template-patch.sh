#!/usr/bin/env bash
set -euo pipefail
PATCH_BUNDLE="${1:-}"
MODE="${2:---check}"
if [ -z "$PATCH_BUNDLE" ]; then
  echo "Использование: apply-template-patch.sh <каталог-patch-bundle> [--check|--dry-run|--apply-safe-zones]"
  exit 1
fi
if [ ! -d "$PATCH_BUNDLE" ]; then
  echo "ОШИБКА: каталог patch bundle не найден"
  exit 1
fi
case "$MODE" in
  --check)
    echo "Найден patch bundle: $PATCH_BUNDLE"
    find "$PATCH_BUNDLE" -maxdepth 1 -type f | sort
    ;;
  --dry-run)
    echo "Dry-run: проверка patch bundle завершена, применение не выполнялось."
    ;;
  --apply-safe-zones)
    APPLY_DIR="$PATCH_BUNDLE/applied-safe-zones"
    PROJECT_ROOT="$(cd "$PATCH_BUNDLE/.." && pwd)"
    mkdir -p "$APPLY_DIR"
    for f in changed-files.txt patch-summary.md template-sync.patch; do [ -f "$PATCH_BUNDLE/$f" ] && cp "$PATCH_BUNDLE/$f" "$APPLY_DIR/$f"; done
    if [ -d "$PATCH_BUNDLE/generated-files" ]; then
      while IFS= read -r -d '' file; do
        rel="${file#"$PATCH_BUNDLE/generated-files/"}"
        mkdir -p "$PROJECT_ROOT/$(dirname "$rel")"
        cp "$file" "$PROJECT_ROOT/$rel"
      done < <(find "$PATCH_BUNDLE/generated-files" -type f -print0)
    fi
    echo "Safe-зоны отмечены как применимые. Фактическое применение выполняется только после ручного подтверждения в template-repo."
    echo "Materialized files, включая root AGENTS.md, синхронизированы в repo root через canonical sync path."
    echo "Каталог результата: $APPLY_DIR"
    ;;
  *)
    echo "ОШИБКА: поддерживаются только режимы --check, --dry-run и --apply-safe-zones"
    exit 1
    ;;
esac
