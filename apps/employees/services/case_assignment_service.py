"""Business capability for assigning operational Cases."""

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.employees.constants import ASSIGNMENT_STATUS_ASSIGNED
from apps.employees.exceptions import (
    CaseAlreadyAssigned,
    CaseNotFound,
    EmployeeNotFound,
)
from apps.employees.models import Assignment
from apps.employees.selectors import AssignmentSelector, EmployeeSelector
from apps.requests.selectors import CaseSelector


class CaseAssignmentService:
    """Assign one Employee to a Case without starting execution workflows."""

    @staticmethod
    def assign_case(case_id: int, employee_id: int) -> Assignment:
        """Create one active Assignment after validating the Case and Employee."""

        with transaction.atomic():
            case = CaseSelector.get_by_id_for_assignment(case_id, for_update=True)
            if case is None:
                raise CaseNotFound

            employee = EmployeeSelector.get_by_id_for_assignment(employee_id)
            if employee is None:
                raise EmployeeNotFound

            if AssignmentSelector.exists_active_for_case(case.id):
                raise CaseAlreadyAssigned

            try:
                with transaction.atomic():
                    return Assignment.objects.create(
                        case=case,
                        employee=employee,
                        status=ASSIGNMENT_STATUS_ASSIGNED,
                        assigned_at=timezone.now(),
                    )
            except IntegrityError as error:
                raise CaseAlreadyAssigned from error
