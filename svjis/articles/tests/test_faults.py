from django.test import TestCase
from django.urls import reverse

from .testdata import UserDataMixin


class FaultsTest(UserDataMixin, TestCase):

    def create_fault_and_get_created_by(self, username, password, user_provided):
        # Login user
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

        # Create Fault
        response = self.client.post(
            reverse('faults_fault_create_save'),
            {
                'pk': 0,
                'subject': 'test',
                'entrance': '',
                'description': 'test',
                'created_by_user': user_provided,
                'assigned_to_user': '',
            },
            follow=True,
        )

        # Test Fault Creator
        fault = response.context['obj']
        return fault.created_by_user

    def test_owner_user(self):
        user = self.create_fault_and_get_created_by("petr", "petr", "")
        self.assertEqual(user, self.u_petr)

    def test_owner_user_on_behalf_of(self):
        user = self.create_fault_and_get_created_by("petr", "petr", self.u_jarda.pk)
        self.assertEqual(user, self.u_petr)

    def test_board_user_on_behalf_of(self):
        user = self.create_fault_and_get_created_by("jiri", "jiri", self.u_jarda.pk)
        self.assertEqual(user, self.u_jarda)
