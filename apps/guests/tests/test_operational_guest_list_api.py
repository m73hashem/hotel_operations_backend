"""Integration tests for operational Guest and Stay list endpoints."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class OperationalGuestListAPITests(TestCase):
    """Verify operational Guest and Stay lists retain authentication protection."""

    def test_guest_list_requires_authentication(self):
        """Unauthenticated callers cannot retrieve the Guest list."""

        response = self.client.get(reverse("guest-list"), {"search": "Smith"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_stay_list_requires_authentication(self):
        """Unauthenticated callers cannot retrieve the Stay list."""

        response = self.client.get(reverse("stays:stay-list"), {"status": "ACTIVE"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
