"""Integration tests for the operational dashboard statistics endpoint."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class DashboardStatisticsAPITests(TestCase):
    """Verify the statistics endpoint retains JWT authentication protection."""

    def test_statistics_requires_authentication(self):
        """Unauthenticated callers cannot retrieve dashboard statistics."""

        response = self.client.get(reverse("dashboard:statistics"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
