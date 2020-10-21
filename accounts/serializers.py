from django.utils import timezone
from rest_framework import serializers

from .models import CustomUser, Profile, License


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates User and User Profile on sign up.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_no=validated_data.pop("phone_no"),
            **validated_data,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes instance based on User.
    """

    class Meta:
        model = CustomUser
        fields = ("name", "email")


class LicenseSerializer(serializers.ModelSerializer):
    """
    Show/Update license
    """

    class Meta:
        model = License
        fields = "__all__"
        read_only_fields = (
            "type",
            "name",
            "price",
            "iat",
            "eat",
        )

    def update(self, instance, validated_data):
        new_instance = super().update(instance, validated_data)

        new_instance.type = "trial"
        new_instance.name = "Trial"
        new_instance.iat = timezone.now()
        new_instance.eat = timezone.now() + timezone.timedelta(7)
        new_instance.save()

        return new_instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    Show Profile with User model information nested inside.
    """

    user = UserSerializer(read_only=True)
    license_name = serializers.CharField(
        source="assigned_license.name",
        read_only=True,
    )
    license_eat = serializers.CharField(
        source="assigned_license.eat",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            "user",
            "org_name",
            "address",
            "phone_no",
            "bank_name",
            "bank_acc",
            "license_name",
            "license_eat",
        )
        read_only_fields = (
            "phone_no",
            "bank_name",
            "bank_acc",
        )