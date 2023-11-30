from catalog.models import *


# Define a dictionary to map table names to model classes
table_to_model = {
    'unit': Unit,
    'dietarypreference': DietaryPreference,
    'allergen': Allergen,
    'equipment': Equipment,
    'meal': Meal,
    'cuisine': Cuisine,
    'ingredient': Ingredient,
    'ingredient_category': IngredientCategory,
}

unique_field_name = 'name_eng'

def db_populate(table_name: str, sheet_data_dict: list[dict]) -> None:
    print(sheet_data_dict)
    for GS_row in sheet_data_dict:
        # Check GS data. Convert empty strings to None in the row dictionary
        for field_name, value in GS_row.items():
            if value == '':
                GS_row[field_name] = None
        populate_database(table_name, GS_row)


# Function to handle database population
def populate_database(table_name: str, GS_row: dict) -> None:
    # Move model_class definition outside the try-except block
    model_class = table_to_model[table_name]

    try:
        # Try to get an existing database entry based on a unique field
        db_entry = model_class.objects.get(name_eng=GS_row[unique_field_name])

        # Iterate through keys in GS_row (assuming they correspond to model fields)
        for key in GS_row:
            # Get the value from GS_row and the current value from the database entry
            v1 = GS_row[key]
            v2 = getattr(db_entry, key)

            # Compare the values
            if v1 != v2:
                # If different, update the database entry's field with the new value
                setattr(db_entry, key, v1)

        # Save the updated entry to the database
        db_entry.save()

    except model_class.DoesNotExist:
        # If the entry doesn't exist, create a new one using GS_row data
        model_instance = model_class(**GS_row)
        model_instance.save()





############################################################################################################################

# Examle queries.

# Creating objects!

    # Django doesn’t hit the database until you explicitly call save().

    # This performs an INSERT SQL statement behind the scenes. 
    # >>> from blog.models import Blog
    # >>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
    # >>> b.save()
    # or
    # p = Person.objects.create(first_name="Bruce", last_name="Springsteen")


# Retrieving all objects!

    # The simplest way to retrieve objects from a table is to get all of them. To do this, use the all() method on a Manager:

    # >>> all_entries = Entry.objects.all()

    # For example, to get a QuerySet of blog entries from the year 2006, use filter() like so:

    # Entry.objects.filter(pub_date__year=2006)

    # With the default manager class, it is the same as:

    # Entry.objects.all().filter(pub_date__year=2006)

    # >>> one_entry = Entry.objects.get(pk=1)



