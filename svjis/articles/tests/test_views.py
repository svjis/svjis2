from django.test import TestCase
from django.urls import reverse

from .testdata import ArticleDataMixin


class ArticleListTest(ArticleDataMixin, TestCase):

    def test_admin_user(self):
        # Login user
        logged_in = self.client.login(username='jarda', password='jarda')
        self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 200)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 5)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')
        self.assertEqual(res_tray_menu[3]['description'], 'Redaction')
        self.assertEqual(res_tray_menu[4]['description'], 'Administration')

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 4)
        self.assertEqual(res_articles[0].header, 'For Board')
        self.assertEqual(res_articles[1].header, 'For Owners and Board')
        self.assertEqual(res_articles[2].header, 'For Owners')
        self.assertEqual(res_articles[3].header, 'For All')

    def test_board_user(self):
        # Login user
        logged_in = self.client.login(username='jiri', password='jiri')
        self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 200)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 4)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')
        self.assertEqual(res_tray_menu[3]['description'], 'Redaction')

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 4)
        self.assertEqual(res_articles[0].header, 'For Board')
        self.assertEqual(res_articles[1].header, 'For Owners and Board')
        self.assertEqual(res_articles[2].header, 'For Owners')
        self.assertEqual(res_articles[3].header, 'For All')

    def test_owner_user(self):
        # Login user
        logged_in = self.client.login(username='petr', password='petr')
        self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Owners
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_owners.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 404)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 3)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 3)
        self.assertEqual(res_articles[0].header, 'For Owners and Board')
        self.assertEqual(res_articles[1].header, 'For Owners')
        self.assertEqual(res_articles[2].header, 'For All')

    def test_vendor_user(self):
        # Login user
        logged_in = self.client.login(username='karel', password='karel')
        self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Owners
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_owners.slug}))
        self.assertEqual(response.status_code, 404)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 404)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 3)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 1)
        self.assertEqual(res_articles[0].header, 'For All')

    def test_anonymous_user(self):
        # Logout user
        self.client.logout()

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Owners
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_owners.slug}))
        self.assertEqual(response.status_code, 404)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 404)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Menu
        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 2)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 1)
        self.assertEqual(res_articles[0].header, 'For All')

    def test_top_articles(self):
        # Login board user
        logged_in = self.client.login(username='jiri', password='jiri')
        self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, 200)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, 200)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Top Articles
        res_top = response.context['top_articles']
        self.assertEqual(len(res_top), 2)
        self.assertEqual(res_top[0]['article_id'], self.article_for_board.pk)
        self.assertEqual(res_top[0]['total'], 2)
        self.assertEqual(res_top[1]['article_id'], self.article_for_all.pk)
        self.assertEqual(res_top[1]['total'], 1)

        # Login owner user
        logged_in = self.client.login(username='petr', password='petr')
        self.assertTrue(logged_in)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Top Articles
        res_top = response.context['top_articles']
        self.assertEqual(len(res_top), 1)
        self.assertEqual(res_top[0]['article_id'], self.article_for_all.pk)
        self.assertEqual(res_top[0]['total'], 1)

        # Logout user
        self.client.logout()

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # Top Articles
        res_top = response.context['top_articles']
        self.assertEqual(len(res_top), 1)
        self.assertEqual(res_top[0]['article_id'], self.article_for_all.pk)
        self.assertEqual(res_top[0]['total'], 1)

    def test_send_article_notifications(self):
        # Login board user
        logged_in = self.client.login(username='jiri', password='jiri')
        self.assertTrue(logged_in)

        # Send notifications for article not published
        response = self.client.get(
            reverse('redaction_article_notifications', kwargs={'pk': self.article_not_published.pk})
        )
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 0)

        # Send notifications for no one
        response = self.client.get(
            reverse('redaction_article_notifications', kwargs={'pk': self.article_for_no_one.pk})
        )
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 0)

        # Send notifications for all
        response = self.client.get(reverse('redaction_article_notifications', kwargs={'pk': self.article_for_all.pk}))
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 4)
        self.assertEqual(res_recipients[0].last_name, 'Beran')
        self.assertEqual(res_recipients[1].last_name, 'Brambůrek')
        self.assertEqual(res_recipients[2].last_name, 'Lukáš')
        self.assertEqual(res_recipients[3].last_name, 'Nebus')

        # Send notifications for owners
        response = self.client.get(
            reverse('redaction_article_notifications', kwargs={'pk': self.article_for_owners.pk})
        )
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 3)
        self.assertEqual(res_recipients[0].last_name, 'Beran')
        self.assertEqual(res_recipients[1].last_name, 'Brambůrek')
        self.assertEqual(res_recipients[2].last_name, 'Nebus')

        # Send notifications for board
        response = self.client.get(
            reverse('redaction_article_notifications', kwargs={'pk': self.article_for_board.pk})
        )
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 2)
        self.assertEqual(res_recipients[0].last_name, 'Beran')
        self.assertEqual(res_recipients[1].last_name, 'Brambůrek')

        # Send notifications for board
        response = self.client.get(
            reverse('redaction_article_notifications', kwargs={'pk': self.article_for_owners_and_board.pk})
        )
        self.assertEqual(response.status_code, 200)
        res_recipients = response.context['object_list']
        self.assertEqual(len(res_recipients), 3)
        self.assertEqual(res_recipients[0].last_name, 'Beran')
        self.assertEqual(res_recipients[1].last_name, 'Brambůrek')
        self.assertEqual(res_recipients[2].last_name, 'Nebus')
