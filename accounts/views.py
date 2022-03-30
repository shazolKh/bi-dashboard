import os
from datetime import datetime
from random import randint

from django.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer

from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from dj_rest_auth.views import LogoutView, PasswordResetView

from .models import Profile, UserLicense, CustomUser, PasswordReset
from .serializers import (
    FeedbackSerializer,
    RetrievePhoneSerializer,
    ProfileSerializer,
    LicenseUpdateSerializer,
    InitPasswordResetSerializer,
)

from accounts.otp import send_otp
from accounts.extended_schema import verify_pass_schema, pass_reset_schema, init_pass_schema


class RetrievePhoneView(RetrieveAPIView):
    """
    Lookup user by phone number.
    """

    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = RetrievePhoneSerializer

    def get_object(self):
        qs = self.get_queryset()
        phone_no = self.kwargs["phone_no"]
        return get_object_or_404(qs, phone_no=phone_no)


class CustomPasswordResetView(PasswordResetView):
    """
    Check if email exists before resetting password.
    """

    def post(self, request, *args, **kwargs):
        data = get_object_or_404(CustomUser.objects.all(), email=request.data["email"])
        return super().post(request=request, args=args, kwargs=kwargs)


class CustomLogoutView(LogoutView):
    """
    Update logout to be auth user only.
    """

    permission_classes = (IsAuthenticated,)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Send access token as http-only cookie when refreshing token.
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if getattr(settings, "REST_USE_JWT", False):
            cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
            cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
            cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
            cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")
            if cookie_name:
                expiration = datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME
                response.set_cookie(
                    cookie_name,
                    serializer.validated_data["access"],
                    expires=expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite,
                )
        return response


class ProfileView(RetrieveUpdateAPIView):
    """
    Read/Update User Profile.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    queryset = Profile.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)


class FeedbackView(CreateAPIView):
    """
    Create User Feedback.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)


class LicenseUpdateView(UpdateAPIView):
    """
    Apply for Pro/Enterprise.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LicenseUpdateSerializer

    queryset = UserLicense.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)


@extend_schema_view(
    post=extend_schema(
        request=inline_serializer(
            name="InitPassSerializer",
            fields={"email": serializers.EmailField()},
        ),
        responses={**init_pass_schema},
    )
)
class InitPasswordResetAPIView(generics.GenericAPIView):
    """
        Create/Update password-reset entry.
    """

    serializer_class = InitPasswordResetSerializer
    permission_classes = (AllowAny,)

    def handle_passwordreset(self, phone_no, user, is_update, *args, **kwargs):
        """
        Create/Update password-reset entry.
        """
        generated_otp = randint(1111, 9999)

        if os.environ.get("DJANGO_ENV") == "production":
            response = send_otp(phone_no, generated_otp)
        else:
            response = {"status": 200, "message": "success"}

        if response.get("status") == 200:
            if is_update:
                pass_rest = PasswordReset.objects.get(phone_no=phone_no)

                serializer = self.serializer_class(
                    pass_rest,
                    data={"user": user.id, "otp_code": generated_otp, 'phone_no': phone_no},
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    data={
                        "message": "Password reset code updated.",
                        'phone_no': f"{phone_no[:6]}*****{phone_no[-3:]}",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = self.serializer_class(
                    data={"user": user.id, "otp_code": generated_otp, 'phone_no': phone_no}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    data={
                        "message": "Password reset code created.",
                        'phone_no': f"{phone_no[:6]}*****{phone_no[-3:]}",
                    },
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                data={"message": "OTP Service Error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if email:
            try:
                user = CustomUser.objects.get(email=email)
                phone_no = Profile.objects.get(user=user).phone_no
                PasswordReset.objects.get(user=user)

                return self.handle_passwordreset(
                    phone_no, user, is_update=True, *args, **kwargs
                )
            except PasswordReset.DoesNotExist:
                return self.handle_passwordreset(
                    phone_no, user, is_update=False, *args, **kwargs
                )
            except CustomUser.DoesNotExist:
                return Response(
                    data={"message": "User with given phone no not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                data={"message": "Invalid Request format."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    post=extend_schema(
        request=inline_serializer(
            name="VerifyOTPSerializer",
            fields={
                "email": serializers.EmailField(),
                "otp_code": serializers.CharField(),
            },
        ),
        responses={**verify_pass_schema},
    )
)
class VerifyPasswordResetAPIView(APIView):
    """
    Verify password reset OTP.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        otp_code = request.data.get("otp_code")
        email = request.data.get("email")

        if email and otp_code:
            try:
                pass_reset = PasswordReset.objects.get(user__email=email)
                if otp_code == pass_reset.otp_code:
                    pass_reset.verified = True
                    pass_reset.otp_code = -1
                    pass_reset.save()
                    return Response(
                        data={"message": "OTP matched."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        data={"message": "OTP didn't match"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except PasswordReset.DoesNotExist:
                return Response(
                    data={"message": "OTP doesn't exist for this number."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                data={"message": "Invalid Request Format."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    post=extend_schema(
        request=inline_serializer(
            name="VerifyPassSerializer",
            fields={
                "email": serializers.EmailField(),
                "new_password": serializers.CharField(),
            },
        ),
        responses={**pass_reset_schema},
    )
)
class PasswordResetAPIView(APIView):
    """
    Reset password of a user if the OTP is verified.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        new_password = request.data.get("new_password")
        email = request.data.get("email")

        if new_password and email:
            try:
                pass_reset = PasswordReset.objects.get(user__email=email)
                if pass_reset.verified:
                    user = CustomUser.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                    pass_reset.verified = False
                    pass_reset.save()
                    return Response(
                        data={"message": "Password reset successful"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        data={"message": "OTP not verified."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except CustomUser.DoesNotExist:
                return Response(
                    data={"message": "Phone number doesn't exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except PasswordReset.DoesNotExist:
                return Response(
                    data={"message": "OTP doesn't exist for this number."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                data={"message": "Invalid request format."},
                status=status.HTTP_400_BAD_REQUEST,
            )
