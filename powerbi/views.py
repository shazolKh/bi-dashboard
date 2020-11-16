from collections import namedtuple
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from .models import Dashboard
from accounts.models import License
from .serializers import DashboardSerializer
from .utils import checkconfig, getaccesstoken, getembedinfo


class DashboardListView(ListAPIView):
    """
    Read a list of Dashboard.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardSerializer

    queryset = Dashboard.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        user = self.request.user
        user_license = user.userlicense.assigned_license
        all_dashboard = serializer.data
        user_dashboard = []

        """Filter licenses according to license type"""
        for dashboard in all_dashboard:
            dashboard_license = License.objects.get(id=dashboard["license_type"])

            if user_license.license_type == "free" and (
                dashboard_license.license_type == "trial"
                or dashboard_license.license_type == "pro"
                or dashboard_license.license_type == "enterprise"
            ):
                dashboard["dashboard_id"] = ""
            elif (
                user_license.license_type == "trial"
                or user_license.license_type == "pro"
            ) and dashboard_license.license_type == "enterprise":
                dashboard["dashboard_id"] = ""
            elif (
                user_license.license_type == "enterprise"
                and dashboard_license.name != user_license.name
            ):
                dashboard["dashboard_id"] = ""

            user_dashboard.append(dashboard)

        return Response(user_dashboard)


class DashboardView(RetrieveAPIView):
    """
    Read a single Dashboard.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardSerializer

    queryset = Dashboard.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        query_id = self.kwargs["id"]
        return get_object_or_404(qs, dashboard_id=query_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        settings.MSAL_CONFIG["REPORT_ID"] = serializer.data["dashboard_id"]

        config = namedtuple("Config", settings.MSAL_CONFIG.keys())(
            *settings.MSAL_CONFIG.values()
        )

        try:
            valid_config = checkconfig(config)
            if valid_config is not None:
                raise ImproperlyConfigured("Check config file/env variables!")
            else:
                embedinfo = getembedinfo(config, getaccesstoken(config))
                return Response(embedinfo)
        except Exception as ex:
            return Response(ex)
