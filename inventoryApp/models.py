from django.db import models

from inventoryApp.constants.measurements import UNITS_OF_MEASUREMENT
from inventoryApp.constants.util import UnitConversionUtil


# Create your models here.
class MenuItem(models.Model):
    # Item on the restaurant's menu
    title = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0.00)

    def get_absolute_url(self):
        return "/menu"

    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    # Ingredient within the restaurant's inventory
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNITS_OF_MEASUREMENT, default='lb')
    price_per_unit = models.FloatField(default=0)

    def get_absolute_url(self):
        return "/ingredients"

    def __str__(self):
        return self.name


class RecipeRequirement(models.Model):
    # An ingredient and corresponding quantity and unit needed for the recipe of a MenuItem.
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNITS_OF_MEASUREMENT, default='lb')

    def __str__(self):
        return f"{self.menu_item.title}: {self.ingredient.name} {self.quantity} {self.get_unit_display()}"

    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        required_quantity = UnitConversionUtil.convert_to_common_unit(self.quantity, self.unit, self.ingredient.name)
        available_quantity = UnitConversionUtil.convert_to_common_unit(self.ingredient.quantity, self.ingredient.unit,
                                                                       self.ingredient.name)
        return required_quantity <= available_quantity


class Purchase(models.Model):
    # Purchase of a MenuItem
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.__str__()} @ {self.timestamp}"

    def get_absolute_url(self):
        return "/purchases"
