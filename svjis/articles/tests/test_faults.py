from django.test import TestCase
from django.urls import reverse

from .testdata import UserDataMixin


class FaultsTest(UserDataMixin, TestCase):

    def test_owner_user(self):
        # Login user
        logged_in = self.client.login(username='petr', password='petr')
        self.assertTrue(logged_in)

        # Create Fault
        response = self.client.post(
            reverse('faults_fault_create_save'),
            {
                'pk': 0,
                'subject': 'test',
                'entrance': '',
                'description': 'test',
                # 'created_by_user': '',
                'assigned_to_user': '',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # Test Fault Creator
        fault = response.context['obj']
        self.assertEqual(fault.created_by_user, self.u_petr)

    def test_owner_user_on_behalf_of(self):
        # Login user
        logged_in = self.client.login(username='petr', password='petr')
        self.assertTrue(logged_in)

        # Create Fault
        response = self.client.post(
            reverse('faults_fault_create_save'),
            {
                'pk': 0,
                'subject': 'test',
                'entrance': '',
                'description': 'test',
                'created_by_user': self.u_jarda.pk,
                'assigned_to_user': '',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # Test Fault Creator
        fault = response.context['obj']
        self.assertEqual(fault.created_by_user, self.u_petr)

    def test_board_user_on_behalf_of(self):
        # Login user
        logged_in = self.client.login(username='jiri', password='jiri')
        self.assertTrue(logged_in)

        # Create Fault
        response = self.client.post(
            reverse('faults_fault_create_save'),
            {
                'pk': 0,
                'subject': 'test',
                'entrance': '',
                'description': 'test',
                'created_by_user': self.u_jarda.pk,
                'assigned_to_user': '',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # Test Fault Creator
        fault = response.context['obj']
        self.assertEqual(fault.created_by_user, self.u_jarda)
