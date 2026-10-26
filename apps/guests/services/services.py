from collections.abc import Mapping

from apps.guests.exceptions import GuestNotFound
from apps.guests.models import Guest
from apps.guests.selectors.selectors import GuestSelector
from apps.employees.services import EmployeeAccessService


class GuestService:
    """Create, retrieve, update, and delete Guests."""

    @staticmethod
    def list_guests(user_id: int, **query_params) -> list[Guest]:
        """Return all Guests for response construction."""

        EmployeeAccessService.get_active_employee(user_id)
        return list(GuestSelector.list(**query_params))

    @staticmethod
    def get_guest(guest_id: int) -> Guest:
        """Return one Guest or raise the domain not-found exception."""

        guest = GuestSelector.get(guest_id)
        if guest is None:
            raise GuestNotFound

        return guest

    @staticmethod
    def create_guest(validated_data: Mapping[str, object]) -> Guest:
        """Persist one Guest from serializer-validated input."""

        return Guest.objects.create(**validated_data)

    @classmethod
    def update_guest(
        cls,
        guest_id: int,
        validated_data: Mapping[str, object],
    ) -> Guest:
        """Update one existing Guest from serializer-validated input."""

        guest = cls.get_guest(guest_id)

        for field, value in validated_data.items():
            setattr(guest, field, value)

        guest.save()

        return guest

    @classmethod
    def delete_guest(cls, guest_id: int) -> None:
        """Delete one existing Guest."""

        cls.get_guest(guest_id).delete()
