from django.test import TestCase
from django.urls import reverse
from .. import (
    views,
    views_contact,
    views_personal_settings,
    views_redaction,
    views_faults,
    views_adverts,
    views_admin,
)

from .testdata import ArticleDataMixin


class MenuTest(ArticleDataMixin, TestCase):

    def do_menu_test(self, username, password, menu_list):
        menu = [
            {'item': 'Articles', 'link': reverse(views.main_view)},
            {'item': 'Contact', 'link': reverse(views_contact.contact_view)},
            {'item': 'Personal settings', 'link': reverse(views_personal_settings.personal_settings_edit_view)},
            {'item': 'Redaction', 'link': reverse(views_redaction.redaction_article_view)},
            {'item': 'Fault reporting', 'link': reverse(views_faults.faults_list_view) + '?scope=open'},
            {'item': 'Adverts', 'link': reverse(views_adverts.adverts_list_view) + '?scope=all'},
            {'item': 'Administration', 'link': reverse(views_admin.admin_company_edit_view)},
        ]
        # Login user
        if username == 'anonymous':
            self.client.logout()
        else:
            logged_in = self.client.login(username=username, password=password)
            self.assertTrue(logged_in)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(
            [m['description'] for m in res_tray_menu],
            menu_list,
        )

        # Menu access
        for m in menu:
            response = self.client.get(m['link'])
            r = 200 if m['item'] in menu_list else 302
            self.assertEqual(response.status_code, r)

    def test_admin_user(self):
        self.do_menu_test(
            'jarda',
            'jarda',
            ['Articles', 'Contact', 'Personal settings', 'Redaction', 'Fault reporting', 'Administration'],
        )

    def test_board_user(self):
        self.do_menu_test('jiri', 'jiri', ['Articles', 'Contact', 'Personal settings', 'Redaction', 'Fault reporting'])

    def test_owner_user(self):
        self.do_menu_test('petr', 'petr', ['Articles', 'Contact', 'Personal settings', 'Fault reporting'])

    def test_vendor_user(self):
        self.do_menu_test('karel', 'karel', ['Articles', 'Contact', 'Personal settings', 'Fault reporting'])

    def test_anonymous_user(self):
        self.do_menu_test('anonymous', '', ['Articles', 'Contact'])
