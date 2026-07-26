# Patches

Plain `git diff` output files, generated from inside `firefox/` and applied
in filename order by `scripts/apply-patches.sh`. Numbered by area so ordering
and intent stay obvious:

- `00xx-telemetry-*.patch` — Glean/Telemetry, data-reporting service, ping
  uploaders
- `01xx-experiments-*.patch` — Normandy/Shield/Nimbus remote experiments
- `02xx-tracking-*.patch` — default-on network calls to Mozilla/partner
  services not required for core browsing (Pocket, sponsored tiles, etc.)
- `03xx-prefs-*.patch` — `browser/app/profile/firefox.js` default overrides

To create a new patch:

```bash
cd firefox
# make your change
git diff > ../patches/00xx-short-name.patch
```
