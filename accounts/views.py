from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    UpdateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from .models import Profile, UserLicense
from .serializers import (
    ProfileSerializer,
    LicenseUpdateSerializer,
)


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