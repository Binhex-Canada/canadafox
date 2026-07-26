#!/usr/bin/env bash
# Rasterizes branding/icon/icon.svg into branding/icon/superbrowserland.icns.
# Uses macOS's own SVG renderer (qlmanage) since there's no rsvg-convert here.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="branding/icon/icon.svg"
DIR="branding/icon"
ICONSET="$DIR/superbrowserland.iconset"

rm -f "$DIR/icon.svg.png"
qlmanage -t -s 1024 -o "$DIR" "$SRC" >/dev/null

rm -rf "$ICONSET"
mkdir "$ICONSET"

sizes=(
  "16 icon_16x16.png"
  "32 icon_16x16@2x.png"
  "32 icon_32x32.png"
  "64 icon_32x32@2x.png"
  "128 icon_128x128.png"
  "256 icon_128x128@2x.png"
  "256 icon_256x256.png"
  "512 icon_256x256@2x.png"
  "512 icon_512x512.png"
  "1024 icon_512x512@2x.png"
)
for spec in "${sizes[@]}"; do
  size="${spec%% *}"
  name="${spec#* }"
  sips -z "$size" "$size" "$DIR/icon.svg.png" --out "$ICONSET/$name" >/dev/null
done

iconutil -c icns "$ICONSET" -o "$DIR/superbrowserland.icns"
echo "Wrote $DIR/superbrowserland.icns"
