from django.urls import path

from .views import DashboardListView, DashboardView

app_name = "powerbi"

urlpatterns = [
    path("", DashboardListView.as_view(), name="dashboard_list"),
    path("<str:id>", DashboardView.as_view(), name="dashboard"),
]