from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser, Profile
from .serializers import RegistrationSerializer, ProfileSerializer


class RegistrationView(CreateAPIView):
    """
    Creates User and Empty Profile.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class ProfileView(RetrieveAPIView):
    """
    Show User profile.
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    serializer_class = ProfileSerializer

    queryset = Profile.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)
