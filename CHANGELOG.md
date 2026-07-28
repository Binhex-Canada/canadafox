# Changelog

All notable changes to CanadaFox are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- uBlock Origin bundled as a pre-installed, unmodified extension (auto-updates
  from AMO like any normal add-on; kept under its own name, authorship, and
  version — CanadaFox doesn't claim it or fork it).
- A dedicated **CanadaFox** section in the Settings sidebar (its own icon, a
  Canadian flag matching the size/style of the other sidebar icons) collecting
  every CanadaFox-specific setting in one place, plus a list of the
  pre-installed add-ons.
- A full-color Canadian flag button, hard-coded into the main toolbar next to
  the app menu.
- AI features (chat sidebar, Smart Window, smart tab groups, link-preview key
  points, PDF alt-text, and the AI Controls settings pane itself) locked off
  by default via distribution policy, with no in-app way to turn them back
  on. On-device page Translations is untouched and still works.

### Fixed
- The first-run Canadian-quote tab now stays pinned and persists across
  restarts like a normal pinned tab, instead of only appearing on the very
  first launch. It stays until the user closes it themselves, then it's gone
  for good.

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
