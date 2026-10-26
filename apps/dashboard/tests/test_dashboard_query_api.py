"""Integration tests for dashboard list query endpoints."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class DashboardQueryAPITests(TestCase):
    """Verify dashboard query endpoints retain authentication protection."""

    def test_my_assignments_requires_authentication(self):
        """The filtered assignment list remains JWT-protected."""

        response = self.client.get(reverse("dashboard:my-assignments"), {"search": "towels"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_department_queue_requires_authentication(self):
        """The filtered department queue remains JWT-protected."""

        response = self.client.get(
            reverse("dashboard:department-queue"),
            {"ordering": "room_number"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
