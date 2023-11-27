from helpers import get_sheet_data_as_json

# Example usage:
sheet_name = 'ingridient'
json_data = get_sheet_data_as_json(sheet_name)

if json_data is not None:
    print(f"JSON data from '{sheet_name}' sheet: {json_data}")
else:
    print("Failed to retrieve sheet data as JSON.")
