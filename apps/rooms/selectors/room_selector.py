"""Read-only selectors for operational Room lists."""

from django.db.models import Q

from apps.rooms.models import Room


class RoomSelector:
    """Load filtered Rooms with their Hotel relation eagerly loaded."""

    @staticmethod
    def list_for_operations(
        *,
        search: str | None = None,
        status: str | None = None,
        ordering: str | None = None,
    ):
        """Return filtered Rooms ordered by one supported database field."""

        queryset = Room.objects.select_related("hotel")
        if search:
            queryset = queryset.filter(
                Q(room_number__icontains=search)
                | Q(room_type__icontains=search)
                | Q(hotel__name__icontains=search),
            )
        if status:
            queryset = queryset.filter(status=status)

        ordering_fields = {
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "room_number": "room_number",
            "-room_number": "-room_number",
            "room_type": "room_type",
            "-room_type": "-room_type",
        }
        return queryset.order_by(ordering_fields.get(ordering, "room_number"))
