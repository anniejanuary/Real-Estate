from typing import Union

import real_estate.settings as settings
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)
from user_api.serializers import (
    CookieTokenBlacklistSerializer,
    CookieTokenRefreshSerializer,
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """
    API view to create new user.
    """

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    API view to obtain info about current session user.
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


class MyTokenObtainPairView(TokenObtainPairView):
    """
    API view to log in - create JWT access and refresh tokens and place them into cookie.

    Takes request with user credentials, credentials check against database and if correct returns
    JWT access and refresh tokens placed into hhtponly cookies.

    Remove access abd refresh JWT's from response body.

    The idea here is to persist token at client side in the cookie not
    in the local storage therefore protect JWTs against access by javascripts/ XSS.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=tokens[settings.SIMPLE_JWT["AUTH_COOKIE"]],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE"],
            value=tokens[settings.SIMPLE_JWT["REFRESH_COOKIE"]],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # Remove tokens from response body for enchanced security.
        del response.data[settings.SIMPLE_JWT["AUTH_COOKIE"]]
        del response.data[settings.SIMPLE_JWT["REFRESH_COOKIE"]]

        return response


class MyTokenRefreshView(TokenRefreshView):
    """
    API view to place refresh access token and place it into httponly cookie 
    to retrieve it later on and be sent to refresh endpoint when session expires.
    """

    def finalize_response(
        self, request: Request, response: Response, *args, **kwargs
    ) -> Response:
        """ 
        Grab refresh token from cookie and return new access token in httponly
        cookie.
        Remove access abd refresh JWT's from response body.
        """
        tokens = response.data
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=tokens[settings.SIMPLE_JWT["AUTH_COOKIE"]],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        # Remove tokens from response body for enchanced security.
        del response.data[settings.SIMPLE_JWT["AUTH_COOKIE"]]
        del response.data[settings.SIMPLE_JWT["REFRESH_COOKIE"]]

        return super().finalize_response(
            request, response, *args, **kwargs
        )

    serializer_class = CookieTokenRefreshSerializer


class MyTokenBlacklistView(TokenBlacklistView):
    """
    API view to log out - remove tokens from response cookies
    and blacklist refresh token.
    """

    def finalize_response(
        self, request, response, *args, **kwargs
    ) -> Response:
        # Remove tokens from response body for enchanced security.
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.SIMPLE_JWT["REFRESH_COOKIE"])

        return super().finalize_response(
            request, response, *args, **kwargs
        )

    serializer_class = CookieTokenBlacklistSerializer
