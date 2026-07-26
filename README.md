# Super Browser Land

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

## Status

- [x] Repo scaffold
- [x] Fetch upstream Firefox source (`mozilla-firefox/firefox`)
- [x] First patch set (see `patches/`): Health Report + Normandy/Shield
      studies disabled at compile time (which also kills the whole
      data-reporting/data-submission-policy subsystem given our unofficial,
      crash-reporter-disabled build); Safe Browsing malware/phishing lookups
      off; region-update and connectivity-service pings off; New Tab
      sponsored tiles (Contile), Discovery Stream/Pocket recommendations,
      search SERP telemetry, and the FxA telemetry ping off
- [ ] Bootstrap build deps and first build
- [ ] Further passes: Nimbus network calls, ASRouter/CFR messaging fetches,
      default search partner codes, DoH provider defaults, Merino/Firefox
      Suggest, branding

Note: disabling Safe Browsing removes built-in phishing/malware warnings —
that protection normally works by querying Google, so removing the query
removes the protection too. Reversible via prefs later if wanted.
