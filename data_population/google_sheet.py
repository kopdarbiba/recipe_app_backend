from helpers import get_sheet_data_as_dict

# Example usage:
sheet_name = 'ingridient'
relative_key_path = 'data_population/recipeapp.json'

sheet_data_dict = get_sheet_data_as_dict(sheet_name, relative_key_path)

if sheet_data_dict is not None:
    print(f"data from '{sheet_name}' sheet: {sheet_data_dict}")
else:
    print("Failed to retrieve sheet data.")
