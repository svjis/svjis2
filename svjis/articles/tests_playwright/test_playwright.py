import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from ..utils import generate_password
from playwright.sync_api import sync_playwright


def get_number():
    n = 0
    while True:
        n += 1
        yield n


class PlaywrightTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.test_output_dir = 'playwright_output'
        cls.user_password = generate_password(6)
        call_command('svjis_setup', password=cls.user_password)
        cls.numbering = get_number()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def get_filename(self, name):
        return f'{self.test_output_dir}/{next(self.numbering):04}-{name}.png'

    def test_all(self):
        page = self.browser.new_page()
        self.login(page, 'admin', self.user_password)
        self.fill_company(page)
        self.logout(page)
        page.close()

    def logout(self, page):
        page.goto(f"{self.live_server_url}/")
        page.wait_for_selector('id=logout-submit')
        page.click('id=logout-submit')
        page.screenshot(path=self.get_filename('logout'))

    def login(self, page, user, password):
        page.goto(f"{self.live_server_url}/")
        page.wait_for_selector('id=login-submit')
        page.screenshot(path=self.get_filename(f'login-{user}'))
        page.fill('[id=login-input]', user)
        page.fill('[id=password-input]', password)
        page.screenshot(path=self.get_filename(f'login-{user}'))
        page.click('id=login-submit')
        page.screenshot(path=self.get_filename(f'login-{user}'))

    def fill_company(self, page):
        page.click('text=Administration')
        page.screenshot(path=self.get_filename('admin-company'))
        page.fill('[id=id_name]', 'My SVJ')
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        page.screenshot(path=self.get_filename('admin-company'))
