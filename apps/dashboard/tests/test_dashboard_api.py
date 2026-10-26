"""Integration tests for dashboard API endpoints."""

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.employees.models import Department, Employee
from apps.users.models import User


class DashboardAPITests(TestCase):
    """Verify authenticated dashboard endpoints return the standard envelope."""

    def setUp(self):
        self.user = User.objects.create_user(username="dashboard-user", password="password")
        group = Group.objects.create(name="HOUSEKEEPING")
        self.user.groups.add(group)
        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        Employee.objects.create(
            user=self.user,
            department=department,
            employee_number="DASH-001",
            name="Dashboard User",
            phone="0500000001",
            status=EMPLOYEE_STATUS_ACTIVE,
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(self.user)}")

    def test_summary_returns_standard_envelope(self):
        """The summary endpoint is registered and returns summary data."""

        response = self.client.get(reverse("dashboard:summary"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["employee_id"], self.user.employee.id)

    def test_my_assignments_returns_standard_envelope(self):
        """The personal assignment endpoint is registered and authenticated."""

        response = self.client.get(reverse("dashboard:my-assignments"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["assignments"], [])

    def test_department_queue_returns_standard_envelope(self):
        """The department queue endpoint is registered and authenticated."""

        response = self.client.get(reverse("dashboard:department-queue"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["cases"], [])
