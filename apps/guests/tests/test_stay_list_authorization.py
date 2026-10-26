"""Unit tests for operational Stay list authorization configuration."""

from django.test import SimpleTestCase
from rest_framework.permissions import IsAuthenticated

from apps.guests.api.views import StayListAPIView
from apps.users.permissions import CanViewDashboard


class StayListAuthorizationTests(SimpleTestCase):
    """Verify Stays use the shared operational authorization path."""

    def test_uses_dashboard_permission(self):
        """The list reuses the same RBAC permission as operational case lists."""

        self.assertEqual(
            StayListAPIView.permission_classes,
            [IsAuthenticated, CanViewDashboard],
        )
