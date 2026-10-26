from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.employees.constants import (
    ASSIGNMENT_STATUS_ASSIGNED,
    ASSIGNMENT_STATUS_IN_PROGRESS,
    ASSIGNMENT_STATUS_RELEASED,
)
from apps.employees.exceptions import CaseAlreadyAssigned, CaseNotFound, EmployeeNotFound
from apps.employees.models import Assignment, Department, Employee
from apps.employees.services import CaseAssignmentService
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case
from apps.rooms.models import Hotel, Room


class CaseAssignmentServiceTests(TestCase):
    """Tests for Assignment persistence and business validation."""

    def create_case_and_employee(self) -> tuple[Case, Employee]:
        """Create the domain objects needed for a Case assignment."""

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
        return case, employee

    def test_assign_case_creates_one_active_assignment(self):
        """The service persists the Case owner with the canonical status."""

        case, employee = self.create_case_and_employee()

        assignment = CaseAssignmentService.assign_case(case.id, employee.id)

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(assignment.case_id, case.id)
        self.assertEqual(assignment.employee_id, employee.id)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_ASSIGNED)
        self.assertIsNotNone(assignment.assigned_at)

    def test_rejects_a_second_active_assignment_for_the_case(self):
        """The business rule prevents duplicate active Case ownership."""

        case, employee = self.create_case_and_employee()
        CaseAssignmentService.assign_case(case.id, employee.id)

        with self.assertRaises(CaseAlreadyAssigned):
            CaseAssignmentService.assign_case(case.id, employee.id)

        self.assertEqual(Assignment.objects.count(), 1)

    def test_database_prevents_second_assignment_while_first_is_in_progress(self):
        """The partial unique constraint includes IN_PROGRESS Assignments."""

        case, employee = self.create_case_and_employee()
        Assignment.objects.create(
            case=case,
            employee=employee,
            status=ASSIGNMENT_STATUS_IN_PROGRESS,
            assigned_at=timezone.now(),
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Assignment.objects.create(
                case=case,
                employee=employee,
                status=ASSIGNMENT_STATUS_ASSIGNED,
                assigned_at=timezone.now(),
            )

    def test_database_allows_assignment_after_prior_assignment_is_released(self):
        """RELEASED Assignments do not participate in the active constraint."""

        case, employee = self.create_case_and_employee()
        Assignment.objects.create(
            case=case,
            employee=employee,
            status=ASSIGNMENT_STATUS_RELEASED,
            assigned_at=timezone.now(),
            released_at=timezone.now(),
        )

        assignment = Assignment.objects.create(
            case=case,
            employee=employee,
            status=ASSIGNMENT_STATUS_ASSIGNED,
            assigned_at=timezone.now(),
        )

        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_ASSIGNED)

    def test_rejects_unknown_case(self):
        """An Assignment cannot be created without a Case."""

        _, employee = self.create_case_and_employee()

        with self.assertRaises(CaseNotFound):
            CaseAssignmentService.assign_case(999, employee.id)

    def test_rejects_unknown_employee(self):
        """An Assignment cannot be created without an Employee."""

        case, _ = self.create_case_and_employee()

        with self.assertRaises(EmployeeNotFound):
            CaseAssignmentService.assign_case(case.id, 999)
