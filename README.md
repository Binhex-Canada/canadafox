# CanadaFox

![The flag of Canada](docs/images/canada-flag-4k.png)

A privacy-hardened macOS browser built by patching upstream Firefox: all
telemetry, tracking, and "phone home" behavior removed as a starting point.

There is no point in using this software. Why would you use this? This was created during a fever dream. Hey, wasn't the movie Obession great? 

See [CHANGELOG.md](CHANGELOG.md) for what's changed release to release.

This repo does **not** vendor the Firefox source tree. It holds:

- `patches/` — patches applied on top of a clean Firefox checkout
- `mozconfig` — build configuration
- `scripts/` — fetch, patch, bootstrap, and build helpers
- `branding/` — app name/icon overrides (added later)
- `vendor/` — unmodified, third-party binary assets (see the README in each subfolder)
- `CHANGELOG.md` — release history

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
| CanadaFox version | `0.0.3.6` |
| Based on | Firefox `153.0.3` (Release channel) |
| Upstream source | [`mozilla-firefox/firefox`](https://github.com/mozilla-firefox/firefox), `release` branch @ `1d94c318b8fd` (2026-08-01) |
| Patches applied | 32 (see `patches/`) |

Note: CanadaFox tracks Firefox's **Release** channel, not Nightly — the
build vetted and shipped to real users every ~4 weeks, rather than daily,
unstable, experimental snapshots. Nobody should run a daily browser as
their main one. `scripts/fetch.sh` pulls the `release` branch.

Note: Safe Browsing (phishing/malware warnings) is left on, at stock
Firefox behavior — it does query Google, unlike everything else this
project strips out, but the security value was judged worth that one
exception.

Note: pinned tabs are "locked" by default (Settings → Tabs → *Keep pinned
tabs from navigating away*) — any link click or address-bar entry on a
pinned tab opens in a new tab instead, matching how Safari-style tabs
behave. Unpin a tab to get normal navigation back. Pure JS-driven
navigation (e.g. a page redirecting itself via `window.location`) isn't
covered by this yet. This setting is flagged in Settings as CanadaFox-specific,
since it doesn't exist in stock Firefox.

Note: every CanadaFox-specific setting also shows up together on its own
page (Settings → CanadaFox Settings) as a cross-reference, in addition to
staying in its normal section — nothing is moved out of where a Firefox
user would expect to find it.

Note: [uBlock Origin](https://addons.mozilla.org/firefox/addon/ublock-origin/)
comes pre-installed, unmodified, and Mozilla-signed — same name, same
author (Raymond Hill & contributors), same GPLv3 license, and it updates
itself through the normal AMO update mechanism like any extension you'd
install yourself. CanadaFox doesn't own, modify, or sell it; see
`vendor/extensions/README.md` for attribution and how to pull in updates.
Users can disable or remove it like any other extension.

Note: New Tab (not the Home button/startup page) shows a self-contained
page with rotating Canadian trivia, or an "on this day in Canadian
history" fact when today's date matches one, instead of the normal
topsites/shortcuts grid. It's registered as a real `about:` page
(`about:canadafoxnewtab`), so the address bar stays empty on a new tab
just like it does in stock Firefox.

Note: the Canadian welcome/quote page (`about:canadafoxwelcome`) opens
pinned the first time a profile runs and, being pinned, comes back on
every launch after that. Close it and it's gone for good.

Note: a **Canadian Services** bookmarks folder (CRA, Service Canada,
Canada.ca Health, CBC News) is pre-loaded onto the bookmarks toolbar,
which is shown by default.

Note: typing an amount followed by "tax" and a province in the address
bar, e.g. `50 tax on` or `$49.99 tax bc`, shows an instant GST/HST/PST
breakdown and total with a one-click copy action. Computed locally from
the standard published rates -- no network request. General rates only;
some goods and services are zero-rated or exempt, so treat it as an
estimate.

Note: DNS-over-HTTPS is pointed at
[CIRA Canadian Shield](https://www.cira.ca/en/canadian-shield/) (Protected
tier), run by the non-profit that operates the `.ca` registry, so DNS
lookups stay on Canadian infrastructure and known malware/phishing domains
are blocked at the DNS layer. Firefox falls back to the system resolver if
it can't be reached, so captive portals still work. A "Sovereign Privacy"
checkbox in Settings → CanadaFox turns it off (reverting to plain system
DNS) without needing to know it's implemented as a policy; it applies
immediately, no restart.

Note: the site-information panel (click the padlock) shows which country
answered the connection, e.g. *Served from Canada*. The lookup is entirely
offline, against a database bundled in the app — no request is made to
produce it. It describes the **responding server**, not where a company
stores your data or which law applies: a foreign site behind a CDN commonly
answers from a Canadian edge node. Data from
[DB-IP](https://db-ip.com) under CC BY 4.0; see `vendor/geoip/README.md`.

Note: genuine network errors (page not found, connection refused, offline —
not certificate/security warnings) show a short blurb from a real Historica
Canada Heritage Minute, e.g. Naismith inventing basketball or Wilder
Penfield's "burnt toast." Wired into both of Firefox's error-page rendering
paths, since a very recent Nightly refresh replaces the classic one for most
error types.

Note: once per session, CanadaFox checks
`github.com/Binhex-Canada/canadafox`'s latest release and shows a
dismissible notification if a newer version exists — no auto-download or
install, just a link to go grab it. This is the one intentional network
call this project adds on top of Safe Browsing; unlike everything else
it strips out, it only ever talks to this project's own GitHub repo.