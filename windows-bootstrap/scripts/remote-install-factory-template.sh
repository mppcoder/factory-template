#!/usr/bin/env bash
set -euo pipefail

MODE=""
REPO_URL="https://github.com/mppcoder/factory-template.git"
TARGET_ROOT="/projects/factory-template"
INCOMING="/projects/factory-template/_incoming"
ARCHIVE_NAME="factory-v2.5.1.zip"
MANIFEST_NAME="factory-v2.5.1.manifest.yaml"
CHECKSUM_NAME="factory-v2.5.1.zip.sha256"
YES_INSTALL_PACKAGES=0

log() { printf '[INFO] %s\n' "$*"; }
pass() { printf 'PASS: %s\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<USAGE
Usage:
  bash remote-install-factory-template.sh --mode clone
  bash remote-install-factory-template.sh --mode archive --archive factory-v2.5.1.zip --manifest factory-v2.5.1.manifest.yaml --checksum factory-v2.5.1.zip.sha256

Options:
  --repo-url URL
  --target-root PATH
  --incoming PATH
  --yes-install-packages
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --repo-url) REPO_URL="${2:-}"; shift 2 ;;
    --target-root) TARGET_ROOT="${2:-}"; shift 2 ;;
    --incoming) INCOMING="${2:-}"; shift 2 ;;
    --archive) ARCHIVE_NAME="${2:-}"; shift 2 ;;
    --manifest) MANIFEST_NAME="${2:-}"; shift 2 ;;
    --checksum) CHECKSUM_NAME="${2:-}"; shift 2 ;;
    --yes-install-packages) YES_INSTALL_PACKAGES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

[[ "$MODE" == "clone" || "$MODE" == "archive" ]] || fail "--mode must be clone or archive"
[[ "$TARGET_ROOT" == "/projects/factory-template" ]] || log "Non-default target root requested: $TARGET_ROOT"
[[ "$INCOMING" == "/projects/factory-template/_incoming" ]] || log "Non-default incoming dir requested: $INCOMING"

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_packages_if_allowed() {
  local missing=("$@")
  [[ "${#missing[@]}" -gt 0 ]] || return 0
  printf 'Missing Linux packages/tools: %s\n' "${missing[*]}" >&2
  local installer=""
  if need_cmd apt-get; then
    installer="apt-get"
  else
    fail "No supported package manager found. Please install missing tools manually: ${missing[*]}"
  fi

  local sudo_prefix=()
  if [[ "$(id -u)" -ne 0 ]]; then
    if need_cmd sudo; then
      sudo_prefix=(sudo)
    else
      fail "Need root or sudo to install missing tools: ${missing[*]}"
    fi
  fi

  if [[ "$YES_INSTALL_PACKAGES" -ne 1 ]]; then
    printf 'Install missing packages with %s now? [y/N] ' "$installer" >&2
    read -r answer
    case "$answer" in
      y|Y|yes|YES) ;;
      *) fail "User did not approve package installation." ;;
    esac
  fi

  "${sudo_prefix[@]}" apt-get update
  "${sudo_prefix[@]}" apt-get install -y "${missing[@]}"
}

ensure_tools() {
  local missing_packages=()
  if ! need_cmd git && [[ "$MODE" == "clone" ]]; then missing_packages+=("git"); fi
  if ! need_cmd unzip && [[ "$MODE" == "archive" ]]; then missing_packages+=("unzip"); fi
  if ! need_cmd python3; then missing_packages+=("python3"); fi
  if ! need_cmd sha256sum && [[ "$MODE" == "archive" ]]; then missing_packages+=("coreutils"); fi
  install_packages_if_allowed "${missing_packages[@]}"

  need_cmd python3 || fail "python3 is unavailable after package check"
  if [[ "$MODE" == "clone" ]]; then need_cmd git || fail "git is unavailable after package check"; fi
  if [[ "$MODE" == "archive" ]]; then
    need_cmd unzip || fail "unzip is unavailable after package check"
    need_cmd sha256sum || fail "sha256sum is unavailable after package check"
  fi
  pass "tool check"
}

is_empty_or_incoming_only() {
  local root="$1"
  [[ -d "$root" ]] || return 0
  local entries=()
  while IFS= read -r item; do entries+=("$item"); done < <(find "$root" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort)
  if [[ "${#entries[@]}" -eq 0 ]]; then return 0; fi
  if [[ "${#entries[@]}" -eq 1 && "${entries[0]}" == "_incoming" ]]; then return 0; fi
  return 1
}

