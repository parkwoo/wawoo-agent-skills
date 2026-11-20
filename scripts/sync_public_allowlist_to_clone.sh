#!/usr/bin/env bash
# vault 運用正本 → 公開 clone：.publish-allowlist の路径のみ rsync/cp（D-06）
#
# workspace/skills 全体を publish しない。正本: docs/plans/SKILLS-RENAME-SITE-TASKS.md §公开境界
#
# Usage:
#   scripts/sync_public_allowlist_to_clone.sh              # 反映
#   scripts/sync_public_allowlist_to_clone.sh --dry-run  # 一覧のみ
#   scripts/sync_public_allowlist_to_clone.sh --check    # 差分があれば exit 1
#
# Env:
#   VAULT_SKILLS   既定: 本脚本の親ディレクトリ（workspace/skills）
#   PUBLIC_CLONE   既定: WAWOO_KIT_OSS_ROOT または /home/git/wawoo-agent-skills
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VAULT_SKILLS="${VAULT_SKILLS:-$ROOT}"
PUBLIC_CLONE="${PUBLIC_CLONE:-${WAWOO_KIT_OSS_ROOT:-/home/git/wawoo-agent-skills}}"
ALLOWLIST="${ALLOWLIST:-$VAULT_SKILLS/.publish-allowlist}"
EXCLUDES="${EXCLUDES:-$ROOT/scripts/public_sync_excludes.txt}"

case "${1:-apply}" in
  --check|check) MODE=check ;;
  --dry-run|dry) MODE=dry ;;
  ""|apply|--apply) MODE=apply ;;
  *)
    echo "usage: $0 [--check|--dry-run|apply]" >&2
    exit 2
    ;;
esac

if [[ ! -f "$ALLOWLIST" ]]; then
  echo "ERROR: allowlist がありません: $ALLOWLIST" >&2
  exit 1
fi
if [[ ! -d "$PUBLIC_CLONE/.git" ]]; then
  echo "ERROR: 公開 clone ではありません: $PUBLIC_CLONE" >&2
  exit 1
fi

RSYNC_DRY=()
[[ "$MODE" == dry ]] && RSYNC_DRY=(--dry-run)
[[ "$MODE" == check ]] && RSYNC_DRY=(--dry-run)

drift=0
scanned=0
changed=0

sync_file() {
  local rel="$1"
  local src="$VAULT_SKILLS/$rel"
  local dst="$PUBLIC_CLONE/$rel"
  if [[ ! -e "$src" ]]; then
    echo "MISSING-VAULT $rel"
    drift=1
    return
  fi
  scanned=$((scanned + 1))
  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    return
  fi
  changed=$((changed + 1))
  case "$MODE" in
    check) echo "DRIFT $rel"; drift=1 ;;
    dry) echo "would sync $rel" ;;
    apply)
      mkdir -p "$(dirname "$dst")"
      cp -f "$src" "$dst"
      echo "synced $rel"
      ;;
  esac
}

sync_dir() {
  local rel="${1%/}"
  local src="$VAULT_SKILLS/$rel/"
  local dst="$PUBLIC_CLONE/$rel/"
  if [[ ! -d "$src" ]]; then
    echo "MISSING-VAULT-DIR $rel/"
    drift=1
    return
  fi
  scanned=$((scanned + 1))
  if [[ "$MODE" == check ]]; then
    if ! rsync -ani --delete "${RSYNC_DRY[@]}" "$src" "$dst" 2>/dev/null | grep -q .; then
      return
    fi
    echo "DRIFT $rel/"
    drift=1
    changed=$((changed + 1))
    return
  fi
  if [[ "$MODE" == dry ]]; then
    echo "would rsync $rel/"
    rsync -ani "${RSYNC_DRY[@]}" "$src" "$dst" || true
    return
  fi
  mkdir -p "$dst"
  if [[ -f "$EXCLUDES" ]] && [[ "$rel" == .kilo ]]; then
    rsync -a --delete --exclude-from="$EXCLUDES" "$src" "$dst"
    echo "rsynced $rel/ (excludes from public_sync_excludes.txt)"
  else
    rsync -a --delete "$src" "$dst"
    echo "rsynced $rel/"
  fi
  changed=$((changed + 1))
}

purge_public_forbidden() {
  [[ "$MODE" != apply ]] && return
  [[ ! -f "$EXCLUDES" ]] && return
  while IFS= read -r rel || [[ -n "$rel" ]]; do
    rel="${rel%%#*}"
    rel="$(echo "$rel" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ -z "$rel" ]] && continue
    local target="$PUBLIC_CLONE/$rel"
    if [[ -e "$target" ]]; then
      rm -rf "$target"
      echo "purged forbidden $rel"
    fi
  done <"$EXCLUDES"
}

while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%#*}"
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" ]] && continue
  if [[ "$line" == internal/* ]] || [[ "$line" == .publish-allowlist ]]; then
    echo "ERROR: allowlist に internal 系が含まれています: $line" >&2
    exit 1
  fi
  if [[ "$line" == */ ]]; then
    sync_dir "$line"
  elif [[ "$line" == */* ]] && [[ -d "$VAULT_SKILLS/$line" ]]; then
    sync_dir "$line"
  else
    sync_file "$line"
  fi
done <"$ALLOWLIST"

purge_public_forbidden

if [[ "$MODE" == check ]]; then
  if [[ $drift -eq 0 ]]; then
    echo "OK: $scanned allowlist エントリ、公開 clone と一致"
    exit 0
  fi
  echo "DRIFT: $changed 件。修正後: $0 apply" >&2
  exit 1
fi

echo "done: mode=$MODE scanned=$scanned changed~=$changed"
echo "  vault:  $VAULT_SKILLS"
echo "  public: $PUBLIC_CLONE"
echo "次: cd $PUBLIC_CLONE && git status && git commit && git push origin master"