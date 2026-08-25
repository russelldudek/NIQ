from pathlib import Path
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def bundled_html():
    html = (ROOT / "index.html").read_text()
    brand = (ROOT / "brand-tokens.css").read_text()
    styles = (ROOT / "styles.css").read_text()
    closing = (ROOT / "closing.css").read_text()
    app = (ROOT / "app.js").read_text()
    html = html.replace('<link rel="stylesheet" href="brand-tokens.css">', f'<style>{brand}</style>')
    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{styles}</style>')
    html = html.replace('<link rel="stylesheet" href="closing.css">', f'<style>{closing}</style>')
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

    def desktop_page(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        page.set_content(self.html, wait_until="load")
        return page

    def test_closing_hero_is_eighth_scene(self):
        page = self.desktop_page()
        try:
            self.assertEqual(page.locator(".scene").count(), 8)
            self.assertEqual(page.locator(".scene-nav [data-jump]").count(), 8)
            final = page.locator("#scene-7")
            self.assertEqual(final.count(), 1)
            self.assertIn("The Full View starts at the source", final.inner_text())
            self.assertIn("help NIQ build what comes next", final.inner_text())
            self.assertEqual(final.locator('a[href^="mailto:"]').count(), 1)
            self.assertEqual(final.locator('a[href*="linkedin.com/in/russelldudek"]').count(), 1)
        finally:
            page.close()

    def test_desktop_scroll_idles_then_snaps_to_nearest_scene(self):
        page = self.desktop_page()
        try:
            metrics = page.evaluate("""() => ({
                max: document.documentElement.scrollHeight - innerHeight,
                count: document.querySelectorAll('.scene').length
            })""")
            target_index = 3
            exact = target_index / (metrics["count"] - 1) * metrics["max"]
            offset = exact + metrics["max"] * 0.035
            page.evaluate("y => scrollTo(0, y)", offset)
            page.wait_for_timeout(1500)
            y = page.evaluate("scrollY")
            self.assertLess(abs(y - exact), 4, f"expected snap near {exact}, got {y}")
            current = page.locator('.scene-nav [aria-current="true"]').get_attribute("data-jump")
            self.assertEqual(current, str(target_index))
            settled_filter = page.locator(f"#scene-{target_index}").evaluate("el => el.style.filter")
            self.assertIn("blur(0", settled_filter, f"settled scene should return to sharp focus, got {settled_filter!r}")
        finally:
            page.close()

    def test_user_input_cancels_an_inflight_snap(self):
        page = self.desktop_page()
        try:
            metrics = page.evaluate("""() => ({
                max: document.documentElement.scrollHeight - innerHeight,
                count: document.querySelectorAll('.scene').length
            })""")
            exact = 2 / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", exact + 260)
            page.wait_for_timeout(280)
            manual = exact + 620
            page.evaluate("""y => {
                dispatchEvent(new WheelEvent('wheel', {deltaY: 320, bubbles: true}));
                scrollTo(0, y);
            }""", manual)
            page.wait_for_timeout(80)
            y = page.evaluate("scrollY")
            self.assertLess(abs(y - manual), 8, f"user scroll should hold immediately after cancellation, got {y}")
        finally:
            page.close()

    def test_desktop_depth_of_field_tracks_scene_distance(self):
        page = self.desktop_page()
        try:
            initial_filter = page.locator("#scene-0").evaluate("el => el.style.filter")
            self.assertIn("blur(0", initial_filter, f"opening focal plane should be sharp, got {initial_filter!r}")

            metrics = page.evaluate("""() => ({
                max: document.documentElement.scrollHeight - innerHeight,
                count: document.querySelectorAll('.scene').length
            })""")
            scene_index = 2
            fraction = 0.42
            midpoint = (scene_index + fraction) / (metrics["count"] - 1) * metrics["max"]
            page.evaluate("y => scrollTo(0, y)", midpoint)
            page.wait_for_function("y => Math.abs(scrollY - y) < 2", arg=midpoint)
            page.wait_for_timeout(25)
            page.evaluate("""() => {
                dispatchEvent(new WheelEvent('wheel', {deltaY: 0, bubbles: true}));
                dispatchEvent(new Event('resize'));
            }""")
            page.wait_for_timeout(600)

            departing_filter = page.locator(f"#scene-{scene_index}").evaluate("el => el.style.filter")
            arriving_filter = page.locator(f"#scene-{scene_index + 1}").evaluate("el => el.style.filter")

            import re
            def blur_px(value):
                match = re.search(r"blur\(([-0-9.]+)px\)", value or "")
                self.assertIsNotNone(match, f"expected blur() filter, got {value!r}")
                return float(match.group(1))

            def expected_blur(distance):
                focus_distance = max(0, min(1, (distance - 80) / 620))
                return 8 * (focus_distance ** 1.65)

            departing_expected = expected_blur(fraction * 1120)
            arriving_expected = expected_blur((1 - fraction) * 1120)
            self.assertAlmostEqual(blur_px(departing_filter), departing_expected, delta=0.06)
            self.assertAlmostEqual(blur_px(arriving_filter), arriving_expected, delta=0.06)
            self.assertLessEqual(blur_px(departing_filter), 8.01)
            self.assertLessEqual(blur_px(arriving_filter), 8.01)
        finally:
            page.close()

    def test_mobile_and_reduced_motion_disable_depth_blur(self):
        mobile_page = self.browser.new_page(viewport={"width": 390, "height": 844})
        try:
            mobile_page.set_content(self.html, wait_until="load")
            mobile_page.evaluate("scrollTo(0, 900)")
            mobile_page.wait_for_timeout(60)
            values = mobile_page.locator('.scene').evaluate_all("els => els.map(el => getComputedStyle(el).filter)")
            self.assertTrue(all(value == 'none' for value in values), values)
        finally:
            mobile_page.close()

        reduced_page = self.browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        try:
            reduced_page.set_content(self.html, wait_until="load")
            reduced_page.evaluate("scrollTo(0, 900)")
            reduced_page.wait_for_timeout(60)
            values = reduced_page.locator('.scene').evaluate_all("els => els.map(el => getComputedStyle(el).filter)")
            self.assertTrue(all(value == 'none' for value in values), values)
        finally:
            reduced_page.close()

    def test_reduced_motion_does_not_auto_snap(self):
        page = self.browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        try:
            page.set_content(self.html, wait_until="load")
            page.evaluate("scrollTo(0, 777)")
            page.wait_for_timeout(1200)
            y = page.evaluate("scrollY")
            self.assertLess(abs(y - 777), 4)
        finally:
            page.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
