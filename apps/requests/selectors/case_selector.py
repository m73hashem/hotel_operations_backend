"""Read-only selectors for operational Cases."""

from django.db.models import Q

from apps.requests.selectors.case_department_scope_selector import CaseDepartmentScopeSelector
from apps.requests.models import Case


class CaseSelector:
    """Read Case existence for Request creation rules."""

    @staticmethod
    def exists_for_request(request_id: int) -> bool:
        """Return whether the Request already has a Case."""

        return Case.objects.filter(request_id=request_id).exists()

    @staticmethod
    def get_by_id_for_assignment(
        case_id: int,
        *,
        for_update: bool = False,
    ) -> Case | None:
        """Return a Case for assignment, optionally locking it for creation."""

        queryset = Case.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=case_id).first()

    @staticmethod
    def get_by_id_for_start_work(
        case_id: int,
        *,
        for_update: bool = False,
    ) -> Case | None:
        """Return a Case for work start, optionally locking its row."""

        queryset = Case.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=case_id).first()

    @staticmethod
    def get_by_id_for_complete_work(
        case_id: int,
        *,
        for_update: bool = False,
    ) -> Case | None:
        """Return a Case for work completion, optionally locking its row."""

        queryset = Case.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=case_id).first()

    @staticmethod
    def get_by_id_for_closure(
        case_id: int,
        *,
        for_update: bool = False,
    ) -> Case | None:
        """Return a Case for closure, optionally locking its row."""

        queryset = Case.objects.all()
        if for_update:
            queryset = queryset.select_for_update()

        return queryset.filter(id=case_id).first()

    @staticmethod
    def list_for_department(
        department_id: int,
        *,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        department: int | None = None,
        ordering: str | None = None,
    ):
        """Return department-visible Cases with list relations loaded."""

        queryset = CaseDepartmentScopeSelector.visible_to_department(department_id).select_related(
            "service__department",
            "stay__guest",
            "stay__room",
        )
        if search:
            queryset = queryset.filter(
                Q(subject__icontains=search)
                | Q(description__icontains=search)
                | Q(stay__guest__first_name__icontains=search)
                | Q(stay__guest__last_name__icontains=search)
                | Q(stay__room__room_number__icontains=search),
            )
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if department:
            queryset = queryset.filter(service__department_id=department)

        ordering_fields = {
            "created_at": "created_at",
            "-created_at": "-created_at",
            "updated_at": "updated_at",
            "-updated_at": "-updated_at",
            "priority": "priority",
            "-priority": "-priority",
            "room_number": "stay__room__room_number",
            "-room_number": "-stay__room__room_number",
        }
        return queryset.order_by(ordering_fields.get(ordering, "-created_at")).distinct()
