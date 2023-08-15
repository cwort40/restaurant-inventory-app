import difflib

from inventoryApp.api.openai_client import fetch_density
from inventoryApp.constants.densities import INGREDIENT_DENSITIES
from inventoryApp.constants.measurements import UNIT_CONVERSIONS, VOLUME_UNITS


class UnitConversionUtil:

    @staticmethod
    def get_best_match(ingredient_name):
        best_ratio = 0.8  # threshold for similarity (needs to be at least 80% similar)
        best_match = None
        for key in INGREDIENT_DENSITIES.keys():
            current_ratio = difflib.SequenceMatcher(None, ingredient_name, key).ratio()
            if current_ratio > best_ratio:
                best_ratio = current_ratio
                best_match = key
        return best_match

    @staticmethod
    def get_density(ingredient_name):
        from inventoryApp.models import Ingredient
        ingredient = Ingredient.objects.get(name=ingredient_name)

        # If density exists in ingredient, return it
        if ingredient and ingredient.density:
            return ingredient.density

        density = INGREDIENT_DENSITIES.get(ingredient_name)
        if density is None:
            best_match = UnitConversionUtil.get_best_match(ingredient_name)
            if best_match:
                density = INGREDIENT_DENSITIES[best_match]
            else:
                fetched_density = fetch_density(ingredient_name)
                ingredient.density = fetched_density
                ingredient.save()
                density = fetched_density if fetched_density is not None else 1  # Density of water as default
        return density

    @staticmethod
    def convert_to_common_unit(quantity, unit, ingredient_name):
        conversion_value = UNIT_CONVERSIONS.get(unit)
        if conversion_value is None:
            raise UnsupportedUnitError(f"'{unit}' is not a supported unit for conversion.")
        density = UnitConversionUtil.get_density(ingredient_name)

        # Check if converting within the same type
        if unit in VOLUME_UNITS:
            return quantity * conversion_value

        return quantity * conversion_value / density  # Convert to grams or milliliters

    @staticmethod
    def convert_to_original_unit(quantity, unit, ingredient_name):
        conversion_value = UNIT_CONVERSIONS.get(unit)
        if conversion_value is None:
            raise UnsupportedUnitError(f"'{unit}' is not a supported unit for conversion.")
        density = UnitConversionUtil.get_density(ingredient_name)

        # Check if converting within the same type
        if unit in VOLUME_UNITS:
            return quantity / conversion_value

        return quantity * density / conversion_value  # Convert to original unit


class UnsupportedUnitError(Exception):
    """Raised when a given unit is not supported for conversion."""
    pass
