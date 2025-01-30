import os
import shutil
import tempfile
from . import commands as cmd
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.conf import settings
from django.test import override_settings
from playwright.sync_api import sync_playwright
from ..utils import generate_password


@override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
class DesktopTests(StaticLiveServerTestCase):

    device_width = 1280
    device_height = 720
    test_output_dir = 'playwright_output/desktop'

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.user_password = generate_password(6)
        call_command('svjis_setup', password=cls.user_password)
        cls.numbering = cmd.get_number()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_all(self):
        context = self.browser.new_context(
            viewport={"width": self.device_width, "height": self.device_height}, device_scale_factor=1
        )
        page = context.new_page()
        # Param
        cmd.login(self, page, 'admin', self.user_password)
        cmd.fill_company(self, page)
        cmd.fill_building(self, page)
        cmd.fill_entrances(self, page)
        cmd.fill_building_units(self, page)
        cmd.fill_users(self, page)
        cmd.fill_board(self, page)
        cmd.fill_user_units(self, page)
        cmd.logout(self, page)
        # Redaction
        cmd.login(self, page, 'petr', self.user_password)
        cmd.create_articles(self, page)
        cmd.logout(self, page)
        cmd.login(self, page, 'jaroslav', self.user_password)
        cmd.create_news(self, page)
        cmd.create_useful_links(self, page)
        cmd.create_survey(self, page)
        cmd.logout(self, page)
        cmd.login(self, page, 'jana', self.user_password)
        cmd.create_comments(self, page)
        cmd.search_for_article(self, page)
        cmd.logout(self, page)
        cmd.vote_survey(self, page)
        page.close()
