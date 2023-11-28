from data_population.models import Ingridient
from catalog.models import Recipe

# def db_populate(sheet_data_dict: dict) -> None:
#     for row in sheet_data_dict:
#         ingredient = Ingridient(title=row['title'], nosaukums=row['nosaukums'], calories=row['calories'])
#         ingredient.save()

def db_populate(sheet_data_dict: dict) -> None:
    recipe_fields = {
    'title': 'title',
    'servings': 'servings',
    'description': 'description',
    'cuisine': 'cuisine',
    'meal': 'meal',
    'food_category': 'food_category',
    'cooking_time': 'cooking_time',
    'equipment': 'equipment',
    'ingredient': 'ingredient',
    'cooking_steps': 'cooking_steps',
    'allergens': 'allergens',
    'ingredient_substitute': 'ingredient_substitute',
    'nutritional_information': 'nutritional_information',
    'calories': 'calories',
    'rating': 'rating',
    'dietary_preference': 'dietary_preference',
    'measurements': 'measurements'
    }

    for row in sheet_data_dict:
        for field, value in row.items():
            if value is '':
                row[field] = None

        recipe = Recipe(title=row['title'], servings=row['servings'], description=row['description'],
                        cuisine=row['cuisine'], meal=row['meal'], food_category=row['food_category'],
                        cooking_time=row['cooking_time'], equipment=row['equipment'], ingredient=row['ingredient'],
                        cooking_steps=row['cooking_steps'], allergens=row['allergens'], ingredient_substitute=row['ingredient_substitute'],
                        nutritional_information=row['nutritional_information'], calories=row['calories'], rating=row['rating'],
                        dietary_preference=row['dietary_preference'], measurements=row['measurements']
                        )
        recipe.save()