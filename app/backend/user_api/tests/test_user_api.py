""" 
Tests for user API
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user_api:create")
TOKEN_URL = reverse("token_obtain_pair")
ME_URL = reverse("user_api:me")


def create_user(**params):
    """Create and return user for tests"""
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """API calls to endpoints where authentication not needed."""

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

    def test_create_token_for_existing_user(self):
        """Test if token generated for valid credentials."""
        new_user_details = {
            "name": "testName",
            "email": "test@example.com",
            "password": "testPassword",
        }
        create_user(**new_user_details)

        payload = {
            "email": new_user_details["email"],
            "password": new_user_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_unvalid_credentials(self):
        """Test if token not produced when wrong pass provided."""
        create_user(email="test@example.com", password="validPass")

        payload = {"email": "test@example.com", "password": "wrongPass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test if token not produced when no password provided."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test if user endpoint returns unathorized when no token 
        in request.
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """API calls to endpoints where authentication needed."""

    def setUp(self):
        """
        Create test user for methods in the class along
        with mocked authentication.
        """
        self.user = create_user(
            email="test@example.com",
            password="testPass",
            name="testName",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_successfuly(self):
        """Test retrieving get authenticated user profile."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST method is not allowed to /me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating user profile by PATCH method for authenicated user
        allowed.
        """
        payload = {
            "name": "newName",
            "password": "newValidPassword",
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload["name"])
        self.assertEqual(self.user.password, payload["password"])

