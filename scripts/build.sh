#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d firefox/.git ]; then
  echo "firefox/ not found; run scripts/fetch.sh first" >&2
  exit 1
fi

export MOZCONFIG="$(pwd)/mozconfig"
cd firefox
python3 ./mach build
