"""Business capability for dashboard Case details retrieval."""

from apps.dashboard.selectors import CaseDetailsSelector
from apps.chat.constants import CASE_STATUS_CLOSED
from apps.employees.exceptions import CaseNotFound


class CaseDetailsService:
    """Load one existing Case and its read-only dashboard details."""

    @staticmethod
    def get_case_details(case_id: int):
        """Return the Case, timeline events, and messages for an existing Case."""

        case = CaseDetailsSelector.get_by_id(case_id)
        if case is None:
            raise CaseNotFound

        assignment = CaseDetailsSelector.get_latest_assignment(case.id)
        request_record = case.request
        request_title = request_record.title if request_record else case.subject
        request_description = (
            request_record.original_message if request_record else case.description
        )
        department = (
            case.service.department.name
            if case.service_id is not None
            else (assignment.employee.department.name if assignment else None)
        )
        assigned_employee = assignment.employee.name if assignment else None
        closed_at = case.updated_at if case.status == CASE_STATUS_CLOSED else None

        return (
            case,
            request_title,
            request_description,
            request_record.created_at if request_record else None,
            department,
            assigned_employee,
            closed_at,
            CaseDetailsSelector.list_timeline_events(case.id),
            CaseDetailsSelector.list_conversation_messages(case.id),
        )
