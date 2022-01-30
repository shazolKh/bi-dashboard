from django.contrib import admin

from .models import Dashboard, PublicDashboard


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


@admin.register(PublicDashboard)
class DashboardAdmin(admin.ModelAdmin):
    model = PublicDashboard

    list_display = (
        "title",
        # "dashboard_url",
        "thumbnail_url",
        'created_at',
        'modified_at'
    )
