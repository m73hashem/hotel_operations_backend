"""DTOs returned by Guest use cases."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GuestDTO:
    """Flat client-facing representation of a Guest."""

    id: int
    created_at: datetime
    updated_at: datetime
    first_name: str
    last_name: str
    phone: str
    email: str
    language: str
