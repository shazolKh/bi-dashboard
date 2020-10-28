from rest_framework import serializers

from .models import Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    """
    Serializes a dashboard.
    """

    class Meta:
        model = Dashboard
        fields = (
            "title",
            "dashboard_id",
            "thumbnail_url",
            "license_type",
        )
