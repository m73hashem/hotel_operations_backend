"""Business capability for starting work on accepted Assignments."""

from django.db import transaction

from apps.chat.constants import CASE_STATUS_IN_PROGRESS, CASE_STATUS_OPEN
from apps.employees.constants import (
    ASSIGNMENT_STATUS_ACCEPTED,
    ASSIGNMENT_STATUS_IN_PROGRESS,
)
from apps.employees.exceptions import (
    AssignmentNotAccepted,
    AssignmentNotFound,
    CaseNotFound,
    CaseNotOpen,
)
from apps.employees.models import Assignment
from apps.employees.selectors import AssignmentSelector
from apps.requests.models import Case
from apps.requests.selectors import CaseSelector


class WorkStartService:
    """Start work by atomically transitioning an Assignment and its Case."""

    @staticmethod
    def start_work(assignment_id: int) -> tuple[Assignment, Case]:
        """Transition the accepted Assignment and open Case to in-progress."""

        with transaction.atomic():
            assignment = AssignmentSelector.get_by_id_for_acceptance(
                assignment_id,
                for_update=True,
            )
            if assignment is None:
                raise AssignmentNotFound

            if assignment.status != ASSIGNMENT_STATUS_ACCEPTED:
                raise AssignmentNotAccepted

            case = CaseSelector.get_by_id_for_start_work(
                assignment.case_id,
                for_update=True,
            )
            if case is None:
                raise CaseNotFound

            if case.status != CASE_STATUS_OPEN:
                raise CaseNotOpen

            assignment.status = ASSIGNMENT_STATUS_IN_PROGRESS
            assignment.save(update_fields=["status", "updated_at"])
            case.status = CASE_STATUS_IN_PROGRESS
            case.save(update_fields=["status", "updated_at"])

            return assignment, case
