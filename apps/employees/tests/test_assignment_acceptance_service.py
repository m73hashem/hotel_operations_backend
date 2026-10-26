from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.employees.constants import (
    ASSIGNMENT_STATUS_ACCEPTED,
    ASSIGNMENT_STATUS_ASSIGNED,
)
from apps.employees.exceptions import AssignmentNotAssigned, AssignmentNotFound
from apps.employees.models import Assignment, Department, Employee
from apps.employees.services import AssignmentAcceptanceService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case
from apps.rooms.models import Hotel, Room


class AssignmentAcceptanceServiceTests(TestCase):
    """Tests for Assignment acceptance persistence and validation."""

    def create_assignment(self, *, status=ASSIGNMENT_STATUS_ASSIGNED) -> Assignment:
        """Create an Assignment with the domain context it requires."""

        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        employee = Employee.objects.create(
            department=department,
            employee_number="EMP-001",
            name="Test Employee",
            phone="555000001",
            status="ACTIVE",
        )
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
        case = Case.objects.create(stay=stay, subject="Please send towels.")
        return Assignment.objects.create(
            case=case,
            employee=employee,
            status=status,
            assigned_at=timezone.now(),
        )

    def test_accept_assignment_updates_only_assignment_state(self):
        """Acceptance changes the Assignment state and accepted timestamp."""

        assignment = self.create_assignment()
        case_status = assignment.case.status

        accepted = AssignmentAcceptanceService.accept_assignment(assignment.id)

        assignment.refresh_from_db()
        assignment.case.refresh_from_db()
        self.assertEqual(accepted.id, assignment.id)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_ACCEPTED)
        self.assertIsNotNone(assignment.accepted_at)
        self.assertEqual(assignment.case.status, case_status)

    def test_rejects_unknown_assignment(self):
        """An Assignment must exist before it can be accepted."""

        with self.assertRaises(AssignmentNotFound):
            AssignmentAcceptanceService.accept_assignment(999)

    def test_rejects_assignment_that_is_not_assigned(self):
        """Only ASSIGNED Assignments can transition to ACCEPTED."""

        assignment = self.create_assignment(status=ASSIGNMENT_STATUS_ACCEPTED)

        with self.assertRaises(AssignmentNotAssigned):
            AssignmentAcceptanceService.accept_assignment(assignment.id)
