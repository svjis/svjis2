import os
from . import commands as cmd
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from playwright.sync_api import sync_playwright
from ..utils import generate_password


class DesktopTests(StaticLiveServerTestCase):

    size_x = 1280
    size_y = 720

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.test_output_dir = 'playwright_output'
        cls.user_password = generate_password(6)
        call_command('svjis_setup', password=cls.user_password)
        cls.numbering = cmd.get_number()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_all(self):
        context = self.browser.new_context(
            viewport={"width": self.size_x, "height": self.size_y}, device_scale_factor=2
        )
        page = context.new_page()
        cmd.login(self, page, 'admin', self.user_password)
        cmd.fill_company(self, page)
        cmd.logout(self, page)
        page.close()
