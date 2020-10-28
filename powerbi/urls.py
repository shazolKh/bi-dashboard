from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DashboardListView, DashboardView

app_name = "powerbi"

urlpatterns = [
    path("", DashboardListView.as_view(), name="dashboard_list"),
    path("<str:id>", DashboardView.as_view(), name="dashboard"),
]

urlpatterns = format_suffix_patterns(urlpatterns)