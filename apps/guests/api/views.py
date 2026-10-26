from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.guests.api.serializers import (
    GuestListQuerySerializer,
    GuestSerializer,
    StayListQuerySerializer,
)
from apps.guests.use_cases import (
    CreateGuestUseCase,
    DeleteGuestUseCase,
    ListGuestsUseCase,
    ListStaysUseCase,
    RetrieveGuestUseCase,
    UpdateGuestUseCase,
)
from apps.users.permissions import CanListOrManageGuests, CanViewDashboard
from core.pagination import DefaultPagination
from core.responses import ApiResponse


class GuestListCreateAPIView(APIView):
    """List and create Guests through Guest use cases."""

    serializer_class = GuestSerializer
    query_serializer_class = GuestListQuerySerializer
    permission_classes = [IsAuthenticated, CanListOrManageGuests]

    def get(self, request, *args, **kwargs):
        serializer = self.query_serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = ListGuestsUseCase.execute(request.user.id, **serializer.validated_data)
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result, request, view=self)
        page_data = page if page is not None else result

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(guest) for guest in page_data],
            },
            message="Guests retrieved successfully",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = CreateGuestUseCase.execute(serializer.validated_data)

        return ApiResponse.success(
            data=asdict(result),
            message="Guest created successfully",
            status=status.HTTP_201_CREATED,
        )


class GuestRetrieveUpdateDestroyAPIView(APIView):
    """Retrieve, update, and delete Guests through Guest use cases."""

    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request, pk, *args, **kwargs):
        result = RetrieveGuestUseCase.execute(pk)

        return ApiResponse.success(
            data=asdict(result),
            message="Guest retrieved successfully",
        )

    def put(self, request, pk, *args, **kwargs):
        return self._update(request, pk)

    def patch(self, request, pk, *args, **kwargs):
        return self._update(request, pk)

    def _update(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = UpdateGuestUseCase.execute(pk, serializer.validated_data)

        return ApiResponse.success(
            data=asdict(result),
            message="Guest updated successfully",
        )

    def delete(self, request, pk, *args, **kwargs):
        DeleteGuestUseCase.execute(pk)

        return ApiResponse.success(
            message="Guest deleted successfully",
        )


class StayListAPIView(APIView):
    """Return operational Stays for an authorized Employee."""

    serializer_class = StayListQuerySerializer
    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = ListStaysUseCase.execute(request.user.id, **serializer.validated_data)
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result, request, view=self)
        page_data = page if page is not None else result

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(stay) for stay in page_data],
            },
            message="Stays retrieved successfully.",
            status=status.HTTP_200_OK,
        )
    
