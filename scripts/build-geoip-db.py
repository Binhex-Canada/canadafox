#!/usr/bin/env python3
"""Rebuild vendor/geoip/dbip-country.bin from DB-IP's IP-to-Country Lite CSV.

The CSV is ~29 MB of text; this packs it into a compact binary of sorted
range starts plus a country index, which the browser binary-searches at
runtime. Country *names* are not stored -- Intl.DisplayNames turns the
two-letter code into a localized name.

Usage:  scripts/build-geoip-db.py [YYYY-MM | path/to/dbip.csv]
"""
import gzip
import ipaddress
import struct
import sys
import urllib.request
from pathlib import Path

MAGIC = b"CFGEO1\0\0"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "vendor" / "geoip" / "dbip-country.bin"


def fetch(source):
    """`source` is either a YYYY-MM tag to download, or a path to a local
    .csv/.csv.gz already fetched."""
    path = Path(source)
    if path.exists():
        print(f"reading {path}")
        raw = path.read_bytes()
        if path.suffix == ".gz":
            raw = gzip.decompress(raw)
        return raw.decode("utf-8")

    url = f"https://download.db-ip.com/free/dbip-country-lite-{source}.csv.gz"
    print(f"downloading {url}")
    # db-ip.com rejects the default urllib agent.
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return gzip.decompress(r.read()).decode("utf-8")


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else None
    if not source:
        from datetime import date

        source = date.today().strftime("%Y-%m")

    v4, v6, countries = [], [], {}

    def idx(code):
        return countries.setdefault(code, len(countries))

    for line in fetch(source).splitlines():
        if not line:
            continue
        start, _end, code = line.split(",")
        if ":" in start:
            packed = int(ipaddress.IPv6Address(start)) >> 64
            v6.append((packed, idx(code)))
        else:
            v4.append((int(ipaddress.IPv4Address(start)), idx(code)))

    v4.sort()
    v6.sort()
    if len(countries) > 255:
        raise SystemExit(f"too many countries for a uint8 index: {len(countries)}")

    codes = sorted(countries, key=countries.get)
    out = bytearray(MAGIC)
    out += struct.pack("<I", len(codes))
    for c in codes:
        out += c.encode("ascii").ljust(2, b"\0")[:2]

    # Pad so the following arrays land on an 8-byte boundary.
    while len(out) % 8:
        out += b"\0"

    out += struct.pack("<I", len(v4))
    out += b"\0" * 4
    out += b"".join(struct.pack("<I", s) for s, _ in v4)
    out += bytes(c for _, c in v4)
    while len(out) % 8:
        out += b"\0"

    out += struct.pack("<I", len(v6))
    out += b"\0" * 4
    out += b"".join(struct.pack("<Q", s) for s, _ in v6)
    out += bytes(c for _, c in v6)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(out)
    print(
        f"wrote {OUT} -- {len(v4)} IPv4 + {len(v6)} IPv6 ranges, "
        f"{len(codes)} countries, {len(out) / 1024 / 1024:.2f} MB"
    )


if __name__ == "__main__":
    main()
