from django.test import TestCase
from django.urls import reverse

from .testdata import ArticleDataMixin


class ArticleListTest(ArticleDataMixin, TestCase):
    def do_user_test(self, username, password, for_all, for_owners, for_board, article_list):
        # Login user
        if username == 'anonymous':
            self.client.logout()
        else:
            logged_in = self.client.login(username=username, password=password)
            self.assertTrue(logged_in)

        # Article for all
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_all.slug}))
        self.assertEqual(response.status_code, for_all)

        # Article for Owners
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_owners.slug}))
        self.assertEqual(response.status_code, for_owners)

        # Article for Board
        response = self.client.get(reverse('article', kwargs={'slug': self.article_for_board.slug}))
        self.assertEqual(response.status_code, for_board)

        # Main page
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        # List of Articles
        res_articles = response.context['article_list']
        self.assertEqual([a.header for a in res_articles], article_list)

    def test_admin_user(self):
        self.do_user_test(
            'jarda',
            self.u_jarda_password,
            200,
            200,
            200,
            ['For Board', 'For Owners and Board', 'For Owners', 'For All'],
        )

    def test_board_user(self):
        self.do_user_test(
            'jiri',
            self.u_jiri_password,
            200,
            200,
            200,
            ['For Board', 'For Owners and Board', 'For Owners', 'For All'],
        )

    def test_owner_user(self):
        self.do_user_test(
            'peter',
            self.u_peter_password,
            200,
            200,
            404,
            ['For Owners and Board', 'For Owners', 'For All'],
        )

    def test_vendor_user(self):
        self.do_user_test(
            'karel',
            self.u_karel_password,
            200,
            404,
            404,
            ['For All'],
        )

    def test_anonymous_user(self):
        self.do_user_test('anonymous', '', 200, 302, 302, ['For All'])

    def test_top_articles(self):
        # Login board user
        logged_in = self.client.login(username='jiri', password=self.u_jiri_password)
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
        logged_in = self.client.login(username='peter', password=self.u_peter_password)
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
        logged_in = self.client.login(username='jiri', password=self.u_jiri_password)
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
