"""Seed the Django Groups used as platform authorization roles."""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.constants import ROLE_NAMES


class Command(BaseCommand):
    """Create the canonical RBAC Groups for development and testing."""

    help = "Create idempotent Django Groups for the platform roles."

    def handle(self, *args, **options):
        """Create missing role Groups and print the resulting status."""

        created_roles: list[str] = []
        existing_roles: list[str] = []

        with transaction.atomic():
            for role_name in ROLE_NAMES:
                _, created = Group.objects.get_or_create(name=role_name)
                (created_roles if created else existing_roles).append(role_name)

        self._print_results(created_roles, existing_roles)

    def _print_results(self, created_roles: list[str], existing_roles: list[str]):
        """Print stable role creation results."""

        self.stdout.write("Roles")
        self.stdout.write(f"Created: {', '.join(created_roles) or 'None'}")
        self.stdout.write(f"Already exists: {', '.join(existing_roles) or 'None'}")
