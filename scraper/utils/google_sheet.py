
import json
import os
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

CURRENT_SHEET_NAME = 'Current'
ARCHIVE_SHEET_NAME = 'Archive'
LOGS_SHEET_NAME = 'Logs'

def get_google_spreadsheet():
    '''
    Authenticate and return the Google Sheet.
    Uses ENVIRONMENT variable to determine which sheet to use:
    - 'production' or unset: uses production sheet
    - 'development': uses test sheet
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

    # Determine which spreadsheet to use based on environment
    environment = os.getenv('ENVIRONMENT', 'development').lower()

    if environment == 'production':
        sheet_name = 'Fido Foster Dogs Database'
        print(f'Using PRODUCTION sheet: {sheet_name}')
    else:
        sheet_name = os.getenv('DEV_SHEET_NAME', 'Fido Foster Dogs Database - TEST')
        print(f'Using DEVELOPMENT sheet: {sheet_name}')

    spreadsheet = client.open(sheet_name)
    return spreadsheet

def update_sheet_with_dogs(spreadsheet: gspread.Spreadsheet, dogs):
    '''Update Google Sheet with scraped dog data.'''
    current = spreadsheet.worksheet(CURRENT_SHEET_NAME)
    archive = spreadsheet.worksheet(ARCHIVE_SHEET_NAME)
    logs = spreadsheet.worksheet(LOGS_SHEET_NAME)
    existing_dogs = current.get_all_records()

    # Build lookup dictionary using composite key: (Their_Id, Rescue_Name) -> (index, dog_data)
    # This allows different rescues to have the same ID without conflicts
    existing_lookup = {
        (str(dog.get('Their_Id', '')), str(dog.get('Rescue_Name', ''))): (idx, dog)
        for idx, dog in enumerate(existing_dogs)
        if dog.get('Their_Id', '') and dog.get('Rescue_Name', '')
    }

    # Track which dogs from the sheet are found in the current scrape
    # Start with all existing keys, we'll remove them as we see them
    existing_keys = set(existing_lookup.keys())
    incoming_keys = set()

    new_dogs_count = 0
    updated_dogs_count = 0
    removed_dogs_count = 0
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for dog in dogs:
        # Create composite key from Their_Id and Rescue_Name
        dog_id = str(dog.get('Their_Id', ''))
        rescue_name = str(dog.get('Rescue_Name', ''))
        composite_key = (dog_id, rescue_name)

        '''
        If for some reason we are missing id or rescue
        We will log it and skip it
        '''
        if not dog_id or not rescue_name:
            logs.append_row([
                time_now,
                'Missing dog_id or rescue_name',
                json.dumps(dog)
            ])
            continue

        incoming_keys.add(composite_key)

        # Add new dog
        if composite_key not in existing_lookup:
            current.append_row([
                dog.get('Name', ''),
                dog.get('Breed', ''),
                dog.get('Age', ''),
                dog.get('Gender', ''),
                dog.get('Weight', ''),
                dog.get('Description', ''),
                dog.get('Image_URL', ''),
                dog.get('Rescue_Name', ''),
                dog.get('Their_Id', ''),
                time_now,
                'false' # Manually edited
            ])
            new_dogs_count += 1
            continue

        # Else find the existing dog by index
        idx, existing_dog = existing_lookup[composite_key]
        row_number = idx + 2  # +2 because sheets are 1-indexed and row 1 is header

        # skip manually edited dogs
        manually_edited = str(existing_dog.get('Manually_Edited', '')).lower()
        if manually_edited != 'false':
            continue

        # Check if any fields have changed
        has_changes = (
            existing_dog.get('Name', '') != dog.get('Name', '') or
            existing_dog.get('Breed', '') != dog.get('Breed', '') or
            existing_dog.get('Age', '') != dog.get('Age', '') or
            existing_dog.get('Gender', '') != dog.get('Gender', '') or
            str(existing_dog.get('Weight', '')) != dog.get('Weight', '') or
            existing_dog.get('Description', '') != dog.get('Description', '') or
            existing_dog.get('Image_URL', '') != dog.get('Image_URL', '')
        )

        if has_changes:
            # Update the entire row with new data
            current.update(range_name=f'A{row_number}:J{row_number}', values=[[
                dog.get('Name', ''),
                dog.get('Breed', ''),
                dog.get('Age', ''),
                dog.get('Gender', ''),
                dog.get('Weight', ''),
                dog.get('Description', ''),
                dog.get('Image_URL', ''),
                dog.get('Rescue_Name', ''),
                dog.get('Their_Id', ''),
                time_now
            ]])
            updated_dogs_count += 1

    # Find dogs that are no longer available (in sheet but not in incoming scrape)
    removed_keys = existing_keys - incoming_keys

    # Move removed dogs to archive sheet (in reverse order to maintain row numbers)
    for key in sorted(removed_keys, key=lambda k: existing_lookup[k][0], reverse=True):
        idx, dog_data = existing_lookup[key]
        row_number = idx + 2

        # Add to archive sheet
        archive.append_row([
            dog_data.get('Name', ''),
            dog_data.get('Breed', ''),
            dog_data.get('Age', ''),
            dog_data.get('Gender', ''),
            dog_data.get('Weight', ''),
            dog_data.get('Description', ''),
            dog_data.get('Image_URL', ''),
            dog_data.get('Rescue_Name', ''),
            dog_data.get('Their_Id', ''),
            dog_data.get('Last_Updated', ''),
            dog_data.get('Manually_Edited', '')
        ])

        # Delete from main sheet
        current.delete_rows(row_number)
        removed_dogs_count += 1

    print(f'Added {new_dogs_count} new dogs')
    print(f'Moved {removed_dogs_count} unavailable dogs to archive')
    print(f'Updated {updated_dogs_count} existing dogs')
