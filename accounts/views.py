from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser, Profile
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
)


class RegistrationView(CreateAPIView):
    """
    Creates User and Empty Profile.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        phone_no = request.data.pop("phone_no")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(phone_no=phone_no)
            if user:
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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