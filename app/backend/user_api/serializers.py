from typing import OrderedDict

from core.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Used to return encoded token with extra fields.
    """

    @classmethod
    def get_token(cls, user: User) -> str:
        """
        Add custom fields and return encoded token.

        Args:
            user (User): for which token will be returned

        Returns:
            str: encoded token with custom fields
        """
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Custom field/s to be attached to the token
        token["name"] = user.name
   
        return token


class UserSerializer(serializers.ModelSerializer):
    """
    Used to create, update and register users in the service.
    """

    class Meta:

        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}
        }

        def create(self, validated_data: OrderedDict[str, str]) -> User:
            """
            Creates, save and returns user.

            Args:
                validated_data (JSON): validated user email, password and name (from Meta)

            Returns:
                User: created user
            """
            user = get_user_model.objects.create_user(**validated_data)

            return user

        def update(
            self, instance: User, validated_data: OrderedDict[str, str]
        ) -> User:
            """
            Update and return user.

            Args:
                instance (User): User object instance
                validated_data (OrderedDict[str, str]): validated user email, password
                                                        and name (from Meta)

            Returns:
                User: updated user
            """
            # If user will not provide password it will be defaulted to None.
            password = validated_data.pop("password", None)
            # super stands for ModelSerializer.
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()

            return user
