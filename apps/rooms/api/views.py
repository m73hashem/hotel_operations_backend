"""API endpoints for operational Room lists."""

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.rooms.api.serializers import RoomListQuerySerializer
from apps.rooms.use_cases import ListRoomsUseCase
from apps.users.permissions import CanViewDashboard
from core.pagination import DefaultPagination
from core.responses import ApiResponse


class RoomListAPIView(APIView):
    """Return Rooms for an authorized operational Employee."""

    serializer_class = RoomListQuerySerializer
    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = ListRoomsUseCase.execute(request.user.id, **serializer.validated_data)
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(result, request, view=self)
        page_data = page if page is not None else result

        return ApiResponse.success(
            data={
                "count": paginator.page.paginator.count if page is not None else len(page_data),
                "next": paginator.get_next_link() if page is not None else None,
                "previous": paginator.get_previous_link() if page is not None else None,
                "results": [asdict(room) for room in page_data],
            },
            message="Rooms retrieved successfully.",
            status=status.HTTP_200_OK,
        )
