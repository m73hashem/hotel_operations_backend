from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.guests.models import Guest


class GuestAPITests(TestCase):
    """Integration tests for Guest CRUD endpoints."""

    def guest_payload(self, **overrides):
        """Return valid Guest request input."""

        payload = {
            "first_name": "Test",
            "last_name": "Guest",
            "phone": "555000000",
            "email": "test@example.com",
            "language": "en",
        }
        payload.update(overrides)
        return payload

    def create_guest(self) -> Guest:
        """Create one Guest for detail endpoint tests."""

        return Guest.objects.create(**self.guest_payload())

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_lists_guests_with_standard_envelope(self):
        """Listing preserves the existing endpoint response contract."""

        guest = self.create_guest()

        response = self.client.get(reverse("guest-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"][0]["id"], guest.id)

    def test_creates_guest_with_standard_envelope(self):
        """Creating returns the persisted Guest and HTTP 201."""

        response = self.client.post(
            reverse("guest-list"),
            data=self.guest_payload(),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["first_name"], "Test")

    def test_retrieves_and_updates_guest(self):
        """Detail reads and updates preserve the established API response envelope."""

        guest = self.create_guest()
        url = reverse("guest-detail", kwargs={"pk": guest.id})

        get_response = self.client.get(url)
        update_response = self.client.put(
            url,
            data=self.guest_payload(first_name="Updated"),
            content_type="application/json",
        )

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["data"]["first_name"], "Updated")

    def test_deletes_guest_with_standard_envelope(self):
        """Deleting retains the prior no-data success response."""

        guest = self.create_guest()

        response = self.client.delete(reverse("guest-detail", kwargs={"pk": guest.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertFalse(Guest.objects.filter(id=guest.id).exists())

    def test_missing_guest_uses_domain_exception_envelope(self):
        """Unknown Guest identifiers use the global domain exception handler."""

        response = self.client.get(reverse("guest-detail", kwargs={"pk": 999}))

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)
