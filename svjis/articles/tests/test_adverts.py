from django.test import TestCase
from django.urls import reverse

from .. import models
from ..model_utils import get_asset_type
from .testdata import UserDataMixin


class AssetTypeTest(TestCase):
    def test_get_asset_type(self):
        asset_types = {
            'picture.JPG': 'PICTURE',
            'document.pdf': 'DOCUMENT',
            'movie.mp4': 'VIDEO',
            'unknown.bin': 'UNKNOWN',
        }

        for basename, expected_type in asset_types.items():
            with self.subTest(basename=basename):
                self.assertEqual(get_asset_type(basename), expected_type)


class AdvertsTest(UserDataMixin, TestCase):
    def create_advert_with_asset(self, filename, description):
        advert = models.Advert.objects.create(
            type=self.advert_types[0],
            header='Advert with asset',
            body='Advert body',
            created_by_user=self.u_peter,
        )
        file_path = f'adverts/{advert.pk}/{filename}'
        models.AdvertAsset.objects.create(
            description=description,
            file=file_path,
            advert=advert,
            created_by_user=self.u_peter,
        )
        self.client.force_login(self.u_peter)
        response = self.client.get(reverse('adverts_list'))
        self.assertEqual(response.status_code, 200)
        return response, file_path

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
            self.assertEqual(response.url, '/adverts_edit/1/')
            response = self.client.get(reverse('adverts_list'), follow=True)
            self.assertEqual(response.status_code, 200)

            adverts = response.context['object_list']
            self.assertEqual(len(adverts), 1)
            return adverts[0]
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

        advert = adverts[0]
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

    def test_image_asset_renders_linked_preview(self):
        response, file_path = self.create_advert_with_asset('preview.jpg', 'Image preview')

        self.assertContains(
            response,
            f'<a href="/media/{file_path}" class="advert-image-preview-link" aria-haspopup="dialog" '
            'aria-controls="advert-image-dialog"><img '
            f'src="/media/{file_path}" class="advert-image-preview" alt="Image preview" loading="lazy"></a>',
            html=True,
        )
        self.assertContains(response, '<dialog id="advert-image-dialog" class="advert-image-dialog">')
        self.assertContains(response, '<script src="/static/js/Adverts_ImagePreview.js"></script>', html=True)

    def test_non_image_asset_keeps_attachment_link(self):
        response, file_path = self.create_advert_with_asset('document.pdf', 'Document')

        self.assertContains(
            response,
            '<img src="/static/gfx/Files_pdf.gif" class="led" alt="document.pdf">',
            html=True,
        )
        self.assertContains(response, f'<a href="/media/{file_path}">Document</a>', html=True)
        self.assertNotContains(response, 'advert-image-preview')
