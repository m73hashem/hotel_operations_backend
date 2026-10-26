from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation, Message
from apps.chat.selectors import MessageSelector
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class MessageSelectorTests(TestCase):
    """Tests for read-only Conversation History message loading."""

    def create_conversation(self) -> Conversation:
        """Create a General Conversation with the required Stay context."""

        hotel = Hotel.objects.create(
            name="Test Hotel",
            timezone="Asia/Riyadh",
            status="ACTIVE",
        )
        room = Room.objects.create(
            hotel=hotel,
            room_number="101",
            room_type="STANDARD",
            status="OCCUPIED",
        )
        guest = Guest.objects.create(
            first_name="Test",
            last_name="Guest",
            phone="555000000",
            language="en",
        )
        stay = Stay.objects.create(
            guest=guest,
            room=room,
            check_in=timezone.now(),
            expected_check_out=timezone.now() + timedelta(days=1),
            status=STAY_STATUS_ACTIVE,
        )
        return Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

    def test_returns_only_requested_fields_in_oldest_first_order(self):
        """The selector orders messages in the database and avoids deferred reads."""

        conversation = self.create_conversation()
        first = Message.objects.create(
            conversation=conversation,
            sender_type="GUEST",
            sender_id=1,
            content="First",
            channel="WEB_CHAT",
        )
        second = Message.objects.create(
            conversation=conversation,
            sender_type="GUEST",
            sender_id=1,
            content="Second",
            channel="WEB_CHAT",
        )

        with self.assertNumQueries(1):
            messages = MessageSelector.list_for_conversation(conversation.id)

        self.assertEqual([message.id for message in messages], [first.id, second.id])
        self.assertEqual(messages[0].get_deferred_fields(), {"conversation_id", "sender_id", "updated_at"})

    def test_returns_an_empty_list_when_the_conversation_has_no_messages(self):
        """An active Conversation without messages has an empty history."""

        conversation = self.create_conversation()

        self.assertEqual(
            MessageSelector.list_for_conversation(conversation.id),
            [],
        )
