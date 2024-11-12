from django.test import TestCase
from django.urls import reverse

from .testdata import UserDataMixin


class FaultsTest(UserDataMixin, TestCase):

    def create_fault_and_get_created_by(self, username, password, fault_form):
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        response = self.client.post(
            reverse('faults_fault_create_save'),
            fault_form,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        return response.context['obj']

    # Created by user
    def test_owner_created_by_user(self):
        fault = self.create_fault_and_get_created_by(
            "petr", "petr", {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': ''}
        )
        self.assertEqual(fault.created_by_user, self.u_petr)

    def test_owner_on_behalf_of(self):
        fault = self.create_fault_and_get_created_by(
            "petr", "petr", {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': self.u_jarda.pk}
        )
        self.assertEqual(fault.created_by_user, self.u_petr)

    def test_board_on_behalf_of(self):
        fault = self.create_fault_and_get_created_by(
            "jiri", "jiri", {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': self.u_jarda.pk}
        )
        self.assertEqual(fault.created_by_user, self.u_jarda)

    def test_board_created_by_user_missing(self):
        fault = self.create_fault_and_get_created_by(
            "jiri", "jiri", {'pk': 0, 'subject': 'test', 'description': 'test'}
        )
        self.assertEqual(fault.created_by_user, self.u_jiri)

    # Assigned to user
    def test_owner_assigned_to_user_empty(self):
        fault = self.create_fault_and_get_created_by(
            "petr", "petr", {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': ''}
        )
        self.assertEqual(fault.assigned_to_user, None)

    def test_owner_assigned_to_user(self):
        fault = self.create_fault_and_get_created_by(
            "petr", "petr", {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': self.u_jarda.pk}
        )
        self.assertEqual(fault.assigned_to_user, None)

    def test_board_assigned_to_user(self):
        fault = self.create_fault_and_get_created_by(
            "jiri", "jiri", {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': self.u_jarda.pk}
        )
        self.assertEqual(fault.assigned_to_user, self.u_jarda)
