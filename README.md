# CanadaFox

A privacy-hardened macOS browser built by patching upstream Firefox: all
telemetry, tracking, and "phone home" behavior removed as a starting point.

There is no point in using this software. Why would you use this?

This repo does **not** vendor the Firefox source tree. It holds:

- `patches/` — patches applied on top of a clean Firefox checkout
- `mozconfig` — build configuration
- `scripts/` — fetch, patch, bootstrap, and build helpers
- `branding/` — app name/icon overrides (added later)

The upstream source is cloned into `./firefox/` (gitignored) so it can be
re-fetched and re-patched against new Firefox releases, the same model
LibreWolf and Mullvad Browser use.

## Setup

```bash
scripts/fetch.sh          # clone latest Firefox source into ./firefox
scripts/apply-patches.sh  # apply patches/*.patch on top of a clean checkout
scripts/bootstrap.sh      # one-time: install Firefox's build dependencies
scripts/build.sh          # build (mach build)
scripts/run.sh            # run the built browser
```

## Version

| | |
|---|---|
| CanadaFox version | `0.0.1` |
| Based on | Firefox `155.0a1` |
| Upstream source | [`mozilla-firefox/firefox`](https://github.com/mozilla-firefox/firefox) @ `34ce15fe54f7` (2026-07-26) |
| Patches applied | 10 (see `patches/`) |

Note: Safe Browsing (phishing/malware warnings) is left on, at stock
Firefox behavior — it does query Google, unlike everything else this
project strips out, but the security value was judged worth that one
exception.

Note: pinned tabs are "locked" by default (Settings → Tabs → *Keep pinned
tabs from navigating away*) — any link click or address-bar entry on a
pinned tab opens in a new tab instead, matching how Safari-style tabs
behave. Unpin a tab to get normal navigation back. Pure JS-driven
navigation (e.g. a page redirecting itself via `window.location`) isn't
covered by this yet.
