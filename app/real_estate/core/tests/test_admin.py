"""Tests for custom Admin dashboard"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Tests for django admin page."""

    def setUp(self):
        """
        Create test user and start test client for
        serving content of the admin page.
        """
        self.client = Client()
        self.admin_user = get_user_model().user_manager.create_superuser(
            email="admin@example.com", password="test_pass_123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().user_manager.create_user(
            email="user@example.com",
            password="test_user_pass_123",
            name="Test User",
        )

    def test_users_listing(self):
        """Test admin page users listing."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user(self):
        """Test admin page user modification."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_create_user(self):
        """Test admin page create user."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    