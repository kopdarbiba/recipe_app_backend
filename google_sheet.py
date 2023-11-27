import gspread
# from catalog.models import Recipe

# Authenticate with Google Sheets
gc = gspread.service_account(filename='recipeapp.json')

# Open the Google Sheet by name
sh = gc.open('Kopdarbs')

# Specify the name of the desired sheet
sheet_name = 'RecipeData'

# Access the specified worksheet
worksheet = sh.worksheet(sheet_name)

# Get all values in the sheet
all_values = worksheet.get_all_values()

print(all_values)

# # Define column indices based on the sheet structure
# column_indices = {
#     "title": 0,
#     "instructions": 1,
#     "servings": 5,
# }

# # Skip the header row
# data_rows = all_values[1:]

# # Iterate over the data rows
# for row_data in data_rows:
#     # Extract values from the row based on column indices
#     values = {
#         "title": row_data[column_indices["title"]],
#         "instructions": row_data[column_indices["instructions"]],
#         "servings": float(row_data[column_indices["servings"]]),
#     }

#     # Create a Recipe instance and save it to the database
#     recipe = Recipe(**values)
#     recipe.save()
