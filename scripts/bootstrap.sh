#!/usr/bin/env bash
# One-time: install Firefox's build dependencies via its own bootstrap tool.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d firefox/.git ]; then
  echo "firefox/ not found; run scripts/fetch.sh first" >&2
  exit 1
fi

cd firefox
python3 ./mach bootstrap --application-choice=browser
