#!/usr/bin/env bash
# Clones the latest upstream Firefox source into ./firefox (shallow, no history).
set -euo pipefail
cd "$(dirname "$0")/.."

REPO_URL="https://github.com/mozilla-firefox/firefox.git"
DEST="firefox"

if [ -d "$DEST/.git" ]; then
  echo "firefox/ already exists; fetching latest main instead of re-cloning"
  git -C "$DEST" fetch --depth 1 origin main
  git -C "$DEST" reset --hard origin/main
else
  git clone --depth 1 --single-branch --branch main "$REPO_URL" "$DEST"
fi

git -C "$DEST" log -1 --format='Fetched Firefox source at commit %H (%ci)'
