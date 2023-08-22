from django.core.management.base import BaseCommand
from inventoryApp.models import MenuItem, Ingredient, RecipeRequirement
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Clears data from specified tables for InventoryApp'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help="ID of the User whose data should be cleared.")
        parser.add_argument('--all', action='store_true', help="Clear all data irrespective of user.")

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']

        # If --all flag is used, clear all data irrespective of user
        if kwargs['all']:
            RecipeRequirement.objects.all().delete()
            MenuItem.objects.all().delete()
            Ingredient.objects.all().delete()
            # Add other models to clear as needed
        else:
            RecipeRequirement.objects.filter(user_id=user_id).delete()
            MenuItem.objects.filter(user_id=user_id).delete()
            Ingredient.objects.filter(user_id=user_id).delete()
            # Add other models with a user relationship to clear as needed

        self.stdout.write(self.style.SUCCESS('Successfully cleared data!'))
