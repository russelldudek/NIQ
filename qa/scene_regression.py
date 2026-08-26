import pathlib, re, unittest
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]

class TestSignalCorridor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def page(self,w=1440,h=900,reduced=None):
        p=self.browser.new_page(viewport={'width':w,'height':h}, reduced_motion=reduced or 'no-preference')
        html=(ROOT/'index.html').read_text()
        p.set_content(html, wait_until='load')
        p.wait_for_timeout(80)
        return p

    def test_scene_count_copy_and_no_fake_percentages(self):
        p=self.page()
        try:
            self.assertEqual(p.locator('.scene').count(),8)
            self.assertEqual(p.locator('.scene-nav button').count(),8)
            self.assertIn('pressure-test the model',p.locator('.primary-cta').inner_text().lower())
            self.assertIn('Protect the knowledge. Change the mechanism.',p.locator('.empathy-close strong').inner_text())
            self.assertNotRegex(p.locator('.source-roles').inner_text(),r'\b\d+%')
        finally:
            p.close()

    def test_scenario_atomic_state(self):
        p=self.page()
        try:
            m=p.evaluate("() => ({max:document.documentElement.scrollHeight-innerHeight,count:document.querySelectorAll('.scene').length})")
            p.evaluate('y=>scrollTo(0,y)', 3/(m['count']-1)*m['max'])
            p.wait_for_timeout(120)
            p.locator('[data-scenario="digital"]').click()
            p.wait_for_timeout(600)
            self.assertEqual(p.locator('[data-scenario="digital"]').get_attribute('aria-pressed'),'true')
            self.assertEqual(p.locator('.source-role[data-key="retailer"] b').inner_text(),'PRIMARY')
            self.assertEqual(p.locator('.source-role[data-key="field"] b').inner_text(),'EXCEPTION')
            self.assertIn('Shift recurring capture toward digital',p.locator('#postureTitle').inner_text())
            self.assertIn('Feeds + passive capture + QA',p.locator('#automateFocus').inner_text())
            self.assertIn('Completeness + schema resilience',p.locator('#proofFocus').inner_text())
        finally:
            p.close()

    def test_depth_blur_and_snap(self):
        p=self.page()
        try:
            m=p.evaluate("() => ({max:document.documentElement.scrollHeight-innerHeight,count:document.querySelectorAll('.scene').length})")
            exact=2/(m['count']-1)*m['max']
            p.evaluate('y=>scrollTo(0,y)',exact)
            p.wait_for_timeout(120)
            self.assertIn('blur(0',p.locator('#scene-2').evaluate('el=>el.style.filter'))
            mid=(2.42/(m['count']-1))*m['max']
            p.evaluate('y=>scrollTo(0,y)',mid)
            p.wait_for_timeout(120)
            f=p.locator('#scene-2').evaluate('el=>el.style.filter')
            val=float(re.search(r'blur\(([\d.]+)px\)',f).group(1))
            self.assertGreater(val,.5)
            p.wait_for_timeout(1300)
            target=round(mid/m['max']*(m['count']-1))/(m['count']-1)*m['max']
            self.assertLess(abs(p.evaluate('scrollY')-target),5)
        finally:
            p.close()

    def test_signal_canvas_and_mobile_static_semantics(self):
        p=self.page()
        try:
            self.assertTrue(p.locator('#signalField').is_visible())
            self.assertGreater(p.locator('#signalField').evaluate('el=>el.width'),1000)
        finally:
            p.close()

        p=self.page(390,844)
        try:
            vals=p.locator('.scene').evaluate_all("els=>els.map(el=>getComputedStyle(el).filter)")
            self.assertTrue(all(v=='none' for v in vals),vals)
            self.assertEqual(p.locator('.scene-nav').evaluate('el=>getComputedStyle(el).display'),'none')
        finally:
            p.close()

        p=self.page(1440,900,'reduce')
        try:
            vals=p.locator('.scene').evaluate_all("els=>els.map(el=>getComputedStyle(el).filter)")
            self.assertTrue(all(v=='none' for v in vals),vals)
        finally:
            p.close()

if __name__=='__main__':
    unittest.main(verbosity=2)
