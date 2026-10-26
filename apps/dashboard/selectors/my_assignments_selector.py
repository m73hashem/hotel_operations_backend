"""Read-only selectors for an Employee's assignments."""

from django.db.models import Q

from apps.employees.models import Assignment


class MyAssignmentsSelector:
    """Load assignment history for one Employee without N+1 queries."""

    @staticmethod
    def list_for_employee(
        employee_id: int,
        *,
        search: str | None = None,
        assignment_status: str | None = None,
        case_status: str | None = None,
        priority: str | None = None,
        ordering: str | None = None,
    ):
        """Return filtered Employee assignments with required relations."""

        queryset = (
            Assignment.objects.filter(employee_id=employee_id)
            .select_related("case__request", "case__stay__room")
        )
        if search:
            queryset = queryset.filter(
                Q(case__request__title__icontains=search)
                | Q(case__stay__guest__first_name__icontains=search)
                | Q(case__stay__guest__last_name__icontains=search)
                | Q(case__stay__room__room_number__icontains=search)
                | Q(employee__name__icontains=search),
            )
        if assignment_status:
            queryset = queryset.filter(status=assignment_status)
        if case_status:
            queryset = queryset.filter(case__status=case_status)
        if priority:
            queryset = queryset.filter(case__priority=priority)

        ordering_fields = {
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "assigned_at": "assigned_at",
            "-assigned_at": "-assigned_at",
            "priority": "case__priority",
            "-priority": "-case__priority",
            "room_number": "case__stay__room__room_number",
            "-room_number": "-case__stay__room__room_number",
        }
        return queryset.order_by(ordering_fields.get(ordering, "-assigned_at"))
