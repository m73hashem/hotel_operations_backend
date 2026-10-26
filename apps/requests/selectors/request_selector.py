"""Read-only selectors for Requests used by Case creation."""

from django.db.models import Q

from apps.requests.selectors.case_department_scope_selector import CaseDepartmentScopeSelector
from apps.chat.models import Request


class RequestSelector:
    """Load Requests required to create operational Cases."""

    @staticmethod
    def get_by_id_for_case(
        request_id: int,
        *,
        for_update: bool = False,
    ) -> Request | None:
        """Return a Request with its Stay loaded, optionally locked for creation."""

        queryset = Request.objects.select_related("stay")
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=request_id).first()

    @staticmethod
    def list_for_operations(
        department_id: int,
        *,
        search: str | None = None,
        status: str | None = None,
        ordering: str | None = None,
    ):
        """Return Requests with their client-facing list relations loaded."""

        visible_request_ids = CaseDepartmentScopeSelector.visible_to_department(
            department_id,
        ).values("request_id")
        queryset = Request.objects.filter(id__in=visible_request_ids).select_related("guest", "room")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(original_message__icontains=search)
                | Q(guest__first_name__icontains=search)
                | Q(guest__last_name__icontains=search)
                | Q(room__room_number__icontains=search),
            )
        if status:
            queryset = queryset.filter(status=status)

        ordering_fields = {
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "title": "title",
            "-title": "-title",
            "room_number": "room__room_number",
            "-room_number": "-room__room_number",
        }
        return queryset.order_by(ordering_fields.get(ordering, "-created_at"))
