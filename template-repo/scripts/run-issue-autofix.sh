#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: bash run-issue-autofix.sh <codex-input.md> [--dry-run] [--no-push]
USAGE
}

HANDOFF=""
DRY_RUN=0
NO_PUSH=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --no-push)
      NO_PUSH=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$HANDOFF" ]]; then
        HANDOFF="$1"
        shift
      else
        echo "Unknown arg: $1" >&2
        usage >&2
        exit 2
      fi
      ;;
  esac
done

if [[ -z "$HANDOFF" || ! -f "$HANDOFF" ]]; then
  echo "codex input file is required" >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
ISSUE_NUMBER="$(grep -E '^- number: ' "$HANDOFF" | head -1 | sed 's/^- number: //')"
REPO="$(grep -E '^- repo: ' "$HANDOFF" | head -1 | sed 's/^- repo: //')"
TITLE="$(grep -E '^- title: ' "$HANDOFF" | head -1 | sed 's/^- title: //' | tr '\n' ' ' | cut -c1-120)"
if [[ -z "$ISSUE_NUMBER" ]]; then
  echo "could not parse issue number from $HANDOFF" >&2
  exit 2
fi
BRANCH="codex/issue-${ISSUE_NUMBER}"
RUN_DIR=".chatgpt/issue-runs/issue-${ISSUE_NUMBER}"
RUN_YAML="$RUN_DIR/run.yaml"
mkdir -p "$RUN_DIR"

gh_label() {
  local add_label="$1"
  local remove_label="${2:-}"
  if [[ -n "${GH_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1 && [[ -n "$REPO" ]]; then
    if [[ -n "$remove_label" ]]; then
      gh issue edit "$ISSUE_NUMBER" --repo "$REPO" --remove-label "$remove_label" >/dev/null 2>&1 || true
    fi
    gh issue edit "$ISSUE_NUMBER" --repo "$REPO" --add-label "$add_label" >/dev/null 2>&1 || true
  fi
}

write_state() {
  local status="$1"
  local verification="$2"
  local launcher_command="$3"
  {
    echo "schema: issue-autofix-run/v1"
    echo "repo: \"$REPO\""
    echo "issue_number: \"$ISSUE_NUMBER\""
    echo "status: \"$status\""
    echo "handoff_path: \"$HANDOFF\""
    echo "branch: \"$BRANCH\""
    echo "pr_number: null"
    echo "verification: \"$verification\""
    echo "launcher_command: \"$launcher_command\""
    echo "no_push: \"$NO_PUSH\""
    echo "dry_run: \"$DRY_RUN\""
  } > "$RUN_YAML"
}

git switch -C "$BRANCH"
gh_label "agent:running" "agent:claimed"

SCRIPT_PREFIX="template-repo/scripts"
if [[ ! -d "$SCRIPT_PREFIX" ]]; then
  SCRIPT_PREFIX="scripts"
fi

LAUNCHER_COMMAND="bash $SCRIPT_PREFIX/launch-codex-task.sh --task-file $HANDOFF --launch-source direct-task --dry-run"
if [[ "$DRY_RUN" -eq 1 ]]; then
  "$SCRIPT_PREFIX/launch-codex-task.sh" --task-file "$HANDOFF" --launch-source direct-task --dry-run | tee "$RUN_DIR/launcher-output.txt"
  write_state "dry_run_complete" "pending" "$LAUNCHER_COMMAND"
  exit 0
fi

"$SCRIPT_PREFIX/launch-codex-task.sh" --task-file "$HANDOFF" --launch-source direct-task --dry-run | tee "$RUN_DIR/launcher-output.txt"

if [[ "${ISSUE_AUTOFIX_EXECUTE:-false}" == "true" ]]; then
  echo "ISSUE_AUTOFIX_EXECUTE=true is set, but non-interactive Codex execution must be supplied by a controlled runner." >&2
fi

VERIFY_CMD="bash $SCRIPT_PREFIX/verify-all.sh quick"
if [[ -x "$SCRIPT_PREFIX/verify-all.sh" || -f "$SCRIPT_PREFIX/verify-all.sh" ]]; then
  bash "$SCRIPT_PREFIX/verify-all.sh" quick | tee "$RUN_DIR/verify-output.txt"
fi

if [[ -n "$(git status --short)" ]]; then
  git add -A
  git commit -m "Fix issue #${ISSUE_NUMBER}"
  if [[ "$NO_PUSH" -eq 0 ]] && git remote get-url origin >/dev/null 2>&1; then
    git push -u origin "$BRANCH"
    if command -v gh >/dev/null 2>&1 && [[ -n "${GH_TOKEN:-}" && -n "$REPO" ]]; then
      PR_BODY=$'Refs #'"$ISSUE_NUMBER"$'\n\nVerification:\n- '"$VERIFY_CMD"
      gh pr create --repo "$REPO" --title "Fix #${ISSUE_NUMBER}: ${TITLE}" --body "$PR_BODY" || true
    fi
  fi
  gh_label "agent:pr-opened"
  gh_label "agent:human-review"
  write_state "pr_ready_or_created" "green" "$LAUNCHER_COMMAND"
else
  gh_label "agent:blocked"
  write_state "blocked_no_changes" "green_no_changes" "$LAUNCHER_COMMAND"
fi
