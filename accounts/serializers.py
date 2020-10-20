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