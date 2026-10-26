"""Business capability for operational Room lists."""

from apps.employees.services import EmployeeAccessService
from apps.rooms.selectors import RoomSelector


class RoomListingService:
    """Load Rooms for an active authorized Employee."""

    @staticmethod
    def get_operational_rooms(user_id: int, **query_params):
        """Return filtered Rooms after validating the Employee context."""

        EmployeeAccessService.get_active_employee(user_id)
        return list(RoomSelector.list_for_operations(**query_params))
