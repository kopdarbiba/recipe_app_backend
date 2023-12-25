from recipes.models import Description, Meal, Cuisine, DietaryPreference, Equipment, Allergen, Ingredient, IngredientCategory, Title, Unit, CookingMethod, Adjective, Occasion


# Define a dictionary to map table names to model classes
table_to_model = {
    'title': Title,
    'description': Description,
    'cuisine': Cuisine,
    'occasion': Occasion,
    'meal': Meal,
    'equipment': Equipment,
    'dietarypreference': DietaryPreference,
    'ingredient_category': IngredientCategory,
    'allergen': Allergen,
    'cooking_method': CookingMethod,
    'unit': Unit,
    'adjective' : Adjective,
    'ingredient': Ingredient,
}

UNIQUE_FIELD_NAME = 'name_en'

def update_db(table_name: str, sheet_data_list_of_dict: list[dict]) -> None:
    model_class = table_to_model[table_name] # Unit, DietaryPreference, .....
    # Query all 'name_en' field values from db, and store in set()
    unique_values_checklist = set(model_class.objects.values_list(UNIQUE_FIELD_NAME, flat=True))
    
    for GS_row in sheet_data_list_of_dict:
        # Remove the updated value from the checklist
        unique_values_checklist.discard(GS_row[UNIQUE_FIELD_NAME])

        check_worksheet_row(GS_row)
        manage_create_update(model_class, GS_row)

    manage_delete(model_class, unique_values_checklist)

def check_worksheet_row(row: dict) -> None:

    for field_name, value in row.items():
        # Check if the value is empty or None and the field is not one of the specified fields
        if (value == '' or value is None) and field_name in ['name_en', 'name_lv', 'name_ru']:
            row[field_name] = row[UNIQUE_FIELD_NAME]


def manage_create_update(model_class, GS_row: dict) -> None:
    # Try to get an existing database entry based on a unique field
    instance, created = model_class.objects.get_or_create(name_en=GS_row[UNIQUE_FIELD_NAME], defaults=GS_row)

    if not created:
        # The object already existed, update its fields
        for key in GS_row:
            value = GS_row[key]

            if isinstance(value, str):
                value = value.lower()
            
            setattr(instance, key, value)
        
        # Save the updated entry to the database
        instance.save()

def manage_delete(model_class, unique_values_checklist: set) -> None:
    # If any value left in set(), means this entry was deleted from GS worksheet    
    if unique_values_checklist:
        for value_to_delete in unique_values_checklist:
            # Delete entries in the database based on the unique values in the set
            model_class.objects.filter(name_en=value_to_delete).delete()

        # After the deletion, clear the set since all entries have been deleted
        unique_values_checklist.clear()
