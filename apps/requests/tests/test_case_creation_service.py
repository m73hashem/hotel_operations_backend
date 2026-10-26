from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CASE_STATUS_OPEN,
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_CASE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation, Request
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.exceptions import CaseAlreadyExistsForRequest
from apps.requests.models import Case
from apps.requests.services import CaseCreationService
from apps.rooms.models import Hotel, Room


class CaseCreationServiceTests(TestCase):
    """Tests for Case and dedicated Conversation persistence."""

    def create_request(self) -> Request:
        """Create a Request with its active General Conversation context."""

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
        return Request.objects.create(
            stay=stay,
            guest=guest,
            room=room,
            conversation=conversation,
            original_message="Please send two towels.",
            title="Please send two towels.",
        )

    def test_create_from_request_persists_case_and_case_conversation(self):
        """The service creates the Case and its dedicated Conversation atomically."""

        request_record = self.create_request()

        case, conversation = CaseCreationService.create_from_request(request_record.id)

        self.assertEqual(Case.objects.count(), 1)
        self.assertEqual(case.request_id, request_record.id)
        self.assertEqual(case.stay_id, request_record.stay_id)
        self.assertEqual(case.subject, request_record.title)
        self.assertEqual(case.status, CASE_STATUS_OPEN)
        self.assertIsNone(case.service)
        self.assertIsNone(case.priority)
        self.assertEqual(conversation.stay_id, request_record.stay_id)
        self.assertEqual(conversation.case_id, case.id)
        self.assertEqual(conversation.type, CONVERSATION_TYPE_CASE)
        self.assertEqual(conversation.status, CONVERSATION_STATUS_ACTIVE)

    def test_rejects_creating_a_second_case_for_the_same_request(self):
        """A Request may create only one operational Case."""

        request_record = self.create_request()
        CaseCreationService.create_from_request(request_record.id)

        with self.assertRaises(CaseAlreadyExistsForRequest):
            CaseCreationService.create_from_request(request_record.id)

        self.assertEqual(Case.objects.count(), 1)
