"""Business capability for completing work on in-progress Assignments."""

from django.db import transaction

from apps.chat.constants import CASE_STATUS_COMPLETED, CASE_STATUS_IN_PROGRESS
from apps.employees.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_IN_PROGRESS,
)
from apps.employees.exceptions import (
    AssignmentNotFound,
    AssignmentNotInProgress,
    CaseNotFound,
    CaseNotInProgress,
)
from apps.employees.models import Assignment
from apps.employees.selectors import AssignmentSelector
from apps.requests.models import Case
from apps.requests.selectors import CaseSelector


class WorkCompletionService:
    """Complete work by atomically transitioning an Assignment and its Case."""

    @staticmethod
    def complete_work(assignment_id: int) -> tuple[Assignment, Case]:
        """Transition the in-progress Assignment and Case to completed."""

        with transaction.atomic():
            assignment = AssignmentSelector.get_by_id_for_completion(
                assignment_id,
                for_update=True,
            )
            if assignment is None:
                raise AssignmentNotFound

            if assignment.status != ASSIGNMENT_STATUS_IN_PROGRESS:
                raise AssignmentNotInProgress

            case = CaseSelector.get_by_id_for_complete_work(
                assignment.case_id,
                for_update=True,
            )
            if case is None:
                raise CaseNotFound

            if case.status != CASE_STATUS_IN_PROGRESS:
                raise CaseNotInProgress

            assignment.status = ASSIGNMENT_STATUS_COMPLETED
            assignment.save(update_fields=["status", "updated_at"])
            case.status = CASE_STATUS_COMPLETED
            case.save(update_fields=["status", "updated_at"])

            return assignment, case
