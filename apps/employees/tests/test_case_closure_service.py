from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import CASE_STATUS_CLOSED, CASE_STATUS_COMPLETED
from apps.employees.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_RELEASED,
)
from apps.employees.exceptions import (
    AssignmentNotCompleted,
    AssignmentNotFound,
    CaseNotCompleted,
    CaseNotFound,
)
from apps.employees.models import Assignment, Department, Employee
from apps.employees.services import CaseClosureService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case, CaseTimeline, WorkOrder
from apps.rooms.models import Hotel, Room


class CaseClosureServiceTests(TestCase):
    """Tests for atomic Case-closure and Assignment-release transitions."""

    def create_case_and_assignment(
        self,
        *,
        case_status=CASE_STATUS_COMPLETED,
        assignment_status=ASSIGNMENT_STATUS_COMPLETED,
        create_assignment=True,
    ) -> tuple[Case, Assignment | None]:
        """Create completed Case context for Case closure."""

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
        case = Case.objects.create(
            stay=stay,
            subject="Please send towels.",
            status=case_status,
        )
        if not create_assignment:
            return case, None

        return case, Assignment.objects.create(
            case=case,
            employee=employee,
            status=assignment_status,
            assigned_at=timezone.now(),
            accepted_at=timezone.now(),
        )

    def test_close_case_releases_assignment_without_side_effects(self):
        """Closing transitions only the Case and its Assignment."""

        case, assignment = self.create_case_and_assignment()

        updated_case, updated_assignment = CaseClosureService.close_case(case.id)

        case.refresh_from_db()
        assignment.refresh_from_db()
        self.assertEqual(updated_case.id, case.id)
        self.assertEqual(updated_assignment.id, assignment.id)
        self.assertEqual(case.status, CASE_STATUS_CLOSED)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_RELEASED)
        self.assertIsNotNone(assignment.released_at)
        self.assertEqual(WorkOrder.objects.count(), 0)
        self.assertEqual(CaseTimeline.objects.count(), 0)

    def test_rejects_unknown_case(self):
        """A Case must exist before it can be closed."""

        with self.assertRaises(CaseNotFound):
            CaseClosureService.close_case(999)

    def test_rejects_case_that_is_not_completed(self):
        """Only COMPLETED Cases can transition to closed."""

        case, _ = self.create_case_and_assignment(case_status=CASE_STATUS_CLOSED)

        with self.assertRaises(CaseNotCompleted):
            CaseClosureService.close_case(case.id)

    def test_rejects_case_without_assignment(self):
        """A completed Case requires an Assignment to be released."""

        case, _ = self.create_case_and_assignment(create_assignment=False)

        with self.assertRaises(AssignmentNotFound):
            CaseClosureService.close_case(case.id)

    def test_rejects_assignment_that_is_not_completed(self):
        """Only COMPLETED Assignments can transition to released."""

        case, _ = self.create_case_and_assignment(
            assignment_status=ASSIGNMENT_STATUS_RELEASED,
        )

        with self.assertRaises(AssignmentNotCompleted):
            CaseClosureService.close_case(case.id)
