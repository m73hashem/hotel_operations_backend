"""Read-only selectors for Employees used by Assignment operations."""

from apps.employees.models import Employee


class EmployeeSelector:
    """Load Employees required for Case assignment."""

    @staticmethod
    def get_by_id_for_assignment(employee_id: int) -> Employee | None:
        """Return the Employee identified for a Case assignment."""

        return Employee.objects.filter(id=employee_id).first()

    @staticmethod
    def get_by_user_id_for_authentication(user_id: int) -> Employee | None:
        """Return the Employee profile for an authenticated User."""

        return (
            Employee.objects.select_related("user", "department")
            .filter(user_id=user_id)
            .first()
        )
