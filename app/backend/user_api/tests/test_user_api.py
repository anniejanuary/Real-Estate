""" 
Tests for user API
"""

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user_api:create")


def create_user(**params):
    """Create and return user for tests"""
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """Tests for public calls to user API (no auth needed)."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test user creation successful"""
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Test if user was created with password from payload.
        user = get_user_model().objects.get(email=payload["email"])
        self.assertEqual(payload["password"], user.password)
        # Test if password not returned to client in response.
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error_produced(self):
        """Test if error returned (on creation) when user already exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test Name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error_produced(self):
        """Test if error returned when password len < 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "test",  # less than 5
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(email=payload["email"])
            .exists()
        )

        self.assertFalse(user_exists)
