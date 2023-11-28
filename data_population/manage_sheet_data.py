from data_population.models import Ingridient
from catalog.models import Recipe


def db_populate(sheet_data_dict: dict) -> None:
    for row in sheet_data_dict:
        # Convert empty strings to None in the row dictionary
        for field, value in row.items():
            if value == '':
                row[field] = None

        # Create a dictionary with cleaned data for creating a Recipe instance
        recipe_data = {
            'title': row['title'],
            'servings': row['servings'],
            'description': row['description'],
            'cuisine': row['cuisine'],
            'meal': row['meal'],
            'food_category': row['food_category'],
            'cooking_time': row['cooking_time'],
            'equipment': row['equipment'],
            'ingredient': row['ingredient'],
            'cooking_steps': row['cooking_steps'],
            'allergens': row['allergens'],
            'ingredient_substitute': row['ingredient_substitute'],
            'nutritional_information': row['nutritional_information'],
            'calories': row['calories'],
            'rating': row['rating'],
            'dietary_preference': row['dietary_preference'],
            'measurements': row['measurements'],
        }

        # Remove keys with values set to None
        recipe_data = {k: v for k, v in recipe_data.items() if v is not None}

        # Create a Recipe instance and save it to the database
        recipe = Recipe(**recipe_data)
        recipe.save()
