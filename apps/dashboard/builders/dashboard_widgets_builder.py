"""Builder for operational dashboard widget DTOs."""

from apps.dashboard.dto import (
    DashboardWidgetsDTO,
    OccupiedRoomWidgetDTO,
    RecentCaseWidgetDTO,
    RecentRequestWidgetDTO,
    RecentStayWidgetDTO,
)


class DashboardWidgetsBuilder:
    """Map already-loaded domain objects into dashboard widget DTOs."""

    @staticmethod
    def build(widgets: dict[str, list]) -> DashboardWidgetsDTO:
        """Build dashboard widget DTOs without executing ORM operations."""

        return DashboardWidgetsDTO(
            recent_cases=[
                RecentCaseWidgetDTO(
                    case_id=case.id,
                    request_title=case.request.title if case.request_id else None,
                    room_number=case.stay.room.room_number,
                    current_status=case.status,
                    priority=case.priority,
                    created_at=case.created_at,
                )
                for case in widgets["recent_cases"]
            ],
            recent_requests=[
                RecentRequestWidgetDTO(
                    request_id=case.request_id,
                    case_id=case.id,
                    request_title=case.request.title,
                    current_status=case.request.status,
                    created_at=case.request.created_at,
                )
                for case in widgets["recent_requests"]
            ],
            recent_stays=[
                RecentStayWidgetDTO(
                    stay_id=stay.id,
                    room_number=stay.room.room_number,
                    guest_name=f"{stay.guest.first_name} {stay.guest.last_name}",
                    status=stay.status,
                    check_in_date=stay.check_in,
                    check_out_date=stay.actual_check_out,
                )
                for stay in widgets["recent_stays"]
            ],
            occupied_rooms=[
                OccupiedRoomWidgetDTO(
                    room_id=room.id,
                    room_number=room.room_number,
                    room_type=room.room_type,
                    status=room.status,
                )
                for room in widgets["occupied_rooms"]
            ],
        )
