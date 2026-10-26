"""Seed one complete idempotent operational scenario for manual testing."""

from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.chat.constants import MESSAGE_CHANNEL_WEB_CHAT, MESSAGE_SENDER_TYPE_GUEST
from apps.chat.models import Message, Request
from apps.chat.selectors import ConversationSelector
from apps.chat.services import (
    GeneralConversationService,
    GuestMessageService,
    RequestCreationService,
)
from apps.employees.models import Assignment, Employee
from apps.employees.services import CaseAssignmentService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case
from apps.requests.services import CaseCreationService
from apps.rooms.models import Hotel, Room

DEMO_HOTEL_NAME = "Demo Operations Hotel"
DEMO_HOTEL_TIMEZONE = "Asia/Riyadh"
DEMO_HOTEL_STATUS = "ACTIVE"
DEMO_ROOM_NUMBER = "101"
DEMO_ROOM_TYPE = "STANDARD"
DEMO_ROOM_STATUS = "OCCUPIED"
DEMO_GUEST_FIRST_NAME = "John"
DEMO_GUEST_LAST_NAME = "Smith"
DEMO_GUEST_PHONE = "0500000000"
DEMO_GUEST_EMAIL = "john.smith@hotel.local"
DEMO_GUEST_LANGUAGE = "en"
DEMO_REQUEST_MESSAGE = "Need extra towels"
DEMO_RECEPTION_MESSAGE = "Your request has been received. Housekeeping will handle it shortly."
DEMO_RECEPTION_SENDER_TYPE = "RECEPTION"
DEMO_HOUSEKEEPING_USERNAME = "housekeeping"


