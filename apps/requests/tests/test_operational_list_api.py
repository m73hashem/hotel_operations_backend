"""Integration tests for operational Request and Case list endpoints."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class OperationalListAPITests(TestCase):
    """Verify operational Request and Case lists retain authentication protection."""

    def test_request_list_requires_authentication(self):
        """Unauthenticated callers cannot retrieve the Request list."""

        response = self.client.get(reverse("requests:request-list"), {"status": "NEW"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_case_list_requires_authentication(self):
        """Unauthenticated callers cannot retrieve the Case list."""

        response = self.client.get(reverse("cases:case-list"), {"priority": "HIGH"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
