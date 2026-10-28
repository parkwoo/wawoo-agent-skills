#!/usr/bin/env bash
# Copy internal.example → internal/ (outside git)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/internal.example"
DST="${ROOT}/internal"

if [[ ! -d "$SRC" ]]; then
  echo "missing: $SRC" >&2
  exit 1
fi

mkdir -p "$DST"
rsync -a --delete "${SRC}/" "${DST}/"
echo "OK: updated ${DST}/ (outside git)"
