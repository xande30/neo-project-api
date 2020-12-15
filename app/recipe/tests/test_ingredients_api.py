from djangocontrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL =  reverse('recipe:ingredient-list')

class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""
    res = self.client.get(INGREDIENTS_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test iprivate ingredienbt api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@neo.com'
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kali')
        Ingredient.objects.create(user=self.user, name='No Sugar')

        res = self.cleint.get(INGREDIENTS_URL)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients are returned"""
        user2 = get_user_model().objects.create_user(
            'other@neo.com'
            'testpass'
        )
        Ingredient = Ingredient.obejects.create(user=user2, name='Orange')

        ingredient = Ingredient.objects.create(user=self.user, name='Turmeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
