"""DTOs for operational dashboard widgets."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RecentCaseWidgetDTO:
    """Transport data for one recent Case widget item."""

    case_id: int
    request_title: str | None
    room_number: str
    current_status: str
    priority: str | None
    created_at: datetime


@dataclass(frozen=True)
class RecentRequestWidgetDTO:
    """Transport data for one recent Request widget item."""

    request_id: int
    case_id: int
    request_title: str
    current_status: str
    created_at: datetime


@dataclass(frozen=True)
class RecentStayWidgetDTO:
    """Transport data for one recent Stay widget item."""

    stay_id: int
    room_number: str
    guest_name: str
    status: str
    check_in_date: datetime
    check_out_date: datetime | None


@dataclass(frozen=True)
class OccupiedRoomWidgetDTO:
    """Transport data for one occupied Room widget item."""

    room_id: int
    room_number: str
    room_type: str
    status: str


@dataclass(frozen=True)
class DashboardWidgetsDTO:
    """Immutable dashboard widget payload."""

    recent_cases: list[RecentCaseWidgetDTO]
    recent_requests: list[RecentRequestWidgetDTO]
    recent_stays: list[RecentStayWidgetDTO]
    occupied_rooms: list[OccupiedRoomWidgetDTO]
