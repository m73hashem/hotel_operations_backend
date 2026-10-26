"""Read-only selectors for operational Stay lists."""

from django.db.models import Q

from apps.guests.models import Stay


class StaySelector:
    """Load filtered Stays with all list relations eagerly loaded."""

    @staticmethod
    def list_for_operations(
        *,
        search: str | None = None,
        status: str | None = None,
        ordering: str | None = None,
    ):
        """Return filtered Stays ordered by one supported database field."""

        queryset = Stay.objects.select_related("guest", "room")
        if search:
            queryset = queryset.filter(
                Q(guest__first_name__icontains=search)
                | Q(guest__last_name__icontains=search)
                | Q(room__room_number__icontains=search),
            )
        if status:
            queryset = queryset.filter(status=status)

        ordering_fields = {
            "check_in": "check_in",
            "-check_in": "-check_in",
            "expected_check_out": "expected_check_out",
            "-expected_check_out": "-expected_check_out",
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "room_number": "room__room_number",
            "-room_number": "-room__room_number",
        }
        return queryset.order_by(ordering_fields.get(ordering, "-check_in"))
