"""Read-only selectors for dashboard summary facts."""

from django.db.models import Count, Q

from apps.chat.constants import (
    CASE_STATUS_ASSIGNED,
    CASE_STATUS_COMPLETED,
    CASE_STATUS_IN_PROGRESS,
    CASE_STATUS_OPEN,
)
from apps.employees.constants import ACTIVE_ASSIGNMENT_STATUSES
from apps.employees.models import Assignment
from apps.requests.selectors import CaseDepartmentScopeSelector


class DashboardSummarySelector:
    """Load optimized aggregate facts for an Employee dashboard summary."""

    @staticmethod
    def get_statistics(department_id: int, employee_id: int, today) -> dict[str, int]:
        """Return department workload and personal active-assignment counts."""

        department_cases = CaseDepartmentScopeSelector.visible_to_department(department_id)
        counts = department_cases.aggregate(
            new_cases_count=Count("id", filter=Q(status=CASE_STATUS_OPEN), distinct=True),
            assigned_cases_count=Count(
                "id",
                filter=Q(status=CASE_STATUS_ASSIGNED),
                distinct=True,
            ),
            in_progress_cases_count=Count(
                "id",
                filter=Q(status=CASE_STATUS_IN_PROGRESS),
                distinct=True,
            ),
            completed_today_count=Count(
                "id",
                filter=Q(status=CASE_STATUS_COMPLETED, completed_at__date=today),
                distinct=True,
            ),
        )
        counts["my_active_assignments_count"] = Assignment.objects.filter(
            employee_id=employee_id,
            status__in=ACTIVE_ASSIGNMENT_STATUSES,
        ).count()
        return counts
