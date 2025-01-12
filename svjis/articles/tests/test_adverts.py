from django.test import TestCase
from django.urls import reverse

from .testdata import UserDataMixin


class AdvertsTest(UserDataMixin, TestCase):

    def create_advert(self, username, password, advert_form, expected_status):
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        response = self.client.post(
            reverse('adverts_save'),
            advert_form,
            follow=False,
        )
        if expected_status == 302:
            self.assertEqual(response.status_code, expected_status)
            self.assertEqual(response.url, '/adverts_list/')
            response = self.client.get(reverse('adverts_list'), follow=True)
            self.assertEqual(response.status_code, 200)

            adverts = response.context['object_list']
            self.assertEqual(len(adverts), 1)

            advert = adverts[0]['advert']
            return advert
        else:
            self.assertEqual(response.status_code, expected_status)
            return None

    def test_hide_adverts_of_deactivated_user(self):
        # create advert
        self.create_advert(
            "peter",
            self.u_peter_password,
            {
                'pk': 0,
                'type': 1,
                'header': 'testing advert',
                'body': 'testing advert body',
                'phone': '123',
                'email': 'test@test.com',
                'published': True,
            },
            302,
        )

        # advert is visible for other users
        logged_in = self.client.login(username='jiri', password=self.u_jiri_password)
        self.assertTrue(logged_in)

        response = self.client.get(reverse('adverts_list'), follow=True)
        self.assertEqual(response.status_code, 200)

        adverts = response.context['object_list']
        self.assertEqual(len(adverts), 1)

        advert = adverts[0]['advert']
        self.assertEqual(advert.created_by_user, self.u_peter)

        # disable advert owner
        self.u_peter.is_active = False
        self.u_peter.save()

        # advert is not visible for other users
        response = self.client.get(reverse('adverts_list'), follow=True)
        self.assertEqual(response.status_code, 200)

        adverts = response.context['object_list']
        self.assertEqual(len(adverts), 0)

    def test_advert_update(self):
        advert = self.create_advert(
            "peter",
            self.u_peter_password,
            {
                'pk': 0,
                'type': 1,
                'header': 'testing advert',
                'body': 'testing advert body',
                'phone': '123',
                'email': 'test@test.com',
                'published': True,
            },
            302,
        )
        self.assertEqual(advert.header, 'testing advert')

        advert = self.create_advert(
            "peter",
            self.u_peter_password,
            {
                'pk': advert.pk,
                'type': 1,
                'header': 'testing advert 2',
                'body': 'testing advert body',
                'phone': '123',
                'email': 'test@test.com',
                'published': True,
            },
            302,
        )
        self.assertEqual(advert.header, 'testing advert 2')

    def test_advert_update_by_another_user(self):
        advert = self.create_advert(
            "peter",
            self.u_peter_password,
            {
                'pk': 0,
                'type': 1,
                'header': 'testing advert',
                'body': 'testing advert body',
                'phone': '123',
                'email': 'test@test.com',
                'published': True,
            },
            302,
        )
        self.assertEqual(advert.header, 'testing advert')

        advert = self.create_advert(
            "jiri",
            self.u_jiri_password,
            {
                'pk': advert.pk,
                'type': 1,
                'header': 'testing advert 2',
                'body': 'testing advert body',
                'phone': '123',
                'email': 'test@test.com',
                'published': True,
            },
            404,
        )
