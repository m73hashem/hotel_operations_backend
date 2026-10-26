"""Business capability for closing completed Cases."""

from django.db import transaction
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
from apps.employees.models import Assignment
from apps.employees.selectors import AssignmentSelector
from apps.requests.models import Case
from apps.requests.selectors import CaseSelector


class CaseClosureService:
    """Close a Case and release its completed Assignment atomically."""

    @staticmethod
    def close_case(case_id: int) -> tuple[Case, Assignment]:
        """Transition one completed Case and Assignment to their terminal states."""

        with transaction.atomic():
            case = CaseSelector.get_by_id_for_closure(case_id, for_update=True)
            if case is None:
                raise CaseNotFound

            if case.status != CASE_STATUS_COMPLETED:
                raise CaseNotCompleted

            assignment = AssignmentSelector.get_by_case_id_for_closure(
                case.id,
                for_update=True,
            )
            if assignment is None:
                raise AssignmentNotFound

            if assignment.status != ASSIGNMENT_STATUS_COMPLETED:
                raise AssignmentNotCompleted

            assignment.status = ASSIGNMENT_STATUS_RELEASED
            assignment.released_at = timezone.now()
            assignment.save(update_fields=["status", "released_at", "updated_at"])
            case.status = CASE_STATUS_CLOSED
            case.save(update_fields=["status", "updated_at"])

            return case, assignment
