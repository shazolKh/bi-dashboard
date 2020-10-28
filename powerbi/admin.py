from django.contrib import admin

from .models import Dashboard


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    model = Dashboard

    list_display = (
        "title",
        "dashboard_id",
        "license_type",
        "thumbnail_url",
    )

    list_filter = ("license_type",)
