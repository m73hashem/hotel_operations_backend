"""Business capability for operational Request lists."""

from apps.employees.services import EmployeeAccessService
from apps.requests.selectors import RequestSelector


class RequestListingService:
    """Load Requests for an active operational Employee."""

    @staticmethod
    def get_operational_requests(user_id: int, **query_params):
        """Return Requests after validating the active Employee context."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return list(
            RequestSelector.list_for_operations(
                employee.department_id,
                **query_params,
            ),
        )
