import pathlib, re, unittest
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]

class TestSignalCorridor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def page(self,w=1440,h=900,reduced=None):
        p=self.browser.new_page(viewport={'width':w,'height':h}, reduced_motion=reduced or 'no-preference')
        html=(ROOT/'index.html').read_text()
        p.set_content(html, wait_until='load')
        p.wait_for_timeout(100)
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
            p.wait_for_timeout(100)
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

    def test_signal_canvas_and_static_semantics(self):
        p=self.page()
        try:
            self.assertTrue(p.locator('#signalField').is_visible())
            self.assertGreater(p.locator('#signalField').evaluate('el=>el.width'),1000)
        finally:
            p.close()

        p=self.page(768,1024)
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
            self.assertEqual(p.locator('.scene-nav').evaluate('el=>getComputedStyle(el).display'),'none')
        finally:
            p.close()

    def test_visual_scale_alignment_and_narrow_phone(self):
        p=self.page()
        try:
            hero=p.locator('#heroTitle')
            self.assertEqual(hero.locator('.hero-line').count(),3)
            metrics=hero.evaluate("el=>({font:parseFloat(getComputedStyle(el).fontSize),h:el.getBoundingClientRect().height})")
            self.assertLessEqual(metrics['font'],70)
            self.assertLessEqual(metrics['h'],200)
            copy=p.locator('.hero-copy').bounding_box()
            stack=p.locator('.source-stack').bounding_box()
            self.assertLess(copy['x']+copy['width'], stack['x']+8)

            proof=p.locator('.evidence-axis article').evaluate_all("els=>els.map(e=>e.getBoundingClientRect()).map(r=>({x:r.x,y:r.y,w:r.width,h:r.height}))")
            self.assertEqual(len(proof),4)
            self.assertLess(max(r['y'] for r in proof)-min(r['y'] for r in proof),2)
            self.assertLess(max(r['w'] for r in proof)-min(r['w'] for r in proof),2)

            phases=p.locator('.milestones article').evaluate_all("els=>els.map(e=>e.getBoundingClientRect()).map(r=>({x:r.x,y:r.y,w:r.width,h:r.height}))")
            self.assertEqual(len(phases),3)
            self.assertLess(max(r['y'] for r in phases)-min(r['y'] for r in phases),2)
        finally:
            p.close()

        p=self.page(320,800)
        try:
            overflow=p.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
            self.assertEqual(overflow,0)
            hero=p.locator('#heroTitle').evaluate("el=>({h:el.getBoundingClientRect().height,font:parseFloat(getComputedStyle(el).fontSize)})")
            self.assertLessEqual(hero['h'],130)
            self.assertLessEqual(hero['font'],44)
        finally:
            p.close()

if __name__=='__main__':
    unittest.main(verbosity=2)
