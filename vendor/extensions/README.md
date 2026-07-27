# Vendored extensions

Binary `.xpi` files bundled with CanadaFox as pre-installed, default
extensions. These are **unmodified, Mozilla-signed builds downloaded
directly from [addons.mozilla.org](https://addons.mozilla.org/)** — not
authored, modified, or repackaged by this project. They retain their own
name, icon, version, authorship, and license exactly as published. CanadaFox
does not claim ownership of, or sell, any of them.

They're installed via Firefox's own distribution-extensions mechanism
(`browser/app/distribution/extensions/`, wired up in
`patches/1201-bundle-ublock-origin.patch`), the same path any distributor
uses to pre-install an extension. Once installed, they behave exactly like
an extension the user installed themselves from AMO: they show up in
`about:addons`, update automatically through Mozilla's normal add-on update
service, and can be disabled or removed by the user at any time.

## uBlock Origin

| | |
|---|---|
| File | `uBlock0@raymondhill.net.xpi` |
| Upstream | [addons.mozilla.org/firefox/addon/ublock-origin](https://addons.mozilla.org/firefox/addon/ublock-origin/) |
| Source | [github.com/gorhill/uBlock](https://github.com/gorhill/uBlock) |
| Author | Raymond Hill & contributors |
| License | GNU GPL v3.0 (full text bundled inside the xpi as `LICENSE.txt`) |
| Vendored version | `1.72.2` |

### Updating

```bash
curl -sL "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi" \
  -o vendor/extensions/uBlock0@raymondhill.net.xpi
```

Then update the "Vendored version" line above to match (check the new
file's `manifest.json` `version` field, or the AMO listing) and rebuild.
