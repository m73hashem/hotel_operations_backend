"""Internal immutable authorization context DTO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizationContextDTO:
    """Authorization facts derived from one loaded Employee profile."""

    employee_id: int
    user_id: int
    department_id: int
    roles: tuple[str, ...]
    is_superuser: bool
