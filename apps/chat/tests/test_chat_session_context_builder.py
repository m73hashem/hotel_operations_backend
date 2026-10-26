from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.chat.builders import ChatSessionContextBuilder


class ChatSessionContextBuilderTests(SimpleTestCase):
    """Tests for flat chat-session context DTO construction."""

    def test_build_maps_already_loaded_domain_objects_without_orm_access(self):
        """The builder exposes only client-facing chat-context fields."""

        conversation = SimpleNamespace(pk=1, type="GENERAL", status="ACTIVE")
        guest = SimpleNamespace(
            pk=2,
            first_name="Test",
            last_name="Guest",
            language="en",
        )
        stay = SimpleNamespace(pk=3)
        room = SimpleNamespace(pk=4, room_number="101", room_type="STANDARD")
        hotel = SimpleNamespace(pk=5, name="Test Hotel", timezone="Asia/Riyadh")

        dto = ChatSessionContextBuilder.build(
            conversation=conversation,
            guest=guest,
            stay=stay,
            room=room,
            hotel=hotel,
        )

        self.assertEqual(dto.conversation_id, 1)
        self.assertEqual(dto.guest_id, 2)
        self.assertEqual(dto.stay_id, 3)
        self.assertEqual(dto.room_number, "101")
        self.assertEqual(dto.hotel_name, "Test Hotel")
