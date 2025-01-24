import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        page.wait_for_selector('text=SVJIS2')
        page.screenshot(path='playwright_output/home-page1.png')
        page.fill('[id=login-input]', 'peter')
        # page.fill('[id=password-input]', self.u_peter_password)
        page.screenshot(path='playwright_output/home-page2.png')
        page.click('id=login-submit')
        page.screenshot(path='playwright_output/home-page3.png')
        page.close()
