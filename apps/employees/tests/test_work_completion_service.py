from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.chat.constants import CASE_STATUS_COMPLETED, CASE_STATUS_IN_PROGRESS
from apps.employees.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_IN_PROGRESS,
)
from apps.employees.exceptions import (
    AssignmentNotFound,
    AssignmentNotInProgress,
    CaseNotInProgress,
)
from apps.employees.models import Assignment, Department, Employee
from apps.employees.services import WorkCompletionService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case, CaseTimeline, WorkOrder
from apps.rooms.models import Hotel, Room


class WorkCompletionServiceTests(TestCase):
    """Tests for atomic Assignment and Case work-completion transitions."""

    def create_assignment(
        self,
        *,
        assignment_status=ASSIGNMENT_STATUS_IN_PROGRESS,
        case_status=CASE_STATUS_IN_PROGRESS,
    ) -> Assignment:
        """Create in-progress Assignment context for work completion."""

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
        return Assignment.objects.create(
            case=case,
            employee=employee,
            status=assignment_status,
            assigned_at=timezone.now(),
            accepted_at=timezone.now(),
        )

    def test_complete_work_transitions_assignment_and_case_without_side_effects(self):
        """Both required state changes complete within the service operation."""

        assignment = self.create_assignment()

        updated_assignment, updated_case = WorkCompletionService.complete_work(
            assignment.id,
        )

        assignment.refresh_from_db()
        assignment.case.refresh_from_db()
        self.assertEqual(updated_assignment.id, assignment.id)
        self.assertEqual(updated_case.id, assignment.case_id)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_COMPLETED)
        self.assertEqual(assignment.case.status, CASE_STATUS_COMPLETED)
        self.assertEqual(WorkOrder.objects.count(), 0)
        self.assertEqual(CaseTimeline.objects.count(), 0)

    def test_rejects_unknown_assignment(self):
        """An Assignment must exist before work can be completed."""

        with self.assertRaises(AssignmentNotFound):
            WorkCompletionService.complete_work(999)

    def test_rejects_assignment_that_is_not_in_progress(self):
        """Only IN_PROGRESS Assignments can transition to completed."""

        assignment = self.create_assignment(
            assignment_status=ASSIGNMENT_STATUS_COMPLETED,
        )

        with self.assertRaises(AssignmentNotInProgress):
            WorkCompletionService.complete_work(assignment.id)

    def test_rejects_case_that_is_not_in_progress(self):
        """Only IN_PROGRESS Cases may transition to completed."""

        assignment = self.create_assignment(case_status=CASE_STATUS_COMPLETED)

        with self.assertRaises(CaseNotInProgress):
            WorkCompletionService.complete_work(assignment.id)
