from datetime import datetime
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from dj_rest_auth.views import LogoutView, PasswordResetView

from .models import Profile, UserLicense, CustomUser
from .serializers import (
    FeedbackSerializer,
    RetrievePhoneSerializer,
    ProfileSerializer,
    LicenseUpdateSerializer,
)


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