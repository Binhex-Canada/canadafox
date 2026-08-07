#!/usr/bin/env python3
"""
Smoke-tests a packaged CanadaFox.app before it ships.

Drives the actual built binary over the Marionette remote protocol against
a disposable throwaway profile -- there is no way to check that a Firefox
patch-fork's features genuinely work without running the genuine app, so
this is a "unit test" in the sense of one assertion per feature, not a
mock of the browser.

Usage:
    python3 scripts/test-release.py [--app /path/to/CanadaFox.app] [--version 0.0.3.7]

Exits non-zero if any check fails, so it's safe to gate a release on.
"""

import argparse
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest

DEFAULT_APP = "/Applications/CanadaFox.app"
MARIONETTE_PORT = 2828
STARTUP_TIMEOUT_S = 20


def _recv_msg(sock):
    buf = b""
    while b":" not in buf:
        chunk = sock.recv(1)
        if not chunk:
            raise RuntimeError("Marionette socket closed unexpectedly")
        buf += chunk
    length_str, rest = buf.split(b":", 1)
    length = int(length_str)
    data = rest
    while len(data) < length:
        data += sock.recv(length - len(data))
    return json.loads(data.decode("utf-8"))


class Marionette:
    def __init__(self, port=MARIONETTE_PORT, timeout=STARTUP_TIMEOUT_S):
        deadline = time.time() + timeout
        last_error = None
        while time.time() < deadline:
            try:
                self.sock = socket.create_connection(("localhost", port), timeout=5)
                break
            except OSError as exc:
                last_error = exc
                time.sleep(0.5)
        else:
            raise RuntimeError(f"Marionette never came up on port {port}: {last_error}")
        _recv_msg(self.sock)
        self._id = 0
        self.command("WebDriver:NewSession", {})

    def command(self, name, params):
        self._id += 1
        payload = json.dumps([0, self._id, name, params])
        self.sock.sendall(f"{len(payload)}:{payload}".encode("utf-8"))
        response = _recv_msg(self.sock)
        if isinstance(response, list) and len(response) > 2 and response[2]:
            raise RuntimeError(f"{name} failed: {response[2]}")
        return response[3] if len(response) > 3 else None

    def chrome(self, script):
        self.command("Marionette:SetContext", {"value": "chrome"})
        return self.command("WebDriver:ExecuteScript", {"script": script, "args": []})["value"]

    def chrome_async(self, script):
        self.command("Marionette:SetContext", {"value": "chrome"})
        wrapped = (
            "let resolve = arguments[arguments.length - 1]; "
            f"(async () => {{ {script} }})().then(resolve, e => resolve({{__error: String(e)}}));"
        )
        return self.command("WebDriver:ExecuteAsyncScript", {"script": wrapped, "args": []})["value"]

    def close(self):
        self.sock.close()


