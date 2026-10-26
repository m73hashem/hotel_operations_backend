from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.employees.models import Department, Employee
from apps.users.models import User


class AuthenticationAPITests(TestCase):
    """Integration tests for employee authentication endpoints."""

    def create_employee(self, *, employee_status=EMPLOYEE_STATUS_ACTIVE):
        """Create a User and related Employee profile for authentication tests."""

        user = User.objects.create_user(
            username="amina",
            password="secure-password",
            email="amina@example.com",
        )
        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        employee = Employee.objects.create(
            user=user,
            department=department,
            employee_number="EMP-001",
            name="Amina Al Saud",
            phone="555000001",
            email="amina@example.com",
            status=employee_status,
        )
        return user, employee

    def assert_success_envelope(self, response, expected_status):
        """Assert the project-standard successful response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertTrue(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)

    def test_login_returns_employee_dto_and_jwt_pair(self):
        """Only an active Employee can obtain a JWT pair."""

        _, employee = self.create_employee()

        response = self.client.post(
            reverse("auth:login"),
            {"username": "amina", "password": "secure-password"},
            content_type="application/json",
        )

        self.assert_success_envelope(response, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["employee_id"], employee.id)
        self.assertEqual(
            set(response.data["data"]),
            {
                "employee_id",
                "user_id",
                "full_name",
                "department_id",
                "access_token",
                "refresh_token",
            },
        )

    def test_login_rejects_invalid_credentials(self):
        """Invalid credentials return the standard domain-error envelope."""

        self.create_employee()

        response = self.client.post(
            reverse("auth:login"),
            {"username": "amina", "password": "wrong"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_me_returns_authenticated_employee_dto(self):
        """A valid JWT resolves the active Employee profile."""

        user, employee = self.create_employee()
        access_token = str(RefreshToken.for_user(user).access_token)

        response = self.client.get(
            reverse("auth:me"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assert_success_envelope(response, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["employee_id"], employee.id)
        self.assertEqual(response.data["data"]["email"], user.email)

    def test_refresh_returns_new_access_token(self):
        """Simple JWT refresh uses the standard response envelope."""

        user, _ = self.create_employee()
        refresh_token = str(RefreshToken.for_user(user))

        response = self.client.post(
            reverse("auth:refresh"),
            {"refresh_token": refresh_token},
            content_type="application/json",
        )

        self.assert_success_envelope(response, status.HTTP_200_OK)
        self.assertEqual(set(response.data["data"]), {"access_token"})

    def test_logout_blacklists_refresh_token(self):
        """Logout blacklists the submitted Simple JWT refresh token."""

        user, _ = self.create_employee()
        refresh_token = str(RefreshToken.for_user(user))

        response = self.client.post(
            reverse("auth:logout"),
            {"refresh_token": refresh_token},
            content_type="application/json",
        )

        self.assert_success_envelope(response, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], {"logged_out": True})
