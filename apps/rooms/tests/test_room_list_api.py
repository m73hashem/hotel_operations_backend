"""Integration tests for the operational Room list endpoint."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class RoomListAPITests(TestCase):
    """Verify the Room list endpoint remains protected by JWT authentication."""

    def test_list_requires_authentication(self):
        """Unauthenticated callers cannot retrieve operational Room data."""

        response = self.client.get(reverse("rooms:room-list"), {"search": "101"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
