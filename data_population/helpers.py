import os
import gspread
import pandas as pd

def get_sheet_data_as_json(sheet_name):
    # Specify the directory where the JSON file is located
    base_dir = '/home/tom/code/kopdarbiba/recipe_app_backend/data_population/'

    # Construct the full path to the JSON file using os.path.join()
    json_file_path = os.path.join(base_dir, 'recipeapp.json')

    try:
        # Authenticate with Google Sheets using the full path
        gc = gspread.service_account(filename=json_file_path)

        # Open the Google Sheet by name
        sh = gc.open('Kopdarbs')

        # Access the specified worksheet
        worksheet = sh.worksheet(sheet_name)

        # Convert the worksheet data to a DataFrame
        df = pd.DataFrame(worksheet.get_all_records())

        # Convert the DataFrame to JSON
        json_data = df.to_json(orient='records')

        return json_data

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"The file '{json_file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
