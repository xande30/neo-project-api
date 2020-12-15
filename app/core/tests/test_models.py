from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@neo.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """Create user with email address"""
        email = 'test@neo.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
        email=email,
        password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test the email for a new user normalized"""
        email = 'test@neo.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')


    def test_create_new_superuser(self):
        """Test create a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@neo.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
