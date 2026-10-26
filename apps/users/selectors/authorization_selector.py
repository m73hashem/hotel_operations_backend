"""Read-only selectors for authorization facts."""

from apps.employees.models import Assignment, Employee
from apps.users.constants import ROLE_NAMES


class AuthorizationSelector:
    """Load only the persisted facts required for RBAC decisions."""

    @staticmethod
    def get_employee_and_roles(user_id: int) -> tuple[Employee, tuple[str, ...]] | None:
        """Return an Employee with recognized Django Group role names."""

        employee = (
            Employee.objects.select_related("user", "department")
            .prefetch_related("user__groups")
            .filter(user_id=user_id)
            .first()
        )
        if employee is None:
            return None

        roles = tuple(
            group.name
            for group in employee.user.groups.all()
            if group.name in ROLE_NAMES
        )
        return employee, roles

    @staticmethod
    def get_assignment_for_access(assignment_id: int) -> Assignment | None:
        """Return an Assignment with ownership and department facts loaded."""

        return (
            Assignment.objects.select_related("employee__user", "employee__department")
            .filter(id=assignment_id)
            .first()
        )
