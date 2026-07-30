# README images

| File | What it is |
|---|---|
| `canada-flag.svg` | Vector source, 9600 × 4800 user units (the flag's official 2:1 ratio) |
| `canada-flag-4k.png` | 3840 × 1920 render of that SVG, used as the banner in the top-level README |

The artwork is the national flag of Canada, taken from
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Flag_of_Canada.svg),
where it is published in the public domain. The design is a national symbol
rather than a copyrighted work, so it carries no redistribution conditions —
unlike the other vendored assets in `vendor/`, which do and are documented
there.

## Regenerating the PNG

```bash
rsvg-convert -w 3840 -h 1920 -o docs/images/canada-flag-4k.png docs/images/canada-flag.svg
```

`rsvg-convert` comes from `librsvg` (`brew install librsvg`). Flat colour
regions compress extremely well, so the 4K PNG is only ~71 KB — keeping the
SVG alongside it means any other size can be produced losslessly.
