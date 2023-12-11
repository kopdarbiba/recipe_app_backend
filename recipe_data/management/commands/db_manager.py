import os
from decouple import config
import gspread
from django.core.management.base import BaseCommand
from recipe_data.management.commands._update_db import update_db


class Command(BaseCommand):
    help = 'Populate Ingridient objects'

    def handle(self, *args, **options):
        db_table_list = ['unit', 'dietarypreference', 'allergen', 'equipment', 'meal', 'cuisine', 'ingredient_category', 'ingredient', 'cooking_method'] # Add table names
        relative_key_path = config('RELATIVE_KEY_PATH')
        
        for table_name in db_table_list:
            sheet_data_list_of_dict = get_sheet_data_as_list_of_dict(table_name, relative_key_path)

            if sheet_data_list_of_dict is None:
                print("Failed to retrieve sheet data.")
            else:
                update_db(table_name, sheet_data_list_of_dict)
                self.stdout.write(self.style.SUCCESS(f'table {table_name} have been successfully created and saved.'))
                
        self.stdout.write(self.style.SUCCESS(f'objects have been successfully created and saved.'))



def get_sheet_data_as_list_of_dict(table_name : str, relative_path: str) -> list[dict]: # Typehint for list of dictionaries
    # Construct the full path to the JSON file using os.path.join()
    json_file_path =  os.path.join(os.path.abspath('.'), relative_path)

    try:
        # Authenticate with Google Sheets using the full path
        gc = gspread.service_account(filename=json_file_path)

        # Open the Google Sheet by name
        sh = gc.open('recipe_db') # Insert Google Sheet name as a global variable

        # Access the specified worksheet
        worksheet = sh.worksheet(table_name)
    
        # Return data as dict
        return worksheet.get_all_records() 

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"The file '{json_file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
