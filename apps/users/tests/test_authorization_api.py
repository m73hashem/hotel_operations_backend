from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.employees.models import Department, Employee
from apps.users.constants import ROLE_RECEPTION
from apps.users.models import User


class AuthorizationAPITests(TestCase):
    """Integration tests for RBAC-protected existing endpoints."""

    def create_employee_user(self, *, role_name=None):
        """Create one authenticated Employee with an optional Django Group role."""

        user = User.objects.create_user(username="employee", password="password")
        department = Department.objects.create(name="Reception", status="ACTIVE")
        Employee.objects.create(
            user=user,
            department=department,
            employee_number="EMP-001",
            name="Reception Employee",
            phone="555000001",
            status="ACTIVE",
        )
        if role_name is not None:
            user.groups.add(Group.objects.create(name=role_name))
        return user

    def test_guest_management_requires_declared_role(self):
        """An Employee without a role receives the standard permission envelope."""

        user = self.create_employee_user()
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("guest-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["success"])

    def test_reception_role_can_access_guest_management(self):
        """Reception receives the guest-management permission from the matrix."""

        user = self.create_employee_user(role_name=ROLE_RECEPTION)
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("guest-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
