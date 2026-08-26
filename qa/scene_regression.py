from pathlib import Path
import re
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def bundled_html():
    html = (ROOT / "index.html").read_text()
    brand = (ROOT / "brand-tokens.css").read_text()
    styles = (ROOT / "styles.css").read_text()
    app = (ROOT / "app.js").read_text()
    html = html.replace('<link rel="stylesheet" href="brand-tokens.css">', f'<style>{brand}</style>')
    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{styles}</style>')
    html = html.replace('<script src="app.js" defer></script>', f'<script>{app}</script>')
    return html


class SceneRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path="/usr/bin/chromium", headless=True)
        cls.html = bundled_html()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def page(self, width=1440, height=900, reduced=False):
        page = self.browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce" if reduced else "no-preference")
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type in ("error", "warning") else None)
        page.set_content(self.html, wait_until="load")
        page._qa_errors = errors
        return page

    def test_eight_scene_argument_and_closing_cta(self):
        page = self.page()
        try:
            self.assertEqual(page.locator(".scene").count(), 8)
            self.assertEqual(page.locator(".scene-nav [data-jump]").count(), 8)
            self.assertEqual(page.locator(".topbar a[href^='mailto:']").count(), 0)
            self.assertIn("The Full View starts at the source", page.locator("#scene-0").inner_text())
            final = page.locator("#scene-7")
            self.assertIn("Would it be a bad idea", final.inner_text())
            self.assertIn("pressure-test the model", final.inner_text().lower())
            cta = final.locator(".final-cta")
            self.assertTrue(cta.get_attribute("href").startswith("mailto:"))
            self.assertIn("NIQ%20source%20portfolio%20discussion", cta.get_attribute("href"))
            self.assertEqual(page._qa_errors, [])
        finally:
            page.close()

    def test_signal_field_exists_and_is_motion_safe(self):
        page = self.page()
        try:
            canvas = page.locator("#signalField")
            self.assertEqual(canvas.count(), 1)
            box = canvas.bounding_box()
            self.assertGreater(box["width"], 1000)
            self.assertGreater(box["height"], 700)
            page.evaluate("scrollTo(0, 950)")
            page.wait_for_timeout(120)
            self.assertGreater(page.evaluate("document.getElementById('signalField').width"), 0)
        finally:
            page.close()

        reduced = self.page(reduced=True)
        try:
            reduced.evaluate("scrollTo(0, 900)")
            reduced.wait_for_timeout(100)
            filters = reduced.locator(".scene").evaluate_all("els => els.map(el => getComputedStyle(el).filter)")
            self.assertTrue(all(v == "none" for v in filters), filters)
            self.assertEqual(reduced._qa_errors, [])
        finally:
            reduced.close()

    def test_qualitative_portfolio_state_updates_atomically_and_resets(self):
        page = self.page()
        try:
            metrics = page.evaluate("""() => ({max: document.documentElement.scrollHeight - innerHeight, count: document.querySelectorAll('.scene').length})""")
            exact = 3 / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", exact)
            page.wait_for_timeout(120)
            page.locator('[data-scenario="digital"]').click()
            page.wait_for_timeout(80)
            self.assertEqual(page.locator('[data-scenario="digital"]').get_attribute("aria-pressed"), "true")
            self.assertEqual(page.locator('[data-scenario="balanced"]').get_attribute("aria-pressed"), "false")
            self.assertIn("digital", page.locator("#postureTitle").inner_text().lower())
            self.assertIn("exceptions", page.locator("#humanAuthority").inner_text().lower())
            self.assertEqual(page.locator('[data-source="retailer"]').get_attribute("data-role"), "primary")
            self.assertEqual(page.locator('[data-source="field"]').get_attribute("data-role"), "exception")
            self.assertNotRegex(page.locator(".portfolio-stage").inner_text(), r"\b\d{1,3}%\b")

            page.locator("#scenarioReset").click()
            page.wait_for_timeout(80)
            self.assertEqual(page.locator('[data-scenario="balanced"]').get_attribute("aria-pressed"), "true")
            self.assertEqual(page.locator('[data-source="field"]').get_attribute("data-role"), "supporting")
            self.assertIn("Augment", page.locator("#postureTitle").inner_text())
        finally:
            page.close()

    def test_desktop_scroll_blurs_then_snaps_to_exact_scene(self):
        page = self.page()
        try:
            metrics = page.evaluate("""() => ({max: document.documentElement.scrollHeight - innerHeight, count: document.querySelectorAll('.scene').length})""")
            index = 2
            exact = index / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", exact)
            page.wait_for_timeout(80)
            sharp = page.locator(f"#scene-{index}").evaluate("el => el.style.filter")
            self.assertIn("blur(0", sharp)

            midpoint = (index + .42) / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", midpoint)
            page.wait_for_timeout(90)
            leaving = page.locator(f"#scene-{index}").evaluate("el => el.style.filter")
            match = re.search(r"blur\(([-0-9.]+)px\)", leaving)
            self.assertIsNotNone(match)
            self.assertGreater(float(match.group(1)), .5)

            offset = exact + metrics["max"] * .035
            page.evaluate("y => scrollTo(0, y)", offset)
            page.wait_for_timeout(1500)
            y = page.evaluate("scrollY")
            self.assertLess(abs(y - exact), 4, f"expected {exact}, got {y}")
            settled = page.locator(f"#scene-{index}").evaluate("el => el.style.filter")
            self.assertIn("blur(0", settled)
        finally:
            page.close()

    def test_user_intent_cancels_inflight_snap(self):
        page = self.page()
        try:
            metrics = page.evaluate("""() => ({max: document.documentElement.scrollHeight - innerHeight, count: document.querySelectorAll('.scene').length})""")
            exact = 3 / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", exact + 280)
            page.wait_for_timeout(300)
            manual = exact + 660
            page.evaluate("""y => { dispatchEvent(new WheelEvent('wheel', {deltaY: 320, bubbles: true})); scrollTo(0, y); }""", manual)
            page.wait_for_timeout(80)
            self.assertLess(abs(page.evaluate("scrollY") - manual), 10)
        finally:
            page.close()

    def test_responsive_matrix_has_no_horizontal_overflow(self):
        for width, height in [(1440,900),(1280,800),(768,1024),(390,844),(320,800)]:
            with self.subTest(viewport=(width,height)):
                page = self.page(width, height)
                try:
                    overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                    self.assertLessEqual(overflow, 1, f"overflow {overflow}px at {width}")
                    self.assertEqual(page._qa_errors, [])
                    if width <= 760:
                        self.assertEqual(page.locator(".scene-nav").evaluate("el => getComputedStyle(el).display"), "none")
                        filters = page.locator(".scene").evaluate_all("els => els.map(el => getComputedStyle(el).filter)")
                        self.assertTrue(all(v == "none" for v in filters), filters)
                finally:
                    page.close()

    def test_reduced_motion_does_not_auto_snap(self):
        page = self.page(reduced=True)
        try:
            page.evaluate("scrollTo(0, 777)")
            page.wait_for_timeout(1200)
            self.assertLess(abs(page.evaluate("scrollY") - 777), 4)
        finally:
            page.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
