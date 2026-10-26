from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.employees.constants import ASSIGNMENT_STATUS_ASSIGNED
from apps.employees.models import Assignment, Department, Employee
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case, CaseTimeline, WorkOrder
from apps.rooms.models import Hotel, Room


class AssignCaseAPITests(TestCase):
    """Integration tests for the Assign Case endpoint."""

    def create_case_and_employee(self) -> tuple[Case, Employee]:
        """Create an unassigned Case and a valid Employee."""

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

    def post_assign_case(self, payload):
        """Post JSON to the registered Assign Case endpoint."""

        return self.client.post(
            reverse("operations:assign-case"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_assigns_case_without_creating_execution_records(self):
        """A valid request creates only one Assignment."""

        case, employee = self.create_case_and_employee()

        response = self.post_assign_case(
            {"case_id": case.id, "employee_id": employee.id},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Case assigned successfully.")
        self.assertEqual(
            set(response.data["data"]),
            {"assignment_id", "case_id", "employee_id", "status", "assigned_at"},
        )
        assignment = Assignment.objects.get(pk=response.data["data"]["assignment_id"])
        self.assertEqual(assignment.case_id, case.id)
        self.assertEqual(assignment.employee_id, employee.id)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_ASSIGNED)
        self.assertEqual(WorkOrder.objects.count(), 0)
        self.assertEqual(CaseTimeline.objects.count(), 0)

    def test_rejects_missing_case_id(self):
        """The request requires a Case identifier."""

        response = self.post_assign_case({"employee_id": 1})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("case_id", response.data["errors"])

    def test_rejects_unknown_case(self):
        """An unknown Case returns the domain not-found response."""

        _, employee = self.create_case_and_employee()

        response = self.post_assign_case({"case_id": 999, "employee_id": employee.id})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_unknown_employee(self):
        """An unknown Employee returns the domain not-found response."""

        case, _ = self.create_case_and_employee()

        response = self.post_assign_case({"case_id": case.id, "employee_id": 999})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_a_duplicate_active_assignment(self):
        """A Case cannot receive a second active Assignment."""

        case, employee = self.create_case_and_employee()
        self.post_assign_case({"case_id": case.id, "employee_id": employee.id})

        response = self.post_assign_case(
            {"case_id": case.id, "employee_id": employee.id},
        )

        self.assert_error_envelope(response, status.HTTP_409_CONFLICT)
        self.assertEqual(Assignment.objects.count(), 1)
