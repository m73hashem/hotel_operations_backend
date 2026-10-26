"""Seed complete Employee accounts for every platform authorization role."""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.employees.constants import EMPLOYEE_STATUS_ACTIVE
from apps.employees.models import Department, Employee
from apps.users.constants import (
    ROLE_ADMIN,
    ROLE_HOUSEKEEPING,
    ROLE_KITCHEN,
    ROLE_MAINTENANCE,
    ROLE_RECEPTION,
    ROLE_SUPERVISOR,
)
from apps.users.models import User

DEMO_PASSWORD = "12345678"
DEMO_DEPARTMENT_STATUS = "ACTIVE"

DEMO_USERS = (
    {
        "username": "admin",
        "role": ROLE_ADMIN,
        "department": "Management",
        "name": "Demo Admin",
        "phone": "+966500000001",
        "employee_number": "DEMO-ADMIN",
    },
    {
        "username": "reception",
        "role": ROLE_RECEPTION,
        "department": "Reception",
        "name": "Demo Reception",
        "phone": "+966500000002",
        "employee_number": "DEMO-RECEPTION",
    },
    {
        "username": "housekeeping",
        "role": ROLE_HOUSEKEEPING,
        "department": "Housekeeping",
        "name": "Demo Housekeeping",
        "phone": "+966500000003",
        "employee_number": "DEMO-HOUSEKEEPING",
    },
    {
        "username": "maintenance",
        "role": ROLE_MAINTENANCE,
        "department": "Maintenance",
        "name": "Demo Maintenance",
        "phone": "+966500000004",
        "employee_number": "DEMO-MAINTENANCE",
    },
    {
        "username": "kitchen",
        "role": ROLE_KITCHEN,
        "department": "Kitchen",
        "name": "Demo Kitchen",
        "phone": "+966500000005",
        "employee_number": "DEMO-KITCHEN",
    },
    {
        "username": "supervisor",
        "role": ROLE_SUPERVISOR,
        "department": "Management",
        "name": "Demo Supervisor",
        "phone": "+966500000006",
        "employee_number": "DEMO-SUPERVISOR",
    },
)


class Command(BaseCommand):
    """Create idempotent demo Users, Employees, Departments, and Groups."""

    help = "Create complete demo Employee accounts for all platform roles."

    def handle(self, *args, **options):
        """Create or reuse all demo authorization accounts."""

        results = {
            "Roles": ([], []),
            "Departments": ([], []),
            "Users": ([], []),
            "Employees": ([], []),
        }

        with transaction.atomic():
            groups = self._seed_groups(results)
            departments = self._seed_departments(results)
            self._seed_users_and_employees(groups, departments, results)

        self._print_results(results)

    def _seed_groups(self, results: dict[str, tuple[list[str], list[str]]]) -> dict[str, Group]:
        """Create or reuse the Groups required by demo Employees."""

        groups = {}
        for account in DEMO_USERS:
            role_name = account["role"]
            group, created = Group.objects.get_or_create(name=role_name)
            groups[role_name] = group
            self._record(results["Roles"], role_name, created)
        return groups

    def _seed_departments(
        self,
        results: dict[str, tuple[list[str], list[str]]],
    ) -> dict[str, Department]:
        """Create or reuse the Departments required by demo Employees."""

        departments = {}
        for department_name in dict.fromkeys(account["department"] for account in DEMO_USERS):
            department, created = Department.objects.get_or_create(
                name=department_name,
                defaults={"status": DEMO_DEPARTMENT_STATUS},
            )
            departments[department_name] = department
            self._record(results["Departments"], department_name, created)
        return departments

    def _seed_users_and_employees(
        self,
        groups: dict[str, Group],
        departments: dict[str, Department],
        results: dict[str, tuple[list[str], list[str]]],
    ) -> None:
        """Create or update each complete demo authorization account."""

        for account in DEMO_USERS:
            username = account["username"]
            email = f"{username}@hotel.local"
            user, created = User.objects.update_or_create(
                username=username,
                defaults={"email": email, "is_active": True},
            )
            if not user.check_password(DEMO_PASSWORD):
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=["password", "updated_at"])
            self._record(results["Users"], username, created)

            user.groups.remove(
                *Group.objects.filter(name__in=groups).exclude(name=account["role"]),
            )
            user.groups.add(groups[account["role"]])

            employee, employee_created = Employee.objects.update_or_create(
                user=user,
                defaults={
                    "department": departments[account["department"]],
                    "employee_number": account["employee_number"],
                    "name": account["name"],
                    "phone": account["phone"],
                    "email": email,
                    "status": EMPLOYEE_STATUS_ACTIVE,
                },
            )
            self._record(results["Employees"], employee.employee_number, employee_created)

    @staticmethod
    def _record(result: tuple[list[str], list[str]], value: str, created: bool) -> None:
        """Record one created or reused entity for command output."""

        (result[0] if created else result[1]).append(value)

    def _print_results(self, results: dict[str, tuple[list[str], list[str]]]) -> None:
        """Print stable seed results grouped by entity type."""

        for heading, (created, existing) in results.items():
            self.stdout.write(heading)
            self.stdout.write(f"Created: {', '.join(created) or 'None'}")
            self.stdout.write(f"Already exists: {', '.join(existing) or 'None'}")
