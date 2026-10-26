"""Read-only aggregate selectors for operational dashboard statistics."""

from django.db.models import Count, Q

from apps.chat.constants import (
    CASE_STATUS_CLOSED,
    CASE_STATUS_IN_PROGRESS,
    CASE_STATUS_OPEN,
    REQUEST_STATUS_NEW,
)
from apps.employees.constants import ACTIVE_ASSIGNMENT_STATUSES, ASSIGNMENT_STATUS_COMPLETED
from apps.employees.models import Assignment
from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.requests.selectors import CaseDepartmentScopeSelector
from apps.rooms.constants import (
    ROOM_STATUS_AVAILABLE,
    ROOM_STATUS_OCCUPIED,
    ROOM_STATUS_OUT_OF_SERVICE,
)
from apps.rooms.models import Room


class DashboardStatisticsSelector:
    """Load department-scoped dashboard aggregates without N+1 queries."""

    @staticmethod
    def get_statistics(department_id: int, employee_id: int, today) -> dict[str, int]:
        """Return the requested operational aggregates for one Employee context."""

        visible_cases = CaseDepartmentScopeSelector.visible_to_department(department_id)
        case_statistics = visible_cases.aggregate(
            total_open_cases=Count("id", filter=Q(status=CASE_STATUS_OPEN), distinct=True),
            total_in_progress_cases=Count(
                "id",
                filter=Q(status=CASE_STATUS_IN_PROGRESS),
                distinct=True,
            ),
            total_closed_today=Count(
                "id",
                filter=Q(status=CASE_STATUS_CLOSED, updated_at__date=today),
                distinct=True,
            ),
            pending_requests=Count(
                "request_id",
                filter=Q(request__status=REQUEST_STATUS_NEW),
                distinct=True,
            ),
            active_stays=Count(
                "stay_id",
                filter=Q(stay__status=STAY_STATUS_ACTIVE),
                distinct=True,
            ),
        )
        room_statistics = Room.objects.filter(stays__cases__in=visible_cases).aggregate(
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
        assignment_statistics = Assignment.objects.filter(employee_id=employee_id).aggregate(
            my_active_assignments=Count(
                "id",
                filter=Q(status__in=ACTIVE_ASSIGNMENT_STATUSES),
            ),
            my_completed_today=Count(
                "id",
                filter=Q(status=ASSIGNMENT_STATUS_COMPLETED, updated_at__date=today),
            ),
        )
        return case_statistics | room_statistics | assignment_statistics