create_dirs() {
  mkdir -p "$INCOMING"
  mkdir -p "$(dirname "$TARGET_ROOT")"
  pass "created $TARGET_ROOT/_incoming"
}

install_clone() {
  if [[ -d "$TARGET_ROOT/.git" ]]; then
    log "Existing git checkout found. Updating with git pull --ff-only."
    git -C "$TARGET_ROOT" remote set-url origin "$REPO_URL" || true
    git -C "$TARGET_ROOT" fetch origin
    git -C "$TARGET_ROOT" pull --ff-only origin main || git -C "$TARGET_ROOT" pull --ff-only
    pass "GitHub clone/download update from mppcoder/factory-template"
    return 0
  fi

  if ! is_empty_or_incoming_only "$TARGET_ROOT"; then
    fail "Target root exists and is not a git checkout or empty/_incoming-only. Refusing to delete or overwrite $TARGET_ROOT."
  fi

  local tmp
  tmp="$(mktemp -d "${TARGET_ROOT}.tmp-clone.XXXXXX")"
  git clone "$REPO_URL" "$tmp"
  mkdir -p "$TARGET_ROOT"
  cp -a "$tmp"/. "$TARGET_ROOT"/
  rm -rf "$tmp"
  pass "GitHub clone/download install from mppcoder/factory-template"
}

install_archive() {
  local archive="$INCOMING/$ARCHIVE_NAME"
  local manifest="$INCOMING/$MANIFEST_NAME"
  local checksum="$INCOMING/$CHECKSUM_NAME"
  [[ -f "$archive" ]] || fail "Missing archive: $archive"
  [[ -f "$manifest" ]] || fail "Missing manifest: $manifest"
  [[ -f "$checksum" ]] || fail "Missing checksum: $checksum"

  (cd "$INCOMING" && sha256sum -c "$CHECKSUM_NAME")
  pass "archive sha256"

  if ! is_empty_or_incoming_only "$TARGET_ROOT"; then
    if [[ -f "$TARGET_ROOT/template-repo/scripts/verify-all.sh" ]]; then
      log "Existing factory-template root found. Archive reinstall will not overwrite it; running validation on existing root."
    else
      fail "Target root exists and is not empty/_incoming-only. Refusing to delete or overwrite $TARGET_ROOT."
    fi
  else
    local unpack
    unpack="$(mktemp -d "$INCOMING/archive-unpack.XXXXXX")"
    unzip -q "$archive" -d "$unpack"
    local roots=()
    while IFS= read -r item; do roots+=("$item"); done < <(find "$unpack" -mindepth 1 -maxdepth 1 -type d -printf '%p\n')
    [[ "${#roots[@]}" -eq 1 ]] || fail "Archive must contain exactly one root folder."
    mkdir -p "$TARGET_ROOT"
    cp -a "${roots[0]}"/. "$TARGET_ROOT"/
    rm -rf "$unpack"
    pass "archive expanded into /projects/factory-template"
  fi

  # Required archive-layout setup and validation commands:
  # bash POST_UNZIP_SETUP.sh
  # python3 template-repo/scripts/validate-release-package.py
  # bash template-repo/scripts/verify-all.sh quick
  (cd "$TARGET_ROOT" && bash POST_UNZIP_SETUP.sh)
  (cd "$TARGET_ROOT" && python3 template-repo/scripts/validate-release-package.py "$archive" --checksum "$checksum" --manifest "$manifest")
  pass "archive manifest/checksum validation"
}

run_quick_verify() {
  [[ -f "$TARGET_ROOT/template-repo/scripts/verify-all.sh" ]] || fail "verify-all.sh not found under $TARGET_ROOT"
  (cd "$TARGET_ROOT" && bash template-repo/scripts/verify-all.sh quick)
  pass "bash template-repo/scripts/verify-all.sh quick"
}

main() {
  log "Factory Template remote install starting"
  log "mode=$MODE target=$TARGET_ROOT incoming=$INCOMING"
  ensure_tools
  create_dirs
  case "$MODE" in
    clone) install_clone ;;
    archive) install_archive ;;
  esac
  run_quick_verify
  pass "FACTORY TEMPLATE REMOTE INSTALL COMPLETE"
}

main "$@"
