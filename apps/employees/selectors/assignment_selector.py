"""Read-only selectors for Assignment business rules."""

from apps.employees.constants import (
    ACTIVE_ASSIGNMENT_STATUSES,
)
from apps.employees.models import Assignment


class AssignmentSelector:
    """Read active Assignment state for a Case."""

    @staticmethod
    def exists_active_for_case(case_id: int) -> bool:
        """Return whether the Case already has an active Assignment."""

        return Assignment.objects.filter(
            case_id=case_id,
            status__in=ACTIVE_ASSIGNMENT_STATUSES,
        ).exists()

    @staticmethod
    def get_by_id_for_acceptance(
        assignment_id: int,
        *,
        for_update: bool = False,
    ) -> Assignment | None:
        """Return an Assignment for acceptance, optionally locking its row."""

        queryset = Assignment.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=assignment_id).first()

    @staticmethod
    def get_by_id_for_completion(
        assignment_id: int,
        *,
        for_update: bool = False,
    ) -> Assignment | None:
        """Return an Assignment for completion, optionally locking its row."""

        queryset = Assignment.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=assignment_id).first()

    @staticmethod
    def get_by_case_id_for_closure(
        case_id: int,
        *,
        for_update: bool = False,
    ) -> Assignment | None:
        """Return a Case Assignment for closure, optionally locking it."""

        queryset = Assignment.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(case_id=case_id).first()
