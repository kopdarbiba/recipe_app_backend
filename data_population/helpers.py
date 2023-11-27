import os
import gspread

def get_sheet_data_as_dict(sheet_name : str, relative_path: str) -> dict:
    # Construct the full path to the JSON file using os.path.join()
    json_file_path =  os.path.join(os.path.abspath('.'), relative_path)

    try:
        # Authenticate with Google Sheets using the full path
        gc = gspread.service_account(filename=json_file_path)

        # Open the Google Sheet by name
        sh = gc.open('Kopdarbs')

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
