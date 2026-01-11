
import json
import os
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_google_sheet():
    '''
    Authenticate and return the Google Sheet.
    '''

    creds_json = os.getenv('GOOGLE_CREDENTIALS')

    if not creds_json:
        raise ValueError('GOOGLE_CREDENTIALS environment variable not set')

    creds_dict = json.loads(creds_json)

    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open('Fido Foster Dogs Database').sheet1
    return sheet

def update_sheet_with_dogs(sheet: gspread.Worksheet, dogs):
    '''Update Google Sheet with scraped dog data.'''
    existing_dogs = sheet.get_all_records()

    # Build lookup dictionary: Their_Id -> (index, dog_data)
    # Convert all IDs to strings for consistency across different rescues
    existing_lookup = {
        str(dog.get('Their_Id', '')): (idx, dog)
        for idx, dog in enumerate(existing_dogs)
        if dog.get('Their_Id', '')
    }

    new_dogs_count = 0
    updated_dogs_count = 0

    for dog in dogs:
        dog['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Convert to string to match lookup dictionary
        dog_id = str(dog.get('Their_Id', '')) if dog.get('Their_Id') else ''

        if not dog_id or dog_id not in existing_lookup:
            # Add new dog
            sheet.append_row([
                dog.get('Name', ''),
                dog.get('Breed', ''),
                dog.get('Age', ''),
                dog.get('Gender', ''),
                dog.get('Size', ''),
                dog.get('Description', ''),
                dog.get('Image_URL', ''),
                dog.get('Rescue_Name', ''),
                dog.get('Their_Id', ''),
                dog.get('Last_Updated', '')
            ])
            new_dogs_count += 1
        else:
            # Find the existing dog by index
            idx, existing_dog = existing_lookup[dog_id]
            row_number = idx + 2  # +2 because sheets are 1-indexed and row 1 is header

            # Check if any fields have changed
            has_changes = (
                existing_dog.get('Name', '') != dog.get('Name', '') or
                existing_dog.get('Breed', '') != dog.get('Breed', '') or
                existing_dog.get('Age', '') != dog.get('Age', '') or
                existing_dog.get('Gender', '') != dog.get('Gender', '') or
                existing_dog.get('Size', '') != dog.get('Size', '') or
                existing_dog.get('Description', '') != dog.get('Description', '') or
                existing_dog.get('Image_URL', '') != dog.get('Image_URL', '')
            )

            if has_changes:
                # Update the entire row with new data
                sheet.update(range_name=f'A{row_number}:J{row_number}', values=[[
                    dog.get('Name', ''),
                    dog.get('Breed', ''),
                    dog.get('Age', ''),
                    dog.get('Gender', ''),
                    dog.get('Size', ''),
                    dog.get('Description', ''),
                    dog.get('Image_URL', ''),
                    dog.get('Rescue_Name', ''),
                    dog.get('Their_Id', ''),
                    dog.get('Last_Updated', '')
                ]])
                updated_dogs_count += 1

    print(f'Added {new_dogs_count} new dogs')
    print(f'Updated {updated_dogs_count} existing dogs')
