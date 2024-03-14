from django.test import TestCase
from django.urls import reverse
from .models import Article, ArticleMenu
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission


groups = {
    'owner': ['svjis_add_article_comment', 'svjis_view_personal_menu', 'svjis_view_phonelist',],
    'board_member': ['svjis_view_redaction_menu','svjis_edit_article','svjis_add_article_comment','svjis_edit_article_menu','svjis_edit_article_news','svjis_view_personal_menu','svjis_view_phonelist',],
    'vendor': ['svjis_add_article_comment','svjis_view_personal_menu',],
}

users = {
    'jiri': {
         'first_name': 'Jiří',
         'last_name': 'Brambůrek',
         'password': 'jiri',
         'email': 'jiri@test.cz',
    },
    'petr': {
         'first_name': 'Petr',
         'last_name': 'Nebus',
         'password': 'petr',
         'email': 'petr@test.cz',
    },
    'karel': {
         'first_name': 'Karel',
         'last_name': 'Lukáš',
         'password': 'karel',
         'email': 'karel@test.cz',
    },
}


def create_group(name):
    gobj = Group(name=name)
    gobj.save()
    for p in groups[name]:
        pobj = Permission.objects.get(content_type__app_label='articles', codename=p)
        gobj.permissions.add(pobj)
    return gobj


def create_user(name, groups):
    u = User.objects.create(username=name,
        email=users[name]['email'],
        password=make_password(users[name]['password']),
        first_name=users[name]['first_name'],
        last_name=users[name]['last_name'],
    )
    u.is_active = True
    u.save()
    for g in groups:
        u.groups.add(g)
    return u


class ArticleListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.g_owner = create_group('owner')
        cls.g_board_member = create_group('board_member')
        cls.g_vendor = create_group('vendor')

        cls.u_jiri = create_user('jiri', [cls.g_owner, cls.g_board_member])
        cls.u_petr = create_user('petr', [cls.g_owner])
        cls.u_karel = create_user('karel', [cls.g_vendor])

        cls.menu_docs = ArticleMenu.objects.create(description='Documents')

        cls.article_for_all = Article.objects.create(header='For All', perex='test perex', body='test body', menu=cls.menu_docs, author=cls.u_jiri, published=True, visible_for_all=True)
        cls.article_for_owners = Article.objects.create(header='For Owners', perex='test perex', body='test body', menu=cls.menu_docs, author=cls.u_jiri, published=True, visible_for_all=False)
        cls.article_for_owners.visible_for_group.add(cls.g_owner)
        cls.article_for_board = Article.objects.create(header='For Board', perex='test perex', body='test body', menu=cls.menu_docs, author=cls.u_jiri, published=True, visible_for_all=False)
        cls.article_for_owners.visible_for_group.add(cls.g_board_member)


    def test_anonymous_user(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 2)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')

        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 1)
        self.assertEqual(res_articles[0].header, 'For All')


    def test_owner_user(self):
        logged_in = self.client.login(username='petr', password=users['petr']['password'])
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 3)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')

        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 2)
        self.assertEqual(res_articles[0].header, 'For Owners')
        self.assertEqual(res_articles[1].header, 'For All')


    def test_board_user(self):
        logged_in = self.client.login(username='jiri', password=users['jiri']['password'])
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 4)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')
        self.assertEqual(res_tray_menu[3]['description'], 'Redaction')

        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 2)
        self.assertEqual(res_articles[0].header, 'For Owners')
        self.assertEqual(res_articles[1].header, 'For All')


    def test_vendor_user(self):
        logged_in = self.client.login(username='karel', password=users['karel']['password'])
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        res_tray_menu = response.context['tray_menu_items']
        self.assertEqual(len(res_tray_menu), 3)
        self.assertEqual(res_tray_menu[0]['description'], 'Articles')
        self.assertEqual(res_tray_menu[1]['description'], 'Contact')
        self.assertEqual(res_tray_menu[2]['description'], 'Personal settings')

        res_articles = response.context['article_list']
        self.assertEqual(len(res_articles), 1)
        self.assertEqual(res_articles[0].header, 'For All')
