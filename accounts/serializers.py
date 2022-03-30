from django.utils import timezone
from rest_framework import serializers
from dj_rest_auth.registration.serializers import setup_user_email
from dj_rest_auth.serializers import LoginSerializer

from .signals import login_signal
from .models import CustomUser, Profile, License, UserLicense, Feedback, PasswordReset


class RetrievePhoneSerializer(serializers.Serializer):
    """
    Retrieve phone number from profile.
    """

    class Meta:
        model = Profile
        fields = ("phone_no",)


class RegistrationSerializer(serializers.Serializer):
    """
    Creates User and User Profile on sign up.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, request):
        phone_no = request.data["phone_no"]
        print(phone_no, request)
        user = CustomUser.objects.create_user(
            **request.data,
        )
        setup_user_email(request, user, [])
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes instance based on User.
    """

    class Meta:
        model = CustomUser
        fields = ("name", "email")
        read_only_fields = (
            "name",
            "email",
        )


class ProfileSerializer(serializers.ModelSerializer):
    """
    Show Profile with User model information nested inside.
    """

    user = UserSerializer(read_only=True)
    user_license = serializers.SerializerMethodField()

    def get_user_license(self, obj):
        user_license = UserLicense.objects.get(user=obj.user)

        """Checks if trial expired"""
        if (
            user_license.assigned_license.license_type == "trial"
            and timezone.now() > user_license.eat
        ):
            default_free = License.objects.get(license_type="free")

            user_license.assigned_license = default_free
            user_license.current_license_price = default_free.price
            user_license.current_license_qt = 1

            user_license.iat = timezone.now()
            user_license.eat = timezone.now()

            user_license.save()

        return LicenseSerializer(user_license).data

    class Meta:
        model = Profile
        fields = (
            "user",
            "user_license",
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


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Create feedback.
    """

    class Meta:
        model = Feedback
        fields = (
            "user",
            "subject",
            "description",
        )


class LoginSerializer(LoginSerializer):
    """
    Overridden to send custom login signal.
    """

    def validate(self, attrs):
        user = super().validate(attrs)
        request = self.context.get("request")
        login_signal.send(
            sender=CustomUser,
            request=request,
            user_email=request.data["email"],
        )
        return user


class LicenseSerializer(serializers.ModelSerializer):
    """
    Retrieve license details of an user.
    """

    assigned_license_name = serializers.SerializerMethodField()

    def get_assigned_license_name(self, obj):
        return obj.assigned_license.license_type

    class Meta:
        model = UserLicense
        fields = (
            "assigned_license_name",
            "current_license_qt",
            "current_license_price",
            "iat",
            "eat",
            "total_price",
            "applied_license",
            "applied_license_qt",
            "applied_for_pro",
        )
        read_only_fields = (
            "assigned_license_name",
            "current_license_qt",
            "current_license_price",
            "iat",
            "eat",
            "total_price",
            "applied_license",
            "applied_license_qt",
            "applied_for_pro",
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

        if (
            current_license.license_type == "free"
            and new_instance.applied_for_pro == False
        ):
            """Create default trial license and user license to that"""

            default_trial = License.objects.get(license_type="trial")

            new_instance.assigned_license = default_trial
            new_instance.current_license_price = default_trial.price
            new_instance.current_license_qt = 1

            new_instance.iat = timezone.now()
            new_instance.eat = timezone.now() + default_trial.duration

            new_instance.applied_for_pro = True

        if not (
            current_license.license_type == "trial"
            and validated_data["applied_license"] == "trial"
        ):
            new_instance.applied_license = validated_data["applied_license"]
            new_instance.applied_license_qt = validated_data["applied_license_qt"]
            new_instance.upgradingfrom_license = current_license.license_type

        new_instance.save()
        return new_instance


class InitPasswordResetSerializer(serializers.ModelSerializer):
    """
    Serialize password reset requests.
    """

    class Meta:
        model = PasswordReset
        fields = ("user", 'phone_no', "otp_code")
