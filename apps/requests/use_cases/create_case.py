"""Application workflow for creating an operational Case."""

from apps.requests.builders import CaseCreationBuilder
from apps.requests.dto import CaseCreationDTO
from apps.requests.services import CaseCreationService


class CreateCaseUseCase:
    """Coordinate Case creation and its response DTO construction."""

    @staticmethod
    def execute(request_id: int) -> CaseCreationDTO:
        """Create one Case for a Request and return its flat DTO."""

        case, conversation = CaseCreationService.create_from_request(request_id)

        return CaseCreationBuilder.build(case, conversation)
