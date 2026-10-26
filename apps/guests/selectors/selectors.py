from django.db.models import Q

from apps.guests.constants import STAY_STATUS_ACTIVE
from apps.guests.models import Guest


class GuestSelector:
    """Load Guests required by Guest use cases."""

    @staticmethod
    def list(
        *,
        search: str | None = None,
        active_stay: bool | None = None,
        ordering: str | None = None,
    ):
        """Return filtered Guests with database ordering."""

        queryset = Guest.objects.all()
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(phone__icontains=search)
                | Q(email__icontains=search),
            )
        if active_stay is True:
            queryset = queryset.filter(stays__status=STAY_STATUS_ACTIVE)
        if active_stay is False:
            queryset = queryset.exclude(stays__status=STAY_STATUS_ACTIVE)

        ordering_fields = {
            "created_at": ("created_at",),
            "-created_at": ("-created_at",),
            "updated_at": ("updated_at",),
            "-updated_at": ("-updated_at",),
            "first_name": ("first_name",),
            "-first_name": ("-first_name",),
            "last_name": ("last_name",),
            "-last_name": ("-last_name",),
            "full_name": ("first_name", "last_name"),
            "-full_name": ("-first_name", "-last_name"),
        }
        ordering_fields = ordering_fields.get(ordering, ("-created_at",))
        return queryset.order_by(*ordering_fields).distinct()

    @staticmethod
    def get(guest_id: int) -> Guest | None:
        """Return a Guest or None when it does not exist."""

        return Guest.objects.filter(pk=guest_id).first()
