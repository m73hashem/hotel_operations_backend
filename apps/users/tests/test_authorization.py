from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.users.builders import AuthorizationContextBuilder
from apps.users.constants import (
    PERMISSION_CASES_CREATE,
    ROLE_RECEPTION,
)
from apps.users.dto import AuthorizationContextDTO


class AuthorizationContextBuilderTests(SimpleTestCase):
    """Tests for immutable authorization-context DTO construction."""

    def test_build_maps_loaded_employee_and_roles_without_orm_access(self):
        """The builder produces a flat immutable authorization DTO."""

        employee = SimpleNamespace(
            id=10,
            user_id=20,
            department_id=30,
            user=SimpleNamespace(is_superuser=False),
        )

        dto = AuthorizationContextBuilder.build(employee, (ROLE_RECEPTION,))

        self.assertEqual(
            dto,
            AuthorizationContextDTO(10, 20, 30, (ROLE_RECEPTION,), False),
        )
        self.assertEqual(PERMISSION_CASES_CREATE, "cases.create")
