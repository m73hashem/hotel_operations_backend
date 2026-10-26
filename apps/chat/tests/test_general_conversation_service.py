from datetime import timedelta
from unittest.mock import patch

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
)
from apps.chat.models import Conversation
from apps.chat.selectors import ConversationSelector
from apps.chat.services import GeneralConversationService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.rooms.models import Hotel, Room


class GeneralConversationServiceTests(TestCase):
    """Tests for active General Conversation creation."""

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

    def test_returns_existing_active_general_conversation(self):
        """An existing active General Conversation is reused."""

        stay = self.create_stay()
        conversation = Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

        result = GeneralConversationService.get_or_create_active_general_conversation(
            stay,
        )

        self.assertEqual(result.pk, conversation.pk)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_creates_an_active_general_conversation(self):
        """A Stay without one receives an active General Conversation."""

        stay = self.create_stay()

        result = GeneralConversationService.get_or_create_active_general_conversation(
            stay,
        )

        self.assertEqual(result.stay_id, stay.id)
        self.assertEqual(result.type, CONVERSATION_TYPE_GENERAL)
        self.assertEqual(result.status, CONVERSATION_STATUS_ACTIVE)
        self.assertIsNone(result.case)

    def test_repeated_requests_return_one_active_general_conversation(self):
        """Repeated calls preserve the one active General Conversation rule."""

        stay = self.create_stay()

        first = GeneralConversationService.get_or_create_active_general_conversation(stay)
        second = GeneralConversationService.get_or_create_active_general_conversation(stay)

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_retries_lookup_after_an_integrity_error(self):
        """A concurrent insert collision returns the newly existing conversation."""

        stay = self.create_stay()
        concurrent_conversation = Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

        with (
            patch.object(
                ConversationSelector,
                "get_active_general_for_stay",
                side_effect=[None, concurrent_conversation],
            ),
            patch(
                "apps.chat.services.general_conversation_service.Conversation.objects.create",
                side_effect=IntegrityError,
            ),
        ):
            result = (
                GeneralConversationService.get_or_create_active_general_conversation(
                    stay,
                )
            )

        self.assertEqual(result.pk, concurrent_conversation.pk)

    def test_database_constraint_prevents_duplicate_active_general_conversations(self):
        """The partial unique constraint forbids a second active General Conversation."""

        stay = self.create_stay()
        Conversation.objects.create(
            stay=stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Conversation.objects.create(
                    stay=stay,
                    type=CONVERSATION_TYPE_GENERAL,
                    status=CONVERSATION_STATUS_ACTIVE,
                )