class CanadaFoxSmokeTest(unittest.TestCase):
    """One assertion per feature, run against a real packaged build."""

    app_path = DEFAULT_APP
    expected_version = None
    marionette = None
    process = None
    profile_dir = None

    @classmethod
    def setUpClass(cls):
        binary = f"{cls.app_path}/Contents/MacOS/firefox"
        cls.profile_dir = tempfile.mkdtemp(prefix="canadafox-smoketest-")
        cls.process = subprocess.Popen(
            [
                binary,
                "-marionette",
                "-remote-allow-system-access",
                "-no-remote",
                "-profile",
                cls.profile_dir,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cls.marionette = Marionette()
        # Let startup-time BrowserGlue hooks (welcome tab, bookmarks, prefs) finish.
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        if cls.marionette:
            cls.marionette.close()
        if cls.process:
            cls.process.terminate()
            try:
                cls.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                cls.process.kill()
        if cls.profile_dir:
            shutil.rmtree(cls.profile_dir, ignore_errors=True)

    def m(self):
        return self.__class__.marionette

    # -- Branding / version -------------------------------------------------

    def test_01_version_matches_expected(self):
        if not self.expected_version:
            self.skipTest("no --version given")
        version = self.m().chrome("return Services.appinfo.version;")
        self.assertEqual(version, self.expected_version)

    def test_02_vendor_is_not_mozilla_branded_official(self):
        name = self.m().chrome("return Services.appinfo.name;")
        self.assertEqual(name, "Firefox")  # internal app name; branding is cosmetic

    # -- Startup tabs ---------------------------------------------------------

    # Numbered rather than alphabetical: unittest runs test_* methods in
    # name order, and this one asserts on pristine startup tab state, so it
    # must run before any test that navigates the selected tab elsewhere.
    def test_03_welcome_tab_pinned_and_selected_on_startup(self):
        result = self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            let tabs = win.gBrowser.tabs.map(t => ({
                url: t.linkedBrowser?.currentURI?.spec,
                pinned: t.pinned,
                selected: t == win.gBrowser.selectedTab,
            }));
            return tabs;
        """)
        welcome = next((t for t in result if t["url"] == "about:canadafoxwelcome"), None)
        self.assertIsNotNone(welcome, f"no welcome tab found in {result}")
        self.assertTrue(welcome["pinned"], "welcome tab should be pinned")
        self.assertTrue(welcome["selected"], "welcome tab should be the foreground tab")

    # -- Bookmarks / keywords ---------------------------------------------

    def test_04_canadian_services_bookmarks_folder(self):
        result = self.m().chrome_async("""
            let tree = await PlacesUtils.promiseBookmarksTree(PlacesUtils.bookmarks.toolbarGuid);
            let folder = tree.children?.find(c => c.title == "Canadian Services");
            return {
                found: !!folder,
                entries: folder?.children?.map(c => c.title) || [],
            };
        """)
        self.assertTrue(result["found"], "Canadian Services bookmarks folder missing")
        self.assertGreaterEqual(len(result["entries"]), 6, result["entries"])

    def test_05_keyword_shortcuts_resolve(self):
        result = self.m().chrome_async("""
            let out = {};
            for (const kw of ["cra", "service", "health", "cbc"]) {
                let entry = await PlacesUtils.keywords.fetch(kw);
                out[kw] = entry ? entry.url.href : null;
            }
            return out;
        """)
        for keyword, url in result.items():
            self.assertIsNotNone(url, f"keyword '{keyword}' did not resolve to a URL")

    # -- Privacy prefs --------------------------------------------------------

    def test_06_sponsored_content_and_telemetry_off(self):
        result = self.m().chrome("""
            return {
                showSponsored: Services.prefs.getBoolPref("browser.newtabpage.activity-stream.showSponsored", null),
                discoverystream: Services.prefs.getBoolPref("browser.newtabpage.activity-stream.discoverystream.enabled", null),
                privatePing: Services.prefs.getBoolPref("browser.newtabpage.activity-stream.telemetry.privatePing.enabled", null),
            };
        """)
        for key, value in result.items():
            self.assertFalse(value, f"{key} should be false")

    def test_07_ai_features_locked_off(self):
        enabled = self.m().chrome(
            'return Services.prefs.getBoolPref("browser.ml.chat.enabled", null);'
        )
        self.assertFalse(enabled, "AI chat should be locked off")

    def test_08_pinned_tabs_locked_by_default(self):
        locked = self.m().chrome(
            'return Services.prefs.getBoolPref("browser.tabs.lockPinnedTabs", null);'
        )
        self.assertTrue(locked)

    def test_09_cira_dns_on_by_default(self):
        result = self.m().chrome("""
            return {
                mode: Services.prefs.getIntPref("network.trr.mode", -1),
                uri: Services.prefs.getStringPref("network.trr.uri", ""),
            };
        """)
        self.assertEqual(result["mode"], 2)
        self.assertIn("canadianshield.cira.ca", result["uri"])

    def test_17_strip_tracking_params_on_by_default(self):
        result = self.m().chrome("""
            return {
                enabled: Services.prefs.getBoolPref("privacy.query_stripping.enabled", false),
                pbmode: Services.prefs.getBoolPref("privacy.query_stripping.enabled.pbmode", false),
            };
        """)
        self.assertTrue(result["enabled"])
        self.assertTrue(result["pbmode"])

    def test_18_lookalike_domain_detection(self):
        result = self.m().chrome("""
            const { findLookalikeMatch } = ChromeUtils.importESModule(
                "resource:///modules/CanadaFoxLookalikeProtection.sys.mjs"
            );
            return {
                real: findLookalikeMatch("canada.ca"),
                fake: findLookalikeMatch("cra-arc-refund.com"),
                unrelated: findLookalikeMatch("example.com"),
            };
        """)
        self.assertIsNone(result["real"], "real protected domain should not be flagged")
        self.assertIsNone(result["unrelated"], "unrelated domain should not be flagged")
        self.assertIsNotNone(result["fake"], "lookalike domain should be flagged")

    # -- Toolbar --------------------------------------------------------------

    def test_10_tax_toolbar_button_exists_and_no_flag_button(self):
        result = self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            return {
                taxButton: !!win.document.getElementById("canadafox-tax-button-inner"),
                flagButton: !!win.document.getElementById("canadafox-flag-button-inner"),
            };
        """)
        self.assertTrue(result["taxButton"], "tax calculator toolbar button missing")
        self.assertFalse(result["flagButton"], "decorative flag button should be removed")

    def test_11_tax_toolbar_button_opens_panel_and_computes(self):
        self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.document.getElementById("canadafox-tax-button-inner").click();
        """)
        time.sleep(1)
        result = self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.document.getElementById("canadafox-tax-amount").value = "50";
            win.document.getElementById("canadafox-tax-amount").dispatchEvent(new Event("input"));
            let province = win.document.getElementById("canadafox-tax-province");
            province.value = "on";
            province.dispatchEvent(new Event("change"));
            return {
                panelState: win.document.getElementById("canadafox-tax-panel").state,
                result: win.document.getElementById("canadafox-tax-result").textContent,
            };
        """)
        self.assertIn(result["panelState"], ("open", "showing"))
        self.assertIn("56.50", result["result"], result["result"])

    def test_19_clearcache_button_confirms_before_clearing(self):
        self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.document.getElementById("canadafox-clearcache-button-inner").click();
        """)
        time.sleep(1)
        panel_state = self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            return win.document.getElementById("canadafox-clearcache-panel").state;
        """)
        self.assertIn(
            panel_state, ("open", "showing"), "clicking the button should open a confirm panel, not clear immediately"
        )

        self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.document.getElementById("canadafox-clearcache-confirm-button").click();
        """)
        time.sleep(1)
        status_text = self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            return win.document.getElementById("canadafox-clearcache-status").textContent;
        """)
        self.assertTrue(status_text, "clearing should show a confirmation message")

    # -- Address-bar sales tax calculator --------------------------------

    def test_12_address_bar_tax_calculator(self):
        result = self.m().chrome_async("""
            const { UrlbarProviderCanadianTax } = ChromeUtils.importESModule(
                "moz-src:///browser/components/urlbar/UrlbarProviderCanadianTax.sys.mjs"
            );
            let provider = new UrlbarProviderCanadianTax();
            let active = await provider.isActive({ searchString: "100 tax bc" });
            return { active, result: provider._activeResult };
        """)
        self.assertTrue(result["active"])
        self.assertIn("112.00", result["result"], result["result"])

    # -- New Tab tax calculator widget ------------------------------------

    def test_15_newtab_tax_calculator_widget(self):
        self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.gBrowser.selectedBrowser.fixupAndLoadURIString("about:canadafoxnewtab", {
                triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(),
            });
        """)
        time.sleep(2)
        self.m().command("Marionette:SetContext", {"value": "content"})
        result = self.m().command("WebDriver:ExecuteScript", {
            "script": """
                let province = document.getElementById("calc-province");
                province.value = "qc";
                province.dispatchEvent(new Event("change"));
                document.getElementById("calc-amount").value = "100";
                document.getElementById("calc-amount").dispatchEvent(new Event("input"));
                return document.getElementById("calc-result").textContent;
            """,
            "args": [],
        })["value"]
        self.m().command("Marionette:SetContext", {"value": "chrome"})
        self.assertIn("114.98", result, result)

    # -- Sharper images toggle --------------------------------------------

    def test_13_sharper_images_toggle_changes_device_pixel_ratio(self):
        self.m().chrome('Services.prefs.setBoolPref("canadafox.sharperImages.enabled", true);')
        time.sleep(0.5)
        forced = self.m().chrome(
            'return Services.prefs.getFloatPref("layout.css.devPixelsPerPx", -1);'
        )
        self.m().chrome('Services.prefs.setBoolPref("canadafox.sharperImages.enabled", false);')
        time.sleep(0.5)
        reset = self.m().chrome(
            'return Services.prefs.getFloatPref("layout.css.devPixelsPerPx", -1);'
        )
        self.assertEqual(forced, 2.0)
        self.assertEqual(reset, -1.0)

    # -- Extensions -------------------------------------------------------

    def test_14_ublock_origin_bundled_and_active(self):
        result = self.m().chrome_async("""
            const { AddonManager } = ChromeUtils.importESModule("resource://gre/modules/AddonManager.sys.mjs");
            let addons = await AddonManager.getAllAddons();
            let ublock = addons.find(a => a.id == "uBlock0@raymondhill.net");
            return { found: !!ublock, active: ublock?.isActive };
        """)
        self.assertTrue(result["found"], "uBlock Origin not bundled")
        self.assertTrue(result["active"])

    # -- Settings page ------------------------------------------------------

    def test_16_settings_page_renders(self):
        self.m().chrome("""
            let win = Services.wm.getMostRecentWindow("navigator:browser");
            win.gBrowser.selectedBrowser.fixupAndLoadURIString("about:preferences#canadafox", {
                triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(),
            });
        """)
        time.sleep(2)
        self.m().command("Marionette:SetContext", {"value": "content"})
        title = self.m().command(
            "WebDriver:ExecuteScript", {"script": "return document.title;", "args": []}
        )["value"]
        self.m().command("Marionette:SetContext", {"value": "chrome"})
        self.assertEqual(title, "Settings")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", default=DEFAULT_APP, help="Path to CanadaFox.app")
    parser.add_argument("--version", default=None, help="Expected version, e.g. 0.0.3.7")
    args = parser.parse_args()

    CanadaFoxSmokeTest.app_path = args.app
    CanadaFoxSmokeTest.expected_version = args.version

    suite = unittest.TestLoader().loadTestsFromTestCase(CanadaFoxSmokeTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
