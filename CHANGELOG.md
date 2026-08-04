# Changelog

All notable changes to CanadaFox are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.0.3.6] - 2026-08-03

### Added
- A Canadian sales tax calculator, in three places for discoverability:
  a green $ button in the toolbar (opens a small panel with an amount
  field and province dropdown), a widget on every New Tab page, and a
  power-user address-bar shortcut (type an amount followed by "tax" and
  a province, e.g. `50 tax on` or `$49.99 tax bc`). All three compute
  the same GST/HST/PST breakdown and total entirely locally from the
  standard published federal and provincial rates -- no network request.
  These are general statutory rates; some goods and services (basic
  groceries, prescription drugs, etc.) are zero-rated or exempt, so
  treat it as an estimate rather than a guarantee of what any specific
  purchase will charge.

### Removed
- The decorative full-colour Canadian flag toolbar button. It did nothing
  when clicked, and sitting immediately beside the new tax-calculator
  button it read as though it were an action, which was more confusing
  than decorative. The Canadian flag icon in the Settings sidebar (which
  does navigate somewhere) is unaffected.

## [0.0.3.5] - 2026-08-02

### Changed
- CanadaFox now tracks Firefox's **Release** channel instead of Nightly.
  Nightly is a daily, unstable, experimental build never meant to be
  anyone's main browser; Release is the same code real Firefox users run,
  vetted and shipped roughly every 4 weeks. Rebased onto Firefox `153.0.3`
  (from Nightly `155.0a1`); all 31 patches carried forward with 100% of
  existing features preserved and re-verified. `scripts/fetch.sh` now
  pulls the `release` branch.
- The welcome/quote tab is now shown in the foreground on every startup,
  instead of pinned in the background while some other tab (often a
  blank-looking `about:home`) is shown up front. Sticks even if a
  different tab was selected when the browser last closed.

### Fixed
- The bookmarks toolbar could get permanently forced to "never show" by a
  one-time Firefox profile-data migration (`ProfileDataUpgrader`) reacting
  to old, pre-CanadaFox profile state, silently overriding our "always
  show" default with a persisted user pref. Not a CanadaFox code bug as
  such -- the migration is stock Firefox behavior -- but worth knowing
  about if this resurfaces: clearing the
  `browser.toolbars.bookmarks.visibility` user pref restores our default.

## [0.0.3a / 0.0.3.1] - 2026-07-30

### Added
- (0.0.3a) Fixed the Canadian Services bookmarks folder and the welcome
  tab both silently going stale on existing profiles, caused by two
  different "did this already run" one-shot flags that never accounted
  for the thing they gated disappearing for reasons other than genuine
  completion: distribution.ini's bookmark import only ever runs once per
  profile ever, so a profile that already ran it before the Benefits
  Finder/BC Services entries were added could never receive them; and the
  welcome tab's own "already created" pref meant it could never come back
  once removed by anything other than the user closing it (a crash, a
  killed test process, mid-session-restore). Both are now self-healing on
  every startup instead: bookmarks are topped up by URL, and the welcome
  tab is checked for with SessionStore.getTabState (which, unlike a plain
  URL check, still works on a not-yet-loaded restored tab). Caught by
  testing directly against a real, previously-used profile rather than
  a fresh one -- every prior verification this cycle used a fresh
  profile, which never exercises the one-shot-flag path at all.
- **Address-bar keyword shortcuts** for the Canadian Services bookmarks:
  type `cra`, `service`, `health`, or `cbc` and hit enter instead of
  navigating there manually.
- Two more entries in the **Canadian Services** bookmarks folder: the
  federal Benefits Finder and BC's Services A-Z directory.
- **Heritage Minute error pages.** Genuine network errors (page not found,
  connection refused, offline) now show a short blurb from a real Historica
  Canada Heritage Minute — Naismith inventing basketball, Wilder Penfield's
  "burnt toast," Vince Coleman at the Halifax Explosion, and others.
  Deliberately left off certificate/security warning pages, where a playful
  aside doesn't belong. Wired into both of Firefox's error-page rendering
  paths, since a very recent Nightly refresh (`security.certerrors.felt-privacy-v1`)
  replaces the classic one for most error types.
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

### Added (cont.)
- A **Sovereign Privacy** toggle in Settings → CanadaFox, so CIRA Canadian
  Shield DNS can be turned off without needing to know it's implemented as an
  enterprise policy. On is the shipped default; off reverts to plain system
  DNS, not a different DoH provider. Takes effect immediately, no restart.

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
