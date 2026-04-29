#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILS=0

die(){ echo "$1"; FAILS=$((FAILS+1)); }

ROOT_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия$/{f=1}' "$ROOT/VERSION.md")"
ROOT_NAME="factory-v${ROOT_VERSION}"
MANIFEST_VERSION="$(awk -F': ' '/^version:/{print $2; exit}' "$ROOT/FACTORY_MANIFEST.yaml")"
MANIFEST_NAME="$(awk -F': ' '/^name:/{print $2; exit}' "$ROOT/FACTORY_MANIFEST.yaml")"
TEMPLATE_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия шаблона$/{f=1}' "$ROOT/template-repo/VERSION.md")"
TEMPLATE_FACTORY_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Версия фабрики-источника$/{f=1}' "$ROOT/template-repo/VERSION.md")"
TEMPLATE_MANIFEST_FACTORY_VERSION="$(awk -F': ' '/^factory_version:/{print $2; exit}' "$ROOT/template-repo/TEMPLATE_MANIFEST.yaml")"
META_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия$/{f=1}' "$ROOT/project-knowledge/factory/template-evolution/VERSION.md")"
META_FACTORY_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Связанная версия фабрики$/{f=1}' "$ROOT/project-knowledge/factory/template-evolution/VERSION.md")"

[ -n "$ROOT_VERSION" ] || die 'ОШИБКА: не удалось определить root version из VERSION.md'
[ "$MANIFEST_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: FACTORY_MANIFEST.yaml version=$MANIFEST_VERSION, ожидалось $ROOT_VERSION"
[ "$MANIFEST_NAME" = "$ROOT_NAME" ] || die "ОШИБКА: FACTORY_MANIFEST.yaml name=$MANIFEST_NAME, ожидалось $ROOT_NAME"
[ "$TEMPLATE_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: template-repo/VERSION.md=$TEMPLATE_VERSION, ожидалось $ROOT_VERSION"
[ "$TEMPLATE_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: template-repo/VERSION.md factory=$TEMPLATE_FACTORY_VERSION, ожидалось $ROOT_VERSION"
[ "$TEMPLATE_MANIFEST_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: TEMPLATE_MANIFEST.yaml factory_version=$TEMPLATE_MANIFEST_FACTORY_VERSION, ожидалось $ROOT_VERSION"
[ "$META_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: project-knowledge/factory/template-evolution/VERSION.md=$META_VERSION, ожидалось $ROOT_VERSION"
[ "$META_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: project-knowledge/factory/template-evolution/VERSION.md factory=$META_FACTORY_VERSION, ожидалось $ROOT_VERSION"

grep -q "## ${ROOT_VERSION}" "$ROOT/docs/releases/factory-template-release-notes.md" || die "ОШИБКА: docs/releases/factory-template-release-notes.md не содержит секцию ${ROOT_VERSION}"

LEGACY_REF_PATTERN='factory-v2\.3\.9-alignment-layer|2\.4\.0-versioning-layer|factory-2\.4\.0-versioning-layer'
LEGACY_REF_MATCHES="$(
  cd "$ROOT"
  find . \
    -path './.git' -prune -o \
    -path './.release-stage' -prune -o \
    -type f -print0 |
    while IFS= read -r -d '' file; do
      rel="${file#./}"
      case "$rel" in
        factory/producer/registry/release-history.md|\
        factory/producer/registry/factory-versions.md|\
        factory/producer/registry/projects-created.md|\
        CHANGELOG.md|\
        VERSION.md|\
        docs/releases/factory-template-release-notes.md)
          continue
          ;;
      esac
      matches="$(grep -nE "$LEGACY_REF_PATTERN" "$file" || true)"
      if [ -n "$matches" ]; then
        printf '%s\n' "$matches" | sed "s#^#${rel}:#"
      fi
    done
)"

if [ -n "$LEGACY_REF_MATCHES" ]; then
  echo 'ОШИБКА: найдены неожиданные legacy/versioning-layer ссылки вне разрешенной истории:'
  printf '%s\n' "$LEGACY_REF_MATCHES"
  FAILS=$((FAILS+1))
fi

if [ "$FAILS" -gt 0 ]; then
  echo 'VERSION SYNC CHECK НЕ ПРОЙДЕН'
  exit 1
fi

echo "VERSION SYNC CHECK ПРОЙДЕН (${ROOT_VERSION})"
