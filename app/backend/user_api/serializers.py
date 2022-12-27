from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import User
from typing import OrderedDict


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
            user = get_user_model.user_manager.create_user(
                **validated_data
            )

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
