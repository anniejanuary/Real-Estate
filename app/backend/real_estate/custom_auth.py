""" 
Custom JWT cookie based authentication.
"""
import real_estate.settings as settings
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Overwritten for cookie based authentication instead of request body
        sent JWTs.
        """

        cookie = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if cookie is None:
            return None

        raw_token = cookie.encode(HTTP_HEADER_ENCODING)
        validated_token = self.get_validated_token(raw_token)
      
        return self.get_user(validated_token), validated_token
    
