"""Business capability for operational Stay lists."""

from apps.employees.services import EmployeeAccessService
from apps.guests.selectors.stay_selector import StaySelector


class StayListingService:
    """Load Stays for an active operational Employee."""

    @staticmethod
    def get_operational_stays(user_id: int, **query_params):
        """Return filtered Stays after validating the Employee context."""

        EmployeeAccessService.get_active_employee(user_id)
        return list(StaySelector.list_for_operations(**query_params))
