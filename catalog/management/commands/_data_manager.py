from catalog.models import *



def db_populate(table_name: str, sheet_data_dict: dict) -> None:
    for row in sheet_data_dict:
        # Check GS data. Convert empty strings to None in the row dictionary
        for field_name, value in row.items():
            if value == '':
                row[field_name] = None

        # Check database data. Removes any existing and equal value from sheet data dict
            # TODO!!!!!         

        # Populate database
        match table_name:
            case 'unit':
                unit = Unit(**row)
                unit.save()
            case 'dietarypreference':
                dietary_preference = DietaryPreference(**row)
                dietary_preference.save()
            case 'allergen':
                allergen = Allergen(**row)
                allergen.save()
            case 'equipment':
                equipment = Equipment(**row)
                equipment.save()
            case 'meal':
                meal = Meal(**row)
                meal.save()
            case 'cuisine':
                cuisine = Cuisine(**row)
                cuisine.save()
            case 'ingredient':
                ingredient = Ingredient(**row)
                ingredient.save()
            case 'ingredient_category':
                ingredient_category = IngredientCategory(**row)
                ingredient_category.save()

