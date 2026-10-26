"""Canonical read-only department ownership scope for Cases."""

from django.db.models import Prefetch, Q

from apps.employees.models import Assignment
from apps.requests.models import Case


class CaseDepartmentScopeSelector:
    """Define the persisted department visibility rule for Cases."""

    @staticmethod
    def visible_to_department(department_id: int):
        """Return Cases owned through service or assigned Employee department."""

        return Case.objects.filter(
            CaseDepartmentScopeSelector._ownership_filter(department_id),
        )

    @staticmethod
    def get_for_access(case_id: int) -> Case | None:
        """Return one Case with the persisted facts required for access decisions."""

        return (
            Case.objects.select_related("service__department")
            .prefetch_related(
                Prefetch(
                    "assignments",
                    queryset=Assignment.objects.select_related("employee__department"),
                    to_attr="department_scope_assignments",
                ),
            )
            .filter(id=case_id)
            .first()
        )

    @staticmethod
    def is_visible_to_department(case: Case, department_id: int) -> bool:
        """Return whether a loaded Case is owned by the given department."""

        if case.service_id is not None and case.service.department_id == department_id:
            return True

        return any(
            assignment.employee.department_id == department_id
            for assignment in case.department_scope_assignments
        )

    @staticmethod
    def _ownership_filter(department_id: int) -> Q:
        """Return the canonical ORM predicate for department Case ownership."""

        return Q(service__department_id=department_id) | Q(
            assignments__employee__department_id=department_id,
        )
