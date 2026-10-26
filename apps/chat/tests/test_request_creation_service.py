from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
    REQUEST_SOURCE_WEB_CHAT,
    REQUEST_STATUS_NEW,
)
from apps.chat.models import Conversation, Request
from apps.chat.services import RequestCreationService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class RequestCreationServiceTests(TestCase):
    """Tests for guest Request persistence."""

    def test_create_from_guest_message_persists_one_request(self):
        """The service preserves the original message and required relationships."""

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

        request_record = RequestCreationService.create_from_guest_message(
            stay=stay,
            conversation=conversation,
            message="  Please send two towels.  ",
        )

        self.assertEqual(Request.objects.count(), 1)
        self.assertEqual(request_record.stay_id, stay.id)
        self.assertEqual(request_record.guest_id, guest.id)
        self.assertEqual(request_record.room_id, room.id)
        self.assertEqual(request_record.conversation_id, conversation.id)
        self.assertEqual(request_record.original_message, "  Please send two towels.  ")
        self.assertEqual(request_record.title, "  Please send two towels.  ")
        self.assertEqual(request_record.status, REQUEST_STATUS_NEW)
        self.assertEqual(request_record.source, REQUEST_SOURCE_WEB_CHAT)
