from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.guests.constants import GUEST_SESSION_STATUS_ACTIVE, STAY_STATUS_ACTIVE
from apps.guests.models import Guest, GuestSession, Stay
from apps.guests.selectors import GuestSessionSelector
from apps.rooms.models import Hotel, Room


class GuestSessionSelectorTests(TestCase):
    """Tests for GuestSessionSelector chat-context loading."""

    def create_guest_session(self) -> GuestSession:
        """Create a valid guest session and all required related objects."""

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
        stay = Stay.objects.create(
            guest=guest,
            room=room,
            check_in=timezone.now(),
            expected_check_out=timezone.now() + timedelta(days=1),
            status=STAY_STATUS_ACTIVE,
        )
        return GuestSession.objects.create(
            stay=stay,
            token="valid-session-token",
            status=GUEST_SESSION_STATUS_ACTIVE,
            expires_at=timezone.now() + timedelta(hours=1),
        )

    def test_get_by_token_for_chat_returns_loaded_related_objects(self):
        """The selector returns the session with its chat context eagerly loaded."""

        guest_session = self.create_guest_session()

        with self.assertNumQueries(1):
            result = GuestSessionSelector.get_by_token_for_chat(guest_session.token)

        self.assertEqual(result.pk, guest_session.pk)
        self.assertIn("stay", result._state.fields_cache)
        self.assertIn("guest", result.stay._state.fields_cache)
        self.assertIn("room", result.stay._state.fields_cache)
        self.assertIn("hotel", result.stay.room._state.fields_cache)

    def test_get_by_token_for_chat_returns_none_for_unknown_token(self):
        """The selector returns None when no Guest Session has the supplied token."""

        result = GuestSessionSelector.get_by_token_for_chat("unknown-session-token")

        self.assertIsNone(result)
