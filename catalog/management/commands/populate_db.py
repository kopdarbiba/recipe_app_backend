import os
import gspread
from django.core.management.base import BaseCommand
from catalog.management.commands._data_manager import db_populate


class Command(BaseCommand):
    help = 'Populate Ingridient objects'

    def handle(self, *args, **options):
        db_table_list = ['unit', 'dietarypreference', 'allergen', 'equipment', 'meal', 'cuisine', 'ingredient', 'ingredient_category']
        relative_key_path = 'catalog/management/commands/recipeapp.json'
        for table in db_table_list:
            sheet_data_dict = get_sheet_data_as_dict(table, relative_key_path)

            if sheet_data_dict is None:
                print("Failed to retrieve sheet data.")
            else:
                db_populate(table, sheet_data_dict)
                self.stdout.write(self.style.SUCCESS(f'table {table} have been successfully created and saved.'))
                
        self.stdout.write(self.style.SUCCESS(f'objects have been successfully created and saved.'))



def get_sheet_data_as_dict(sheet_name : str, relative_path: str) -> dict:
    # Construct the full path to the JSON file using os.path.join()
    json_file_path =  os.path.join(os.path.abspath('.'), relative_path)

    try:
        # Authenticate with Google Sheets using the full path
        gc = gspread.service_account(filename=json_file_path)

        # Open the Google Sheet by name
        sh = gc.open('recipe_db')

        # Access the specified worksheet
        worksheet = sh.worksheet(sheet_name)

        # Return data as dict
        return worksheet.get_all_records()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"The file '{json_file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
