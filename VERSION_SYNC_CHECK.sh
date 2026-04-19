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
META_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Текущая версия$/{f=1}' "$ROOT/meta-template-project/VERSION.md")"
META_FACTORY_VERSION="$(awk 'f{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit} /^## Связанная версия фабрики$/{f=1}' "$ROOT/meta-template-project/VERSION.md")"

[ -n "$ROOT_VERSION" ] || die 'ОШИБКА: не удалось определить root version из VERSION.md'
[ "$MANIFEST_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: FACTORY_MANIFEST.yaml version=$MANIFEST_VERSION, ожидалось $ROOT_VERSION"
[ "$MANIFEST_NAME" = "$ROOT_NAME" ] || die "ОШИБКА: FACTORY_MANIFEST.yaml name=$MANIFEST_NAME, ожидалось $ROOT_NAME"
[ "$TEMPLATE_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: template-repo/VERSION.md=$TEMPLATE_VERSION, ожидалось $ROOT_VERSION"
[ "$TEMPLATE_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: template-repo/VERSION.md factory=$TEMPLATE_FACTORY_VERSION, ожидалось $ROOT_VERSION"
[ "$TEMPLATE_MANIFEST_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: TEMPLATE_MANIFEST.yaml factory_version=$TEMPLATE_MANIFEST_FACTORY_VERSION, ожидалось $ROOT_VERSION"
[ "$META_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: meta-template-project/VERSION.md=$META_VERSION, ожидалось $ROOT_VERSION"
[ "$META_FACTORY_VERSION" = "$ROOT_VERSION" ] || die "ОШИБКА: meta-template-project/VERSION.md factory=$META_FACTORY_VERSION, ожидалось $ROOT_VERSION"

grep -q "## ${ROOT_VERSION}" "$ROOT/meta-template-project/RELEASE_NOTES.md" || die "ОШИБКА: meta-template-project/RELEASE_NOTES.md не содержит секцию ${ROOT_VERSION}"

if rg -n 'factory-v2\.3\.9-alignment-layer|2\.4\.0-versioning-layer|factory-2\.4\.0-versioning-layer' \
  "$ROOT" \
  -g '!registry/release-history.md' \
  -g '!registry/factory-versions.md' \
  -g '!registry/projects-created.md' \
  -g '!CHANGELOG.md' \
  -g '!VERSION.md' \
  -g '!meta-template-project/RELEASE_NOTES.md' >/dev/null; then
  echo 'ОШИБКА: найдены неожиданные legacy/versioning-layer ссылки вне разрешенной истории:'
  rg -n 'factory-v2\.3\.9-alignment-layer|2\.4\.0-versioning-layer|factory-2\.4\.0-versioning-layer' \
    "$ROOT" \
    -g '!registry/release-history.md' \
    -g '!registry/factory-versions.md' \
    -g '!registry/projects-created.md' \
    -g '!CHANGELOG.md' \
    -g '!VERSION.md' \
    -g '!meta-template-project/RELEASE_NOTES.md' || true
  FAILS=$((FAILS+1))
fi

if [ "$FAILS" -gt 0 ]; then
  echo 'VERSION SYNC CHECK НЕ ПРОЙДЕН'
  exit 1
fi

echo "VERSION SYNC CHECK ПРОЙДЕН (${ROOT_VERSION})"
