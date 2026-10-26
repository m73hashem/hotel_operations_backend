from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation
from apps.chat.selectors import ConversationSelector
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class ConversationSelectorTests(TestCase):
    """Tests for read-only General Conversation lookups."""

    def create_stay(self) -> Stay:
        """Create a Stay suitable for a General Conversation."""

        hotel = Hotel.objects.create(
            name="Test Hotel",
            timezone="Asia/Riyadh",
            status="ACTIVE",
        )
        room = Room.objects.create(
            hotel=hotel,
            room_number="101",
            room_type="STANDARD",
            status="AVAILABLE",
        )
        guest = Guest.objects.create(
            first_name="Test",
            last_name="Guest",
            phone="555000000",
            language="en",
        )
        return Stay.objects.create(
            guest=guest,
            room=room,
            check_in=timezone.now(),
            expected_check_out=timezone.now() + timedelta(days=1),
            status=STAY_STATUS_ACTIVE,
        )

    def test_returns_active_general_conversation_with_stay_loaded(self):
        """The selector returns the active General Conversation in one query."""

        stay = self.create_stay()
        conversation = Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

        with self.assertNumQueries(1):
            result = ConversationSelector.get_active_general_for_stay(stay.id)

        self.assertEqual(result.pk, conversation.pk)
        self.assertIn("stay", result._state.fields_cache)

    def test_returns_none_when_no_active_general_conversation_exists(self):
        """Inactive General Conversations are not returned."""

        stay = self.create_stay()
        Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status="CLOSED",
        )

        result = ConversationSelector.get_active_general_for_stay(stay.id)

        self.assertIsNone(result)
