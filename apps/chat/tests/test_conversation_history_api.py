from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import (
    CONVERSATION_STATUS_ACTIVE,
    CONVERSATION_TYPE_GENERAL,
    MESSAGE_CHANNEL_WEB_CHAT,
    MESSAGE_SENDER_TYPE_GUEST,
)
from apps.chat.models import Conversation, Message
from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room


class ConversationHistoryAPITests(TestCase):
    """Integration tests for the Conversation History endpoint."""

    def create_guest_session(
        self,
        *,
        session_status=GUEST_SESSION_STATUS_ACTIVE,
        stay_status=STAY_STATUS_ACTIVE,
        expires_at=None,
    ) -> GuestSession:
        """Create a guest session with its required chat context."""

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
            status=stay_status,
        )
        return GuestSession.objects.create(
            stay=stay,
            token="guest-session-token",
            status=session_status,
            expires_at=expires_at or timezone.now() + timedelta(hours=1),
        )

    def get_history(self, session_token=None):
        """Get the registered Conversation History endpoint."""

        params = {} if session_token is None else {"session_token": session_token}
        return self.client.get(reverse("chat:send-message"), data=params)

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_returns_active_general_conversation_messages_oldest_first(self):
        """A valid Guest Session receives only its active General Conversation history."""

        guest_session = self.create_guest_session()
        conversation = Conversation.objects.create(
            stay=guest_session.stay,
            type=CONVERSATION_TYPE_GENERAL,
            status=CONVERSATION_STATUS_ACTIVE,
        )
        first = Message.objects.create(
            conversation=conversation,
            sender_type=MESSAGE_SENDER_TYPE_GUEST,
            sender_id=guest_session.stay.guest_id,
            content="First",
            channel=MESSAGE_CHANNEL_WEB_CHAT,
        )
        second = Message.objects.create(
            conversation=conversation,
            sender_type=MESSAGE_SENDER_TYPE_GUEST,
            sender_id=guest_session.stay.guest_id,
            content="Second",
            channel=MESSAGE_CHANNEL_WEB_CHAT,
        )

        response = self.get_history(f"  {guest_session.token}  ")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Conversation history retrieved successfully.")
        self.assertEqual(
            response.data["data"]["messages"],
            [
                {
                    "id": first.id,
                    "sender_type": MESSAGE_SENDER_TYPE_GUEST,
                    "content": "First",
                    "channel": MESSAGE_CHANNEL_WEB_CHAT,
                    "created_at": response.data["data"]["messages"][0]["created_at"],
                },
                {
                    "id": second.id,
                    "sender_type": MESSAGE_SENDER_TYPE_GUEST,
                    "content": "Second",
                    "channel": MESSAGE_CHANNEL_WEB_CHAT,
                    "created_at": response.data["data"]["messages"][1]["created_at"],
                },
            ],
        )

    def test_returns_empty_history_without_creating_a_conversation(self):
        """A read request does not create a missing General Conversation."""

        guest_session = self.create_guest_session()

        response = self.get_history(guest_session.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["messages"], [])
        self.assertEqual(Conversation.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)

    def test_rejects_a_missing_session_token(self):
        """The request requires a session token."""

        response = self.get_history()

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_token", response.data["errors"])

    def test_rejects_an_unknown_session(self):
        """An unknown Guest Session token is unauthorized."""

        response = self.get_history("unknown-token")

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_session(self):
        """An inactive Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(session_status="INACTIVE")

        response = self.get_history(guest_session.token)

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_expired_session(self):
        """An expired Guest Session token is unauthorized."""

        guest_session = self.create_guest_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        response = self.get_history(guest_session.token)

        self.assert_error_envelope(response, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_an_inactive_stay(self):
        """An inactive Stay does not expose Conversation History."""

        guest_session = self.create_guest_session(stay_status="CHECKED_OUT")

        response = self.get_history(guest_session.token)

        self.assert_error_envelope(response, status.HTTP_403_FORBIDDEN)
