from django.test import TestCase
from django.urls import reverse
from .models import Article
from django.contrib.auth.models import User

class ArticleListTest(TestCase):

    def test_anonymous_user_menu(self):
        response = self.client.get(reverse('main'))
        response_tray_menu = response.context['tray_menu_items']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_tray_menu), 1)
        self.assertEqual(response_tray_menu[0]['description'], 'Articles')