class Command(BaseCommand):
    """Create one reusable guest-to-assignment operational demo scenario."""

    help = "Create an idempotent operational scenario for local manual testing."

    def handle(self, *args, **options):
        """Create or reuse the complete demo operation within one transaction."""

        results = {
            "Guest": [False],
            "Room": [False],
            "Stay": [False],
            "Conversation": [False],
            "Request": [False],
            "Case": [False],
            "Assignment": [False],
            "Messages": [False, False, False],
        }

        with transaction.atomic():
            hotel = self._get_hotel()
            guest, results["Guest"][0] = self._get_guest()
            room, results["Room"][0] = self._get_room(hotel)
            stay, results["Stay"][0] = self._get_stay(guest, room)
            conversation, results["Conversation"][0] = self._get_conversation(stay)
            request_record, results["Request"][0] = self._get_request(stay, conversation)
            case, results["Case"][0] = self._get_case(request_record)
            assignment, results["Assignment"][0] = self._get_assignment(case)
            reception_employee = self._get_reception_employee()
            results["Messages"] = self._get_messages(
                conversation,
                guest,
                reception_employee,
            )

        self._print_results(results)

    @staticmethod
    def _get_hotel() -> Hotel:
        """Return the Hotel required by the demo Room."""

        hotel, _ = Hotel.objects.get_or_create(
            name=DEMO_HOTEL_NAME,
            defaults={
                "timezone": DEMO_HOTEL_TIMEZONE,
                "status": DEMO_HOTEL_STATUS,
            },
        )
        return hotel

    @staticmethod
    def _get_guest() -> tuple[Guest, bool]:
        """Return the stable demo Guest."""

        return Guest.objects.get_or_create(
            phone=DEMO_GUEST_PHONE,
            defaults={
                "first_name": DEMO_GUEST_FIRST_NAME,
                "last_name": DEMO_GUEST_LAST_NAME,
                "email": DEMO_GUEST_EMAIL,
                "language": DEMO_GUEST_LANGUAGE,
            },
        )

    @staticmethod
    def _get_room(hotel: Hotel) -> tuple[Room, bool]:
        """Return the stable occupied demo Room."""

        return Room.objects.get_or_create(
            hotel=hotel,
            room_number=DEMO_ROOM_NUMBER,
            defaults={
                "room_type": DEMO_ROOM_TYPE,
                "status": DEMO_ROOM_STATUS,
            },
        )

    @staticmethod
    def _get_stay(guest: Guest, room: Room) -> tuple[Stay, bool]:
        """Return one active Stay for the demo Guest and Room."""

        stay = Stay.objects.filter(
            guest=guest,
            room=room,
            status=STAY_STATUS_ACTIVE,
        ).first()
        if stay is not None:
            return stay, False

        now = timezone.now()
        return (
            Stay.objects.create(
                guest=guest,
                room=room,
                check_in=now,
                expected_check_out=now + timedelta(days=1),
                status=STAY_STATUS_ACTIVE,
            ),
            True,
        )

    @staticmethod
    def _get_conversation(stay: Stay):
        """Return the default General Conversation through its business service."""

        existing = ConversationSelector.get_active_general_for_stay(stay.id)
        if existing is not None:
            return existing, False

        return GeneralConversationService.get_or_create_active_general_conversation(stay), True

    @staticmethod
    def _get_request(stay: Stay, conversation) -> tuple[Request, bool]:
        """Return or create the original Request through its business service."""

        request_record = Request.objects.filter(
            stay=stay,
            conversation=conversation,
            original_message=DEMO_REQUEST_MESSAGE,
        ).first()
        if request_record is not None:
            return request_record, False

        return (
            RequestCreationService.create_from_guest_message(
                stay,
                conversation,
                DEMO_REQUEST_MESSAGE,
            ),
            True,
        )

    @staticmethod
    def _get_case(request_record: Request) -> tuple[Case, bool]:
        """Return or create the Case through its business service."""

        case = Case.objects.filter(request=request_record).first()
        if case is not None:
            return case, False

        case, _ = CaseCreationService.create_from_request(request_record.id)
        return case, True

    @staticmethod
    def _get_assignment(case: Case) -> tuple[Assignment, bool]:
        """Return or create the Case Assignment through its business service."""

        assignment = Assignment.objects.filter(case=case).first()
        if assignment is not None:
            return assignment, False

        employee = Employee.objects.filter(
            user__username=DEMO_HOUSEKEEPING_USERNAME,
        ).first()
        if employee is None:
            raise CommandError(
                "Housekeeping demo Employee not found. Run seed_demo_users first.",
            )

        return CaseAssignmentService.assign_case(case.id, employee.id), True

    @staticmethod
    def _get_reception_employee() -> Employee:
        """Return the demo Reception Employee for the manual response message."""

        employee = Employee.objects.filter(user__username="reception").first()
        if employee is None:
            raise CommandError(
                "Reception demo Employee not found. Run seed_demo_users first.",
            )
        return employee

    @staticmethod
    def _get_messages(
        conversation,
        guest: Guest,
        reception_employee: Employee,
    ) -> list[bool]:
        """Return or create the manual guest and Reception conversation messages."""

        results = []
        for content in ("Hello", "I need extra towels"):
            message = Message.objects.filter(
                conversation=conversation,
                sender_type=MESSAGE_SENDER_TYPE_GUEST,
                sender_id=guest.id,
                content=content,
                channel=MESSAGE_CHANNEL_WEB_CHAT,
            ).first()
            if message is None:
                GuestMessageService.send_to_general_conversation(
                    conversation,
                    guest.id,
                    content,
                )
                results.append(True)
            else:
                results.append(False)

        _, created = Message.objects.get_or_create(
            conversation=conversation,
            sender_type=DEMO_RECEPTION_SENDER_TYPE,
            sender_id=reception_employee.id,
            content=DEMO_RECEPTION_MESSAGE,
            channel=MESSAGE_CHANNEL_WEB_CHAT,
        )
        results.append(created)
        return results

    def _print_results(self, results: dict[str, list[bool]]) -> None:
        """Print created-versus-existing status for each scenario component."""

        for name, created_values in results.items():
            self.stdout.write(name)
            self.stdout.write("Created" if any(created_values) else "Exists")
