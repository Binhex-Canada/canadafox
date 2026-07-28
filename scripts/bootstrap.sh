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

# sccache caches compiled objects across builds, speeding up repeat
# `mach build` runs (e.g. after apply-patches.sh resets the tree). Optional:
# only wired up in mozconfig if it's actually on PATH.
if ! command -v sccache >/dev/null 2>&1 && command -v brew >/dev/null 2>&1; then
  brew install sccache
fi
