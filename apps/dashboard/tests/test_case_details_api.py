"""Integration tests for the dashboard Case details endpoint."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class CaseDetailsAPITests(TestCase):
    """Verify endpoint registration and the standard response envelope."""

    def test_requires_authentication(self):
        """Unauthenticated requests are rejected before Case retrieval."""

        response = self.client.get(reverse("dashboard:case-details", kwargs={"case_id": 1}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
