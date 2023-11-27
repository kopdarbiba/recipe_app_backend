from helpers import get_sheet_data_as_json

# Example usage:
sheet_name = 'ingridient'
base_directory = '/home/tom/code/kopdarbiba/recipe_app_backend/data_population/'
json_file = 'recipeapp.json'

json_data = get_sheet_data_as_json(sheet_name, base_directory, json_file)

if json_data is not None:
    print(f"JSON data from '{sheet_name}' sheet: {json_data}")
else:
    print("Failed to retrieve sheet data as JSON.")
