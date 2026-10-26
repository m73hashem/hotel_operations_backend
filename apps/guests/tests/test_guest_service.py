from django.test import TestCase
from unittest.mock import patch

from apps.guests.exceptions import GuestNotFound
from apps.guests.models import Guest
from apps.guests.services import GuestService


class GuestServiceTests(TestCase):
    """Tests for Guest persistence and domain validation."""

    def create_guest(self) -> Guest:
        """Create a Guest with valid CRUD input."""

        return Guest.objects.create(
            first_name="Test",
            last_name="Guest",
            phone="555000000",
            email="test@example.com",
            language="en",
        )

    @patch("apps.guests.services.services.EmployeeAccessService.get_active_employee")
    def test_list_guests_returns_persisted_guests(self, get_active_employee):
        """The service retrieves Guests through the selector."""

        guest = self.create_guest()

        self.assertEqual(GuestService.list_guests(1), [guest])
        get_active_employee.assert_called_once_with(1)

    def test_get_guest_raises_domain_exception_when_missing(self):
        """Missing Guests use the shared domain exception flow."""

        with self.assertRaises(GuestNotFound):
            GuestService.get_guest(999)

    def test_update_guest_persists_validated_data(self):
        """The service updates an existing Guest."""

        guest = self.create_guest()

        updated_guest = GuestService.update_guest(
            guest.id,
            {"first_name": "Updated", "language": "ar"},
        )

        updated_guest.refresh_from_db()
        self.assertEqual(updated_guest.first_name, "Updated")
        self.assertEqual(updated_guest.language, "ar")

    def test_delete_guest_removes_existing_guest(self):
        """The service deletes an existing Guest."""

        guest = self.create_guest()

        GuestService.delete_guest(guest.id)

        self.assertFalse(Guest.objects.filter(id=guest.id).exists())
