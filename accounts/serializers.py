from rest_framework import serializers

from .models import CustomUser, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates User and User Profile on sign up.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes instance based on UserProfile.
    """

    class Meta:
        model = CustomUser
        fields = ("name", "email")


class ProfileSerializer(serializers.ModelSerializer):
    """
    Show profile with user information nested inside.
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
            "license_type",
            "license_price",
            "license_iat",
            "license_duration",
        )
# {
#     "user": {
#         "name": "Stewart",
#         "email": "stewart@gmail.com"
#     },
#     "phone_no": "",
#     "org_name": "",
#     "address": "",
#     "bank_name": "",
#     "bank_acc": "",
#     "license_type": "free",
#     "license_price": 0,
#     "license_iat": "2020-10-20T11:01:12.842439+06:00",
#     "license_duration": null
# }