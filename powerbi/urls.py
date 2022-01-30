from django.urls import path

from .views import DashboardListView, DashboardView, PublicDashboardListAPIView, SingleDashboardAPIView

app_name = "powerbi"

urlpatterns = [
    path("", DashboardListView.as_view(), name="dashboard_list"),
    path("<str:id>", DashboardView.as_view(), name="dashboard"),
    path('public-dashboards/', PublicDashboardListAPIView.as_view(), name='public-dashboards'),
    path('public-dashboard/<str:pk>/', SingleDashboardAPIView.as_view(), name='public-dashboards'),
]
