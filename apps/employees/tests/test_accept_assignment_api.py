from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.employees.constants import (
    ASSIGNMENT_STATUS_ACCEPTED,
    ASSIGNMENT_STATUS_ASSIGNED,
)
from apps.employees.models import Assignment, Department, Employee
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case, CaseTimeline, WorkOrder
from apps.rooms.models import Hotel, Room


class AcceptAssignmentAPITests(TestCase):
    """Integration tests for the Accept Assignment endpoint."""

    def create_assignment(self, *, status_value=ASSIGNMENT_STATUS_ASSIGNED) -> Assignment:
        """Create an Assignment and all required domain context."""

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
            status=status_value,
            assigned_at=timezone.now(),
        )

    def post_accept_assignment(self, payload):
        """Post JSON to the registered Accept Assignment endpoint."""

        return self.client.post(
            reverse("operations:accept-assignment"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_accepts_assignment_without_creating_workflow_records(self):
        """A valid request changes only the Assignment state."""

        assignment = self.create_assignment()
        case_status = assignment.case.status

        response = self.post_accept_assignment({"assignment_id": assignment.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Assignment accepted successfully.")
        self.assertEqual(
            set(response.data["data"]),
            {"assignment_id", "case_id", "employee_id", "status", "accepted_at"},
        )
        assignment.refresh_from_db()
        assignment.case.refresh_from_db()
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_ACCEPTED)
        self.assertIsNotNone(assignment.accepted_at)
        self.assertEqual(assignment.case.status, case_status)
        self.assertEqual(WorkOrder.objects.count(), 0)
        self.assertEqual(CaseTimeline.objects.count(), 0)

    def test_rejects_missing_assignment_id(self):
        """The request requires an Assignment identifier."""

        response = self.post_accept_assignment({})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("assignment_id", response.data["errors"])

    def test_rejects_unknown_assignment(self):
        """An unknown Assignment returns the domain not-found response."""

        response = self.post_accept_assignment({"assignment_id": 999})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_assignment_that_is_not_assigned(self):
        """An accepted Assignment cannot be accepted again."""

        assignment = self.create_assignment(status_value=ASSIGNMENT_STATUS_ACCEPTED)

        response = self.post_accept_assignment({"assignment_id": assignment.id})

        self.assert_error_envelope(response, status.HTTP_409_CONFLICT)
