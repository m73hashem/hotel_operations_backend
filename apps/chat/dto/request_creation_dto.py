"""DTO returned after a guest creates a service request."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RequestCreationDTO:
    """Flat representation of a persisted guest Request."""

    request_id: int
    status: str
    title: str
    created_at: datetime
