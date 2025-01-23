"""
Tests for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
                ['test1@EXAMPLE.COM', 'test1@example.com'],
                ['Test2@Example.com', 'Test2@example.com'],
                ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
                ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'Sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that a creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'Sample123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Sample123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_activity(self):
        """Testing creating an activity is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        activity = models.Activity.objects.create(
            user=user,
            title='Sample activity name',
            time_hours=5,
            price=Decimal('12.00'),
            description='Sample activity description',
        )

        self.assertEqual(str(activity), activity.title)
