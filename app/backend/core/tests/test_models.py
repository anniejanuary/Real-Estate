from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests from models."""

    def test_create_user_with_email_successful(self):
        """Test creating user with email successful."""
        email = "test@test.com"
        password = "testPass"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_create_superuser(self):
        email = "admin@test.com"
        password = "testPass"
        user = get_user_model().objects.create_superuser(
            email=email, password=password
        )

        self.assertTrue(user.is_superuser)