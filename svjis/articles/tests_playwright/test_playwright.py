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
        cls.browser = cls.playwright.chromium.launch(headless=True)
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
        context = self.browser.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=2)
        page = context.new_page()
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
        page.fill('[id=id_name]', 'Společenství vlastníků domu Práčská 1')
        page.fill('[id=id_address]', 'Práčská 1')
        page.fill('[id=id_city]', 'Praha')
        page.fill('[id=id_post_code]', '102 00')
        page.fill('[id=id_phone]', '+420 111 111')
        page.fill('[id=id_email]', 'pracska@seznam.cz')
        page.fill('[id=id_registration_no]', '123456')
        page.fill('[id=id_vat_registration_no]', 'CZ123456')
        page.fill('[id=id_internet_domain]', 'www.pracska.cz')
        page.set_input_files('[id=id_header_picture]', 'articles/tests_playwright/assets/Header_1.png')
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        page.screenshot(path=self.get_filename('admin-company'))
