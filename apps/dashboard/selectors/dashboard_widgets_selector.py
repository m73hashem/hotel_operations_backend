"""Read-only selectors for operational dashboard widgets."""

from apps.guests.models import Stay
from apps.requests.selectors import CaseDepartmentScopeSelector
from apps.rooms.constants import ROOM_STATUS_OCCUPIED
from apps.rooms.models import Room


class DashboardWidgetsSelector:
    """Load dashboard widget records with required relations eagerly loaded."""

    DEFAULT_WIDGET_LIMIT = 5

    @staticmethod
    def get_widgets(department_id: int) -> dict[str, list]:
        """Return persisted widget records for one Employee department."""

        visible_cases = CaseDepartmentScopeSelector.visible_to_department(department_id)
        recent_cases = list(
            visible_cases.select_related(
                "request",
                "stay__room",
            )
            .order_by("-created_at")
            .distinct()[: DashboardWidgetsSelector.DEFAULT_WIDGET_LIMIT],
        )
        recent_requests = list(
            visible_cases.filter(request__isnull=False)
            .select_related("request")
            .order_by("-request__created_at")
            .distinct()[: DashboardWidgetsSelector.DEFAULT_WIDGET_LIMIT],
        )
        recent_stays = list(
            Stay.objects.select_related("guest", "room").order_by("-created_at")[
                : DashboardWidgetsSelector.DEFAULT_WIDGET_LIMIT
            ],
        )
        occupied_rooms = list(
            Room.objects.filter(status=ROOM_STATUS_OCCUPIED).order_by("-updated_at")[
                : DashboardWidgetsSelector.DEFAULT_WIDGET_LIMIT
            ],
        )
        return {
            "recent_cases": recent_cases,
            "recent_requests": recent_requests,
            "recent_stays": recent_stays,
            "occupied_rooms": occupied_rooms,
        }
