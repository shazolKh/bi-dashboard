from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .signals import login_signal
from .models import CustomUser, Profile, License, UserLicense
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
    LicenseUpdateSerializer,
)


class RegistrationView(CreateAPIView):
    """
    Creates User and Empty Profile.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Phone no. passing flow:
        from view: serializer.save(phone_no) to serializer: validated_data.phone_no
        from serializer: create_user(phone_no) to managers: create_user(param=phone_no)
        from managers user.phone_no to signal: instance.phone_no
        """
        phone_no = request.data.pop("phone_no")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(phone_no=phone_no)
            if user:
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Add custom login signal.
    """

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        login_signal.send(
            sender=CustomUser,
            request=request,
            user_email=request.data["email"],
        )
        return response


class UserView(RetrieveUpdateDestroyAPIView):
    """
    Read/Update/Delete User.
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    serializer_class = UserSerializer

    queryset = CustomUser.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, email=self.request.user.email)


class ProfileView(RetrieveUpdateAPIView):
    """
    Read/Update User Profile.
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    serializer_class = ProfileSerializer

    queryset = Profile.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)


class LicenseUpdateView(UpdateAPIView):
    """
    Apply for Pro/Enterprise.
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    serializer_class = LicenseUpdateSerializer

    queryset = UserLicense.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)