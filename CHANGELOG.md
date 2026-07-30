# Changelog

All notable changes to CanadaFox are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.0.3] - unreleased

### Added
- **Canadian DNS.** DNS-over-HTTPS now goes through
  [CIRA Canadian Shield](https://www.cira.ca/en/canadian-shield/) — the
  resolver run by the non-profit that operates the `.ca` registry — on its
  Protected tier, which also blocks known malware and phishing domains.
  Lookups stay on Canadian infrastructure instead of a US resolver. Firefox
  falls back to the system resolver if it is unreachable, so captive portals
  and hotel Wi-Fi still work, and the setting is left unlocked so it can be
  changed in Settings.
- **"Served from" in the site-information panel.** Click the padlock and
  CanadaFox shows which country answered the connection. The lookup runs
  entirely offline against a bundled database — nothing about your browsing
  is sent anywhere to produce it. Note this reports the *responding server*,
  not where a company stores your data: a foreign site behind a CDN often
  answers from a Canadian edge node.
- New Tab shows a self-contained page (no network request) that rotates
  through Canadian trivia, or an "on this day in Canadian history" fact when
  today's date matches one, instead of the normal topsites/shortcuts grid.
  It's a real `about:` page (`about:canadafoxnewtab`), so the address bar
  stays empty on a new tab exactly as it does in stock Firefox.
- A pre-loaded **Canadian Services** bookmarks folder (Canada Revenue Agency,
  Service Canada, Canada.ca Health, CBC News) on the bookmarks toolbar.
- CanadaFox checks GitHub once per session for a newer release and shows a
  dismissible notification bar if one's available, linking to the release
  page. It never downloads or installs anything automatically, and only
  notifies once per newly-seen version.

### Changed
- The bookmarks toolbar is shown by default, so the pre-loaded folder is
  actually visible. Set as a real default pref rather than through
  distribution.ini's `browser.showPersonalToolbar`, which only writes the
  setting on a profile's very first run and so never reached existing
  profiles. Changing it in View > Toolbars still takes precedence.
- The About dialog no longer shows the internal distribution identifier
  (e.g. "canadafox - 1.0").
- `about:home`'s startup cache is disabled. It assumes Activity Stream has
  been constructed, which no longer happens now that new tabs point
  elsewhere; the cache only pre-renders `about:home` slightly sooner, so
  this trades a marginal startup optimization for a clean startup.

### Fixed
- The Canadian welcome/quote page now actually persists. It opens pinned on a
  profile's first run and is restored on every launch after that until the
  user closes it, after which it stays gone. Three separate causes: it was a
  `data:` URI, which Firefox blocks for top-level navigation outright; its
  appearance was tied to Firefox's one-shot first-run trigger, which fires
  once per profile and so could never mean "always there until dismissed";
  and dismissal was recorded on any tab close, including the ones fired while
  the window tears down at shutdown — so quitting counted as dismissing it.
- The welcome and New Tab pages are served as real `about:` pages rather than
  `data:` URIs. Besides being blocked for top-level navigation, `data:` pages
  get a null principal, which is why a raw base64 blob used to appear in the
  address bar.
- An intermittent startup crash introduced while fixing the New Tab page:
  overriding `AboutNewTab` tore down Activity Stream, which
  `AboutHomeStartupCache` then dereferenced unconditionally.

### Internal
- Rebased onto Firefox Nightly `878b64a4c024` (2026-07-30), 769 commits newer
  than the previous base. All patches applied without conflict.
- Builds go through `sccache`, so unchanged objects are reused between
  rebuilds instead of recompiled from scratch.

## [0.0.2] - 2026-07-28

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
