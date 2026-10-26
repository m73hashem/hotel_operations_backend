"""Read-only aggregate selectors for operational dashboard metrics."""

from django.db.models import Count, Q

from apps.chat.constants import CASE_STATUS_CLOSED, CASE_STATUS_IN_PROGRESS, CASE_STATUS_OPEN
from apps.employees.constants import ACTIVE_ASSIGNMENT_STATUSES
from apps.employees.models import Assignment
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.requests.selectors import CaseDepartmentScopeSelector
from apps.rooms.constants import (
    ROOM_STATUS_AVAILABLE,
    ROOM_STATUS_OCCUPIED,
    ROOM_STATUS_OUT_OF_SERVICE,
)
from apps.rooms.models import Room


class DashboardMetricsSelector:
    """Load department-scoped operational metrics without N+1 queries."""

    @staticmethod
    def get_metrics(department_id: int) -> dict[str, int]:
        """Return metrics derived only from the certified department Case scope."""

        visible_cases = CaseDepartmentScopeSelector.visible_to_department(department_id)
        case_metrics = visible_cases.aggregate(
            open_cases=Count("id", filter=Q(status=CASE_STATUS_OPEN), distinct=True),
            in_progress_cases=Count(
                "id",
                filter=Q(status=CASE_STATUS_IN_PROGRESS),
                distinct=True,
            ),
            closed_cases=Count(
                "id",
                filter=Q(status=CASE_STATUS_CLOSED),
                distinct=True,
            ),
            active_stays=Count(
                "stay_id",
                filter=Q(stay__status=STAY_STATUS_ACTIVE),
                distinct=True,
            ),
        )
        assignment_metrics = Assignment.objects.filter(
            case__in=visible_cases,
        ).aggregate(
            active_assignments=Count(
                "id",
                filter=Q(status__in=ACTIVE_ASSIGNMENT_STATUSES),
                distinct=True,
            ),
        )
        room_metrics = Room.objects.filter(stays__cases__in=visible_cases).aggregate(
            occupied_rooms=Count(
                "id",
                filter=Q(status=ROOM_STATUS_OCCUPIED),
                distinct=True,
            ),
            available_rooms=Count(
                "id",
                filter=Q(status=ROOM_STATUS_AVAILABLE),
                distinct=True,
            ),
            out_of_service_rooms=Count(
                "id",
                filter=Q(status=ROOM_STATUS_OUT_OF_SERVICE),
                distinct=True,
            ),
        )
        return case_metrics | assignment_metrics | room_metrics
