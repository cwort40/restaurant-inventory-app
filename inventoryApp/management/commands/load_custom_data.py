from django.core.management.base import BaseCommand
import json
from inventoryApp.models import MenuItem, Ingredient, RecipeRequirement
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Loads custom data from a JSON file for InventoryApp'

    def add_arguments(self, parser):
        # Argument names have been updated for clarity.
        parser.add_argument('file_path', type=str, help="The path to the JSON file with the data.")
        parser.add_argument('user_id', type=int, help="ID of the User to associate the data with.")

    def handle(self, *args, **kwargs):
        # Correctly reference the renamed arguments
        file_path = kwargs['file_path']
        user_id = kwargs['user_id']
        user = User.objects.get(pk=user_id)

        with open(file_path, 'r') as file:
            data = json.load(file)

            # Create Ingredients
            for ingredient_data in data.get("ingredients", []):
                Ingredient.objects.create(
                    name=ingredient_data['name'],
                    quantity=ingredient_data['quantity'],
                    unit=ingredient_data['unit'],
                    price_per_unit=ingredient_data['price_per_unit'],
                    user=user,
                    density=ingredient_data.get('density', None)
                )

            # Create Menu Items and their associated Recipe Requirements
            for menu_item_data in data.get("menu_items", []):
                menu_item = MenuItem.objects.create(
                    title=menu_item_data['title'],
                    price=menu_item_data['price'],
                    user=user
                )

                for req in menu_item_data.get("requirements", []):
                    ingredient = Ingredient.objects.get(name=req['ingredient_name'], user=user)
                    RecipeRequirement.objects.create(
                        menu_item=menu_item,
                        ingredient=ingredient,
                        quantity=req['quantity'],
                        unit=req['unit'],
                        user=user
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data!'))
