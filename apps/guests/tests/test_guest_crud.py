from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.guests.api.serializers import GuestSerializer
from apps.guests.builders import GuestBuilder
from apps.guests.dto import GuestDTO
from apps.guests.exceptions import GuestNotFound
from apps.guests.use_cases.create_guest import CreateGuestUseCase
from apps.guests.use_cases.list_guests import ListGuestsUseCase
from apps.guests.use_cases.retrieve_guest import RetrieveGuestUseCase


class GuestCrudUseCaseTests(SimpleTestCase):
    """Tests for Guest CRUD application orchestration."""

    @patch("apps.guests.use_cases.list_guests.GuestBuilder.build_list")
    @patch("apps.guests.use_cases.list_guests.GuestService.list_guests")
    def test_list_execute_coordinates_service_and_builder(self, list_guests, build_list):
        """Listing loads Guests before building their DTOs."""

        guests = [SimpleNamespace()]
        dto_list = [Mock(spec=GuestDTO)]
        list_guests.return_value = guests
        build_list.return_value = dto_list

        result = ListGuestsUseCase.execute(5)

        self.assertIs(result, dto_list)
        list_guests.assert_called_once_with(5)
        build_list.assert_called_once_with(guests)

    @patch("apps.guests.use_cases.create_guest.GuestBuilder.build")
    @patch("apps.guests.use_cases.create_guest.GuestService.create_guest")
    def test_create_execute_coordinates_service_and_builder(self, create_guest, build):
        """Creation persists the Guest before building its DTO."""

        validated_data = {"first_name": "Test"}
        guest = SimpleNamespace()
        dto = Mock(spec=GuestDTO)
        create_guest.return_value = guest
        build.return_value = dto

        result = CreateGuestUseCase.execute(validated_data)

        self.assertIs(result, dto)
        create_guest.assert_called_once_with(validated_data)
        build.assert_called_once_with(guest)

    @patch("apps.guests.use_cases.retrieve_guest.GuestService.get_guest")
    def test_retrieve_propagates_domain_exceptions_unchanged(self, get_guest):
        """Guest lookup failures remain domain exceptions."""

        error = GuestNotFound()
        get_guest.side_effect = error

        with self.assertRaises(GuestNotFound) as raised:
            RetrieveGuestUseCase.execute(1)

        self.assertIs(raised.exception, error)

    def test_serializer_validates_guest_request_shape(self):
        """The serializer validates Guest request data before the Use Case."""

        serializer = GuestSerializer(
            data={
                "first_name": "Test",
                "last_name": "Guest",
                "phone": "555000000",
                "email": "test@example.com",
                "language": "en",
            },
        )

        self.assertTrue(serializer.is_valid())


class GuestBuilderTests(SimpleTestCase):
    """Tests for flat Guest DTO construction."""

    def test_build_returns_a_flat_guest_dto(self):
        """The builder transforms an already-loaded Guest without ORM access."""

        timestamp = datetime(2026, 8, 1, 12, 0, 0)
        guest = SimpleNamespace(
            id=1,
            created_at=timestamp,
            updated_at=timestamp,
            first_name="Test",
            last_name="Guest",
            phone="555000000",
            email="test@example.com",
            language="en",
        )

        dto = GuestBuilder.build(guest)

        self.assertEqual(dto.id, 1)
        self.assertEqual(dto.first_name, "Test")
        self.assertEqual(dto.updated_at, timestamp)
