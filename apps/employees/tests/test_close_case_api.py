from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.chat.constants import CASE_STATUS_CLOSED, CASE_STATUS_COMPLETED
from apps.employees.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_RELEASED,
)
from apps.employees.models import Assignment, Department, Employee
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest, Stay
from apps.requests.models import Case, CaseTimeline, WorkOrder
from apps.rooms.models import Hotel, Room


class CloseCaseAPITests(TestCase):
    """Integration tests for the Close Case endpoint."""

    def create_case_and_assignment(
        self,
        *,
        case_status=CASE_STATUS_COMPLETED,
        assignment_status=ASSIGNMENT_STATUS_COMPLETED,
        create_assignment=True,
    ) -> tuple[Case, Assignment | None]:
        """Create completed Case context for the endpoint."""

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

    def post_close_case(self, payload):
        """Post JSON to the registered Close Case endpoint."""

        return self.client.post(
            reverse("operations:close-case"),
            data=payload,
            content_type="application/json",
        )

    def assert_error_envelope(self, response, expected_status):
        """Assert the standard error response envelope."""

        self.assertEqual(response.status_code, expected_status)
        self.assertFalse(response.data["success"])
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_closes_case_without_creating_workflow_records(self):
        """A valid request closes the Case and releases its Assignment only."""

        case, assignment = self.create_case_and_assignment()

        response = self.post_close_case({"case_id": case.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Case closed successfully.")
        self.assertEqual(
            set(response.data["data"]),
            {
                "case_id",
                "assignment_id",
                "case_status",
                "assignment_status",
                "closed_at",
            },
        )
        case.refresh_from_db()
        assignment.refresh_from_db()
        self.assertEqual(case.status, CASE_STATUS_CLOSED)
        self.assertEqual(assignment.status, ASSIGNMENT_STATUS_RELEASED)
        self.assertIsNotNone(assignment.released_at)
        self.assertEqual(WorkOrder.objects.count(), 0)
        self.assertEqual(CaseTimeline.objects.count(), 0)

    def test_rejects_missing_case_id(self):
        """The request requires a Case identifier."""

        response = self.post_close_case({})

        self.assert_error_envelope(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn("case_id", response.data["errors"])

    def test_rejects_unknown_case(self):
        """An unknown Case returns the domain not-found response."""

        response = self.post_close_case({"case_id": 999})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_case_without_assignment(self):
        """A completed Case requires an Assignment to be released."""

        case, _ = self.create_case_and_assignment(create_assignment=False)

        response = self.post_close_case({"case_id": case.id})

        self.assert_error_envelope(response, status.HTTP_404_NOT_FOUND)

    def test_rejects_assignment_that_is_not_completed(self):
        """Only COMPLETED Assignments may be released during closure."""

        case, _ = self.create_case_and_assignment(
            assignment_status=ASSIGNMENT_STATUS_RELEASED,
        )

        response = self.post_close_case({"case_id": case.id})

        self.assert_error_envelope(response, status.HTTP_409_CONFLICT)
