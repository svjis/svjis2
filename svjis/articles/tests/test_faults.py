from django.test import TestCase
from django.urls import reverse

from .testdata import UserDataMixin


class FaultsTest(UserDataMixin, TestCase):

    def create_fault_and_get_created_by(self, username, password, user_provided):
        # Login user
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

        # Create Fault
        fault = {
            'pk': 0,
            'subject': 'test',
            'entrance': '',
            'description': 'test',
            'assigned_to_user': '',
        }

        if user_provided is not None:
            fault['created_by_user'] = user_provided

        response = self.client.post(
            reverse('faults_fault_create_save'),
            fault,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        # Test Fault Creator
        fault = response.context['obj']
        return fault.created_by_user

    def test_owner_user(self):
        fault_creator = self.create_fault_and_get_created_by("petr", "petr", "")
        self.assertEqual(fault_creator, self.u_petr)

    def test_owner_user_on_behalf_of(self):
        fault_creator = self.create_fault_and_get_created_by("petr", "petr", self.u_jarda.pk)
        self.assertEqual(fault_creator, self.u_petr)

    def test_board_user_on_behalf_of(self):
        fault_creator = self.create_fault_and_get_created_by("jiri", "jiri", self.u_jarda.pk)
        self.assertEqual(fault_creator, self.u_jarda)

    def test_board_user_empty_user_provided(self):
        fault_creator = self.create_fault_and_get_created_by("jiri", "jiri", None)
        self.assertEqual(fault_creator, self.u_jiri)
