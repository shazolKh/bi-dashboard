from django.utils import timezone
from rest_framework import serializers

from .models import CustomUser, Profile, License, UserLicense


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


class ProfileSerializer(serializers.ModelSerializer):
    """
    Show Profile with User model information nested inside.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "phone_no",
            "org_name",
            "address",
            "bank_name",
            "bank_acc",
        )
        read_only_fields = (
            "phone_no",
            "bank_name",
            "bank_acc",
        )


class LicenseUpdateSerializer(serializers.ModelSerializer):
    """
    Update license and Applied for field. User can only specify,
    1. What license is being applied for?
    2. What is the quantity if its of type 'pro'?
    """

    class Meta:
        model = UserLicense
        fields = (
            "applied_license",
            "applied_license_qt",
        )

    def update(self, instance, validated_data):

        current_license = instance.assigned_license
        new_instance = instance

        if current_license.license_type == "free":
            """Create default trial license and user license to that"""
            default_trial = License.objects.get(license_type="trial")

            new_instance.assigned_license = default_trial
            new_instance.current_license_price = default_trial.price
            new_instance.current_license_qt = 1

            new_instance.iat = timezone.now()
            new_instance.eat = timezone.now() + default_trial.duration

        if not (
            current_license.license_type == "trial"
            and validated_data["applied_license"] == "trial"
        ):
            new_instance.applied_license = validated_data["applied_license"]
            new_instance.applied_license_qt = validated_data["applied_license_qt"]
            new_instance.upgradingfrom_license = current_license.license_type

        new_instance.save()
        return new_instance