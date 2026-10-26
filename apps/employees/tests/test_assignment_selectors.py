from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.employees.constants import ASSIGNMENT_STATUS_ASSIGNED
from apps.employees.models import Assignment, Department, Employee
from apps.employees.selectors import AssignmentSelector, EmployeeSelector
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case
from apps.rooms.models import Hotel, Room


class AssignmentSelectorTests(TestCase):
    """Tests for Assignment selectors used by Assign Case."""

    def create_case(self) -> Case:
        """Create a Case with the required Stay context."""

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
        return Case.objects.create(stay=stay, subject="Test")

    def test_employee_selector_returns_the_requested_employee(self):
        """Employee lookup is read-only and returns a matching Employee."""

        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        employee = Employee.objects.create(
            department=department,
            employee_number="EMP-001",
            name="Test Employee",
            phone="555000001",
            status="ACTIVE",
        )

        self.assertEqual(
            EmployeeSelector.get_by_id_for_assignment(employee.id).id,
            employee.id,
        )

    def test_assignment_selector_identifies_an_active_assignment(self):
        """The active-state query uses only active Assignment statuses."""

        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        employee = Employee.objects.create(
            department=department,
            employee_number="EMP-001",
            name="Test Employee",
            phone="555000001",
            status="ACTIVE",
        )
        case = self.create_case()
        Assignment.objects.create(
            case=case,
            employee=employee,
            status=ASSIGNMENT_STATUS_ASSIGNED,
            assigned_at="2026-08-01T12:00:00Z",
        )

        self.assertTrue(AssignmentSelector.exists_active_for_case(case.id))

    def test_assignment_selector_returns_assignment_for_acceptance(self):
        """The acceptance lookup returns the requested Assignment without writes."""

        department = Department.objects.create(name="Housekeeping", status="ACTIVE")
        employee = Employee.objects.create(
            department=department,
            employee_number="EMP-001",
            name="Test Employee",
            phone="555000001",
            status="ACTIVE",
        )
        case = self.create_case()
        assignment = Assignment.objects.create(
            case=case,
            employee=employee,
            status=ASSIGNMENT_STATUS_ASSIGNED,
            assigned_at="2026-08-01T12:00:00Z",
        )

        result = AssignmentSelector.get_by_id_for_acceptance(assignment.id)

        self.assertEqual(result.id, assignment.id)
