"""Read-only selectors for department Case queues."""

from django.db.models import Q

from apps.chat.constants import CASE_STATUS_ASSIGNED, CASE_STATUS_OPEN
from apps.requests.selectors import CaseDepartmentScopeSelector


class DepartmentQueueSelector:
    """Load queued Cases belonging to one department without N+1 queries."""

    @staticmethod
    def list_for_department(
        department_id: int,
        *,
        search: str | None = None,
        case_status: str | None = None,
        priority: str | None = None,
        ordering: str | None = None,
    ):
        """Return filtered open and assigned Cases for one department."""

        queryset = (
            CaseDepartmentScopeSelector.visible_to_department(department_id)
            .filter(
                status__in=(CASE_STATUS_OPEN, CASE_STATUS_ASSIGNED),
            )
            .select_related("request", "stay__room")
        )
        if search:
            queryset = queryset.filter(
                Q(request__title__icontains=search)
                | Q(stay__guest__first_name__icontains=search)
                | Q(stay__guest__last_name__icontains=search)
                | Q(stay__room__room_number__icontains=search)
                | Q(assignments__employee__name__icontains=search),
            )
        if case_status:
            queryset = queryset.filter(status=case_status)
        if priority:
            queryset = queryset.filter(priority=priority)

        ordering_fields = {
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "assigned_at": "assignments__assigned_at",
            "-assigned_at": "-assignments__assigned_at",
            "priority": "priority",
            "-priority": "-priority",
            "room_number": "stay__room__room_number",
            "-room_number": "-stay__room__room_number",
        }
        return queryset.order_by(ordering_fields.get(ordering, "-created_at")).distinct()
