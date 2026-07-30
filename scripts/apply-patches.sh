#!/usr/bin/env bash
# Resets ./firefox to a clean upstream checkout, then applies every patch in
# patches/ (in filename order) on top of it.
set -euo pipefail
cd "$(dirname "$0")/.."

DEST="firefox"
if [ ! -d "$DEST/.git" ]; then
  echo "firefox/ not found; run scripts/fetch.sh first" >&2
  exit 1
fi

git -C "$DEST" reset --hard HEAD
git -C "$DEST" clean -fdx --exclude=/obj-*

shopt -s nullglob
patches=(patches/*.patch)
if [ ${#patches[@]} -eq 0 ]; then
  echo "No patches in patches/ yet"
  exit 0
fi

for patch in "${patches[@]}"; do
  echo "Applying $patch"
  git -C "$DEST" apply --index "../$patch"
done

echo "Applied ${#patches[@]} patch(es)"

# Binary assets (icons etc.) live in branding/ and are copied in rather than
# diffed, to keep patches/ as plain text.
if [ -f branding/icon/canadafox.icns ]; then
  cp branding/icon/canadafox.icns "$DEST/browser/branding/unofficial/firefox.icns"
  echo "Copied branding/icon/canadafox.icns -> $DEST/browser/branding/unofficial/firefox.icns"
fi

# Vendored IP-to-country database (see vendor/geoip/README.md). Binary asset,
# so it is copied rather than carried as a text patch.
if [ -f vendor/geoip/dbip-country.bin ]; then
  cp vendor/geoip/dbip-country.bin "$DEST/browser/branding/unofficial/content/dbip-country.bin"
  echo "Copied vendor/geoip/dbip-country.bin -> $DEST/browser/branding/unofficial/content/"
fi

# Vendored, unmodified, Mozilla-signed extension xpis (see vendor/extensions/
# README.md) get copied in the same way, rather than committed as a diff.
if [ -d vendor/extensions ]; then
  mkdir -p "$DEST/browser/app/distribution/extensions"
  cp vendor/extensions/*.xpi "$DEST/browser/app/distribution/extensions/"
  echo "Copied vendor/extensions/*.xpi -> $DEST/browser/app/distribution/extensions/"
fi
