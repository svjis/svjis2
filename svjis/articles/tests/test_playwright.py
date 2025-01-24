import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from ..utils import generate_password
from playwright.sync_api import sync_playwright


class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.test_output_dir = 'playwright_output'
        cls.user_password = generate_password(6)
        call_command('svjis_setup', password=cls.user_password)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        page.wait_for_selector('text=SVJIS2')
        page.screenshot(path=f'{self.test_output_dir}/home-page-01.png')
        page.fill('[id=login-input]', 'admin')
        page.fill('[id=password-input]', self.user_password)
        page.screenshot(path=f'{self.test_output_dir}/home-page-02.png')
        page.click('id=login-submit')
        page.screenshot(path=f'{self.test_output_dir}/home-page-03.png')
        page.close()
