"""Unit tests for operational Room list orchestration and mapping."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.rooms.builders import RoomListBuilder
from apps.rooms.dto import RoomListItemDTO
from apps.rooms.use_cases import ListRoomsUseCase


class ListRoomsUseCaseTests(SimpleTestCase):
    """Verify Room list use-case orchestration."""

    @patch("apps.rooms.use_cases.list_rooms.RoomListBuilder.build")
    @patch("apps.rooms.use_cases.list_rooms.RoomListingService.get_operational_rooms")
    def test_execute_coordinates_service_and_builder(self, get_operational_rooms, build):
        """The use case delegates retrieval before DTO construction."""

        rooms = [SimpleNamespace()]
        dto = (Mock(spec=RoomListItemDTO),)
        get_operational_rooms.return_value = rooms
        build.return_value = dto

        self.assertIs(
            ListRoomsUseCase.execute(user_id=4, search="101", ordering="room_number"),
            dto,
        )
        get_operational_rooms.assert_called_once_with(4, search="101", ordering="room_number")
        build.assert_called_once_with(rooms)


class RoomListBuilderTests(SimpleTestCase):
    """Verify Room list DTO mapping."""

    def test_build_maps_already_loaded_room_and_hotel(self):
        """The builder maps only the selected Room transport fields."""

        timestamp = datetime(2026, 8, 2, 9, 0, 0)
        room = SimpleNamespace(
            id=7,
            hotel_id=3,
            hotel=SimpleNamespace(name="Demo Hotel"),
            room_number="101",
            room_type="STANDARD",
            status="OCCUPIED",
            created_at=timestamp,
            updated_at=timestamp,
        )

        result = RoomListBuilder.build([room])

        self.assertEqual(result[0].room_id, 7)
        self.assertEqual(result[0].hotel_name, "Demo Hotel")
        self.assertEqual(result[0].room_number, "101")
