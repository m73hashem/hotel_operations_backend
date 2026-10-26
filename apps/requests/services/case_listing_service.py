"""Business capability for visible operational Case lists."""

from apps.employees.services import EmployeeAccessService
from apps.requests.selectors import CaseSelector


class CaseListingService:
    """Load Cases available to the authenticated Employee department."""

    @staticmethod
    def get_visible_cases(user_id: int, **query_params):
        """Return department-visible Cases for an active Employee."""

        employee = EmployeeAccessService.get_active_employee(user_id)
        return list(CaseSelector.list_for_department(employee.department_id, **query_params))
