from typing import Union

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from user_api.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
)


class MyObtainTokenPairView(TokenObtainPairView):
    """
    API view to obtain token with custom added fields in it.
    """

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    """
    API view created to create new user.
    Protected by JWT.
    """

    serializer_class = UserSerializer
    # TODO decide whether authentication needed on that endpoint
    #permission_classes = [IsAuthenticated]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    API view to obtain info of current user.
    Protected by JWT.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Union[AbstractBaseUser, AnonymousUser]:
        """
        Return current user if is authenticated with JWT.

        Returns:
            AbstractBaseUser - if authenticated
            AnonymousUser - if not authenticated
        """
        return self.request.user
