# Vendored IP-to-country database

`dbip-country.bin` is a repacked copy of **DB-IP IP to Country Lite**.

| | |
|---|---|
| Source | <https://db-ip.com/db/download/ip-to-country-lite> |
| Author | DB-IP (db-ip.com) |
| License | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) |
| Snapshot | 2026-07 |

CC BY 4.0 requires attribution, which CanadaFox gives in the Settings →
CanadaFox pane and here. The data itself is unmodified: `scripts/build-geoip-db.py`
only repacks the published CSV into a compact binary (sorted range starts plus
a country index) so the browser can binary-search it without parsing 29 MB of
text at runtime. No ranges are added, removed, or altered.

## Refreshing it

DB-IP publishes a new snapshot monthly:

```bash
scripts/build-geoip-db.py 2026-08          # download that month directly
scripts/build-geoip-db.py path/to/dbip.csv # or repack a CSV you already have
```

Then rebuild. The file is copied into the Firefox tree by
`scripts/apply-patches.sh`, the same way the vendored extension xpis are — it
is a binary asset, so it is not carried as a text patch.

## What it is used for

The "Served from" line in the site-information panel (click the padlock).
It reports the country of the server that answered the connection, which is
**not** a statement about where a company stores your data or which
jurisdiction governs it — a US site behind a CDN often answers from a
Canadian edge node, and a Canadian site may be hosted abroad.
