"""Create idempotent local demo data for Vertical Slice development."""

from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.chat.services import GeneralConversationService
from apps.guests.constants import (
    GUEST_SESSION_STATUS_ACTIVE,
    STAY_STATUS_ACTIVE,
)
from apps.guests.models import Guest, GuestSession, Stay
from apps.rooms.models import Hotel, Room

DEMO_HOTEL_NAME = "Demo Hotel"
DEMO_HOTEL_TIMEZONE = "Asia/Riyadh"
DEMO_HOTEL_STATUS = "ACTIVE"
DEMO_ROOM_NUMBER = "101"
DEMO_ROOM_TYPE = "STANDARD"
DEMO_ROOM_STATUS = "OCCUPIED"
DEMO_GUEST_FIRST_NAME = "Ahmed"
DEMO_GUEST_LAST_NAME = "Al-Harbi"
DEMO_GUEST_PHONE = "+966500000000"
DEMO_GUEST_EMAIL = "ahmed.alharbi@example.com"
DEMO_GUEST_LANGUAGE = "en"
DEMO_SESSION_TOKEN = "test-session-token"


class Command(BaseCommand):
    """Create the minimum demo data required to exercise Vertical Slices."""

    help = "Create idempotent local demo data for development."

    def handle(self, *args, **options):
        """Create or reuse the demo Hotel, guest context, and conversation."""

        with transaction.atomic():
            hotel = self._get_hotel()
            room = self._get_room(hotel)
            guest = self._get_guest()
            stay = self._get_active_stay(guest, room)
            guest_session = self._get_active_guest_session(stay)
            conversation = (
                GeneralConversationService.get_or_create_active_general_conversation(
                    stay,
                )
            )

        self._print_summary(hotel, room, guest, stay, conversation, guest_session)

    def _get_hotel(self):
        """Return the reusable active demo Hotel."""

        hotel, created = Hotel.objects.get_or_create(
            name=DEMO_HOTEL_NAME,
            defaults={
                "timezone": DEMO_HOTEL_TIMEZONE,
                "status": DEMO_HOTEL_STATUS,
            },
        )
        if not created and hotel.status != DEMO_HOTEL_STATUS:
            hotel.status = DEMO_HOTEL_STATUS
            hotel.save(update_fields=["status", "updated_at"])
        return hotel

    def _get_room(self, hotel):
        """Return the reusable occupied demo Room."""

        room, created = Room.objects.get_or_create(
            hotel=hotel,
            room_number=DEMO_ROOM_NUMBER,
            defaults={
                "room_type": DEMO_ROOM_TYPE,
                "status": DEMO_ROOM_STATUS,
            },
        )
        if not created and room.status != DEMO_ROOM_STATUS:
            room.status = DEMO_ROOM_STATUS
            room.save(update_fields=["status", "updated_at"])
        return room

    def _get_guest(self):
        """Return the reusable demo Guest."""

        guest, _ = Guest.objects.get_or_create(
            phone=DEMO_GUEST_PHONE,
            defaults={
                "first_name": DEMO_GUEST_FIRST_NAME,
                "last_name": DEMO_GUEST_LAST_NAME,
                "email": DEMO_GUEST_EMAIL,
                "language": DEMO_GUEST_LANGUAGE,
            },
        )
        return guest

    def _get_active_stay(self, guest, room):
        """Return an existing active demo Stay or create one."""

        stay = (
            Stay.objects.filter(
                guest=guest,
                room=room,
                status=STAY_STATUS_ACTIVE,
            )
            .order_by("-check_in")
            .first()
        )
        if stay is not None:
            return stay

        now = timezone.now()
        return Stay.objects.create(
            guest=guest,
            room=room,
            check_in=now,
            expected_check_out=now + timedelta(days=1),
            status=STAY_STATUS_ACTIVE,
        )

    def _get_active_guest_session(self, stay):
        """Return the demo Stay session while preserving the fixed token contract."""

        guest_session = GuestSession.objects.filter(stay=stay).first()
        token_session = GuestSession.objects.filter(token=DEMO_SESSION_TOKEN).first()

        if guest_session is None:
            if token_session is not None and token_session.stay_id != stay.id:
                raise CommandError(
                    "The demo session token is already assigned to another Stay.",
                )
            guest_session = GuestSession.objects.create(
                stay=stay,
                token=DEMO_SESSION_TOKEN,
                status=GUEST_SESSION_STATUS_ACTIVE,
                expires_at=timezone.now() + timedelta(days=30),
            )

        if token_session is not None and token_session.pk != guest_session.pk:
            raise CommandError(
                "The demo session token is already assigned to another Stay.",
            )

        if (
            guest_session.token != DEMO_SESSION_TOKEN
            or guest_session.status != GUEST_SESSION_STATUS_ACTIVE
            or guest_session.expires_at <= timezone.now()
        ):
            guest_session.token = DEMO_SESSION_TOKEN
            guest_session.status = GUEST_SESSION_STATUS_ACTIVE
            guest_session.expires_at = timezone.now() + timedelta(days=30)
            guest_session.save(
                update_fields=["token", "status", "expires_at", "updated_at"],
            )

        return guest_session

    def _print_summary(self, hotel, room, guest, stay, conversation, guest_session):
        """Print the stable demo-data summary for local development."""

        self.stdout.write("====================================")
        self.stdout.write("Demo data ready")
        self.stdout.write("====================================")
        self.stdout.write("")
        self.stdout.write(f"Hotel: {hotel.name} (ID: {hotel.id})")
        self.stdout.write(f"Room: {room.room_number} (ID: {room.id})")
        self.stdout.write(f"Guest: {guest.first_name} {guest.last_name} (ID: {guest.id})")
        self.stdout.write(f"Stay: {stay.id}")
        self.stdout.write(f"Conversation: {conversation.id}")
        self.stdout.write("Session Token:")
        self.stdout.write(guest_session.token)
