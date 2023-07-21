from django.test import TestCase
from django.contrib.auth.models import User
from inventoryApp.models import Ingredient


class IngredientTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')  # Create a test user
        Ingredient.objects.create(name="Test Ingredient", quantity=10, unit="lb", price_per_unit=2.99,
                                  user=self.test_user)

    def test_ingredient_exists(self):
        test_ingredient = Ingredient.objects.get(name="Test Ingredient")
        self.assertTrue(test_ingredient)

    def test_ingredient_quantity(self):
        test_ingredient = Ingredient.objects.get(name="Test Ingredient")
        self.assertEqual(test_ingredient.quantity, 10)

    def test_ingredient_unit(self):
        test_ingredient = Ingredient.objects.get(name="Test Ingredient")
        self.assertEqual(test_ingredient.unit, "lb")

    def test_ingredient_price_per_unit(self):
        test_ingredient = Ingredient.objects.get(name="Test Ingredient")
        self.assertAlmostEqual(test_ingredient.price_per_unit, 2.99, places=2)