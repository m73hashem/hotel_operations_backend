"""Business capability for accepting Case Assignments."""

from django.db import transaction
from django.utils import timezone

from apps.employees.constants import (
    ASSIGNMENT_STATUS_ACCEPTED,
    ASSIGNMENT_STATUS_ASSIGNED,
)
from apps.employees.exceptions import AssignmentNotAssigned, AssignmentNotFound
from apps.employees.models import Assignment
from apps.employees.selectors import AssignmentSelector


class AssignmentAcceptanceService:
    """Accept an Assignment without starting execution workflows."""

    @staticmethod
    def accept_assignment(assignment_id: int) -> Assignment:
        """Transition an assigned Assignment to accepted state."""

        with transaction.atomic():
            assignment = AssignmentSelector.get_by_id_for_acceptance(
                assignment_id,
                for_update=True,
            )
            if assignment is None:
                raise AssignmentNotFound

            if assignment.status != ASSIGNMENT_STATUS_ASSIGNED:
                raise AssignmentNotAssigned

            assignment.status = ASSIGNMENT_STATUS_ACCEPTED
            assignment.accepted_at = timezone.now()
            assignment.save(update_fields=["status", "accepted_at", "updated_at"])

            return assignment
