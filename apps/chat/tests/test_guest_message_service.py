from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
    MESSAGE_CHANNEL_WEB_CHAT,
    MESSAGE_SENDER_TYPE_GUEST,
)
from apps.chat.models import Conversation, Message
from apps.chat.services import GuestMessageService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class GuestMessageServiceTests(TestCase):
    """Tests for guest message persistence."""

    def test_send_to_general_conversation_creates_one_guest_message(self):
        """The service persists one message with canonical sender and channel values."""

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
        conversation = Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

        message = GuestMessageService.send_to_general_conversation(
            conversation=conversation,
            guest_id=guest.id,
            content="  Exact content  ",
        )

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.conversation_id, conversation.id)
        self.assertEqual(message.sender_id, guest.id)
        self.assertEqual(message.sender_type, MESSAGE_SENDER_TYPE_GUEST)
        self.assertEqual(message.channel, MESSAGE_CHANNEL_WEB_CHAT)
        self.assertEqual(message.content, "  Exact content  ")
