"""Application workflow for dashboard Case details retrieval."""

from apps.dashboard.builders import CaseDetailsBuilder
from apps.dashboard.dto import CaseDetailsDTO
from apps.dashboard.services import CaseDetailsService


class CaseDetailsUseCase:
    """Coordinate Case details retrieval and DTO construction."""

    @staticmethod
    def execute(case_id: int) -> CaseDetailsDTO:
        """Return the requested Case details DTO."""

        (
            case,
            request_title,
            request_description,
            request_created_at,
            department,
            assigned_employee,
            closed_at,
            timeline_events,
            messages,
        ) = CaseDetailsService.get_case_details(case_id)
        return CaseDetailsBuilder.build(
            case,
            request_title,
            request_description,
            request_created_at,
            department,
            assigned_employee,
            closed_at,
            timeline_events,
            messages,
        )
