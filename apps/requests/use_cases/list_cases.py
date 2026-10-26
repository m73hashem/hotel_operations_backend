"""Application workflow for operational Case list retrieval."""

from apps.requests.builders import CaseListBuilder
from apps.requests.dto import CaseListItemDTO
from apps.requests.services.case_listing_service import CaseListingService


class ListCasesUseCase:
    """Coordinate visible Case retrieval and DTO mapping."""

    @staticmethod
    def execute(user_id: int, **query_params) -> tuple[CaseListItemDTO, ...]:
        """Return immutable Case list DTOs for one Employee context."""

        cases = CaseListingService.get_visible_cases(user_id, **query_params)
        return CaseListBuilder.build(cases)
