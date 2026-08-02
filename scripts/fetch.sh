#!/usr/bin/env bash
# Clones the latest upstream Firefox source into ./firefox (shallow, no history).
set -euo pipefail
cd "$(dirname "$0")/.."

REPO_URL="https://github.com/mozilla-firefox/firefox.git"
DEST="firefox"
# CanadaFox tracks Release, not Nightly: the channel real users actually run,
# vetted and shipped every ~4 weeks, vs. Nightly's daily, experimental churn.
BRANCH="release"

if [ -d "$DEST/.git" ]; then
  echo "firefox/ already exists; fetching latest $BRANCH instead of re-cloning"
  git -C "$DEST" fetch --depth 1 origin "$BRANCH"
  # Not "origin/$BRANCH": a --single-branch clone only tracks one branch's
  # refspec, so switching branches here means origin/<branch> was never
  # created. FETCH_HEAD always works regardless of tracking-ref state.
  git -C "$DEST" reset --hard FETCH_HEAD
else
  git clone --depth 1 --single-branch --branch "$BRANCH" "$REPO_URL" "$DEST"
fi

git -C "$DEST" log -1 --format='Fetched Firefox source at commit %H (%ci)'
