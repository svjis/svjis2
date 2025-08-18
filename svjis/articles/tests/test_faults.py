from django.test import TestCase
from django.urls import reverse

from .factories.fault_report import FaultReportFactory
from .testdata import UserDataMixin, PreferencesDataMixin


class FaultsTest(UserDataMixin, PreferencesDataMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fault = FaultReportFactory(created_by_user=cls.u_jiri, closed=False)

        cls.create_url = reverse('faults_fault_create_save')
        cls.detail_url = reverse('fault', kwargs={'slug': cls.fault.slug})
        cls.update_url = reverse('faults_fault_update')

    def create_fault_and_get_created_by(self, username, password, fault_form):
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        response = self.client.post(
            self.create_url,
            fault_form,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        return response.context['obj']

    def test_retrieve(self):
        logged_in = self.client.login(username='jiri', password=self.u_jiri_password)
        self.assertTrue(logged_in)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        fault = response.context['obj']
        self.assertEqual(fault, self.fault)
        self.assertEqual(fault.logs.count(), 0)

    def test_close_fault_retrieve_logs(self):
        logged_in = self.client.login(username='jiri', password=self.u_jiri_password)
        self.assertTrue(logged_in)
        response = self.client.post(
            self.update_url,
            {
                'assigned_to_user': self.u_jarda.pk,
                'closed': True,
                'pk': self.fault.pk,
                'subject': self.fault.subject,
                'description': self.fault.description,
                'created_by_user': self.fault.created_by_user.pk,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.fault.refresh_from_db()

        self.assertEqual(self.fault.closed, True)
        self.assertEqual(self.fault.logs.count(), 2)
        assigned, closed = self.fault.logs.all()
        self.assertEqual(assigned.type, assigned.TYPE_ASSIGNED)
        self.assertEqual(assigned.resolver, self.u_jarda)
        self.assertEqual(assigned.user, self.u_jiri)
        self.assertEqual(closed.type, closed.TYPE_CLOSED)
        self.assertEqual(closed.resolver, self.u_jarda)
        self.assertEqual(closed.user, self.u_jiri)

    # Created by user
    def test_owner_created_by_user(self):
        fault = self.create_fault_and_get_created_by(
            "peter", self.u_peter_password, {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': ''}
        )
        self.assertEqual(fault.created_by_user, self.u_peter)

    def test_owner_on_behalf_of(self):
        fault = self.create_fault_and_get_created_by(
            "peter",
            self.u_peter_password,
            {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': self.u_jarda.pk},
        )
        self.assertEqual(fault.created_by_user, self.u_peter)

    def test_board_on_behalf_of(self):
        fault = self.create_fault_and_get_created_by(
            "jiri",
            self.u_jiri_password,
            {'pk': 0, 'subject': 'test', 'description': 'test', 'created_by_user': self.u_jarda.pk},
        )
        self.assertEqual(fault.created_by_user, self.u_jarda)

    def test_board_created_by_user_missing(self):
        fault = self.create_fault_and_get_created_by(
            "jiri", self.u_jiri_password, {'pk': 0, 'subject': 'test', 'description': 'test'}
        )
        self.assertEqual(fault.created_by_user, self.u_jiri)

    # Assigned to user
    def test_owner_assigned_to_user_empty(self):
        fault = self.create_fault_and_get_created_by(
            "peter", self.u_peter_password, {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': ''}
        )
        self.assertEqual(fault.assigned_to_user, None)

    def test_owner_assigned_to_user(self):
        fault = self.create_fault_and_get_created_by(
            "peter",
            self.u_peter_password,
            {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': self.u_jarda.pk},
        )
        self.assertEqual(fault.assigned_to_user, None)

    def test_board_assigned_to_user(self):
        fault = self.create_fault_and_get_created_by(
            "jiri",
            self.u_jiri_password,
            {'pk': 0, 'subject': 'test', 'description': 'test', 'assigned_to_user': self.u_jarda.pk},
        )
        self.assertEqual(fault.assigned_to_user, self.u_jarda)

    # Closed
    def test_owner_closed(self):
        fault = self.create_fault_and_get_created_by(
            "peter", self.u_peter_password, {'pk': 0, 'subject': 'test', 'description': 'test', 'closed': True}
        )
        self.assertEqual(fault.closed, False)

    def test_board_closed(self):
        fault = self.create_fault_and_get_created_by(
            "jiri", self.u_jiri_password, {'pk': 0, 'subject': 'test', 'description': 'test', 'closed': True}
        )
        self.assertEqual(fault.closed, True)
