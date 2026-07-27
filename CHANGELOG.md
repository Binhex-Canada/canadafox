# Changelog

All notable changes to CanadaFox are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- [uBlock Origin](https://addons.mozilla.org/firefox/addon/ublock-origin/)
  now comes pre-installed as a normal, unmodified, Mozilla-signed extension
  (`1.72.2` at time of vendoring) — same name, author, and GPLv3 license as
  upstream, updates itself through the regular AMO update mechanism, and
  can be disabled or removed like any other extension. See
  `vendor/extensions/README.md` for attribution and update instructions.

### Changed
- The CanadaFox Settings page now has its own sidebar entry ("CanadaFox",
  with a Canada-flag icon matching the style of the other sidebar icons)
  instead of only being reachable as a subsection, and gained a
  "Pre-installed extensions" section listing uBlock Origin with a link to
  manage it in `about:addons`.

### Fixed
- The first-run Canadian-quote page only ever showed once, then never
  again even if you hadn't closed it. It's now pinned on first run, so it
  persists across restarts like any other pinned tab — it sticks around
  until you close it, then it's gone for good.

## [0.0.1] - 2026-07-27

### Added
- DuckDuckGo set as the default search engine.
- Pinned tabs "locked" by default: link clicks and address-bar entry on a
  pinned tab open in a new tab instead of navigating it away. Toggle at
  Settings → Tabs → *Keep pinned tabs from navigating away*.
- A dedicated **Settings → CanadaFox Settings** page that cross-references
  every CanadaFox-specific setting in one place, without moving any of them
  out of their normal section.
- First-run tab now shows a local, self-contained page (no network request)
  with a Canadian historical quote, in place of Mozilla's privacy policy
  page. Static for now — may pull from a public archive of random Canadian
  facts later.
- Custom About-dialog tagline ("Because the Internet won't browse itself!").
- About dialog now also shows "Based on Firefox `<version>`", the upstream
  Gecko platform version, alongside the CanadaFox version.
- Typing a URL or search into the address bar opens in a new tab instead of
  overwriting the current one (except on a blank/new tab), matching
  Safari-style tab persistence.

### Changed
- Rebranded from Nightly to CanadaFox throughout: app name, bundle ID,
  macOS icon, About dialog, New Tab and Private Browsing wordmarks.
- Safe Browsing (phishing/malware protection) re-enabled at stock Firefox
  behavior, reversing the initial scaffold's removal — judged worth the one
  remaining Google network call.
- Version scheme reset to `0.0.1`.

### Fixed
- About dialog, New Tab, and Private Browsing pages still showed "Nightly"
  after the rebrand — the wordmark was vector artwork with the name drawn
  in, not a translatable string. Replaced with a text-based wordmark.
- The first-run Canadian-quote page was opening in a background tab while
  a blank New Tab loaded in front of it, hiding it. Switched to Firefox's
  built-in first-run mechanism so the quote page is the sole startup tab.

## [Unreleased scaffold]
- Initial patch-fork of Firefox with telemetry and tracking removed:
  Health Report and Normandy/Shield studies disabled at compile time,
  Safe Browsing malware/phishing lookups off, region-update and
  connectivity-service pings off, New Tab sponsored tiles and Discovery
  Stream/Pocket recommendations off, search SERP telemetry and the FxA
  telemetry ping off.
