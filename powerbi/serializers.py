from rest_framework import serializers

from .models import Dashboard, PublicDashboard


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


class PublicDashboardSerializer(serializers.ModelSerializer):
    """
    Serializes a public dashboard.
    """

    class Meta:
        model = PublicDashboard
        fields = (
            'id',
            "title",
            # "dashboard_url",
            "thumbnail_url",
        )


class SinglePublicDashboardSerializer(serializers.ModelSerializer):
    """
    Serializes a public dashboard.
    """

    class Meta:
        model = PublicDashboard
        fields = (
            'id',
            "title",
            "dashboard_url",
            # "thumbnail_url",
        )
