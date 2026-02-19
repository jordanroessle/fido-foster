from utils.google_sheet import get_google_spreadsheet


def pull_cantu_foundation():
    '''
    Scrape foster dogs from Cantu Foundation.

    Returns:
        list: List of dictionaries containing dog information
    '''

    rescue_name = 'Cantu Foundation'
    dogs = []
    spreadsheet_name = 'TCF x Fido spreadsheet'
    stop_at = 'DOGS IN SAN DIEGO'
    name_header = '' # IMPORTRANGE doesn't pull the header, so we have to use a blank column as the name key

    try:
        spreadsheet = get_google_spreadsheet(spreadsheet_name)
        print(f'Successfully accessed spreadsheet: {spreadsheet_name}')
        worksheet = spreadsheet.sheet1
        rows = worksheet.get_all_records()

        for row in rows:
            name = row.get(name_header, '')
            if name == stop_at:
                break

            has_foster = row.get('Foster lined up', '').strip().lower()
            note_for_website = row.get('Notes for website ', '').strip().lower()
            if has_foster == '' and note_for_website != '':
                dog = {
                    'Name': name,
                    'Breed': row.get('Breed', ''),
                    'Age': row.get('Age ', ''),
                    'Gender': row.get('Gender', ''),
                    'Weight': row.get('Weight', ''),
                    'Description': note_for_website,
                    'Image_URL': row.get('Image', ''),
                    'Rescue_Name': rescue_name,
                    'Their_Id': f'{name}_{row.get("Fur Color", "")}'
                }
                dogs.append(dog)
        print(f'Scraped {len(dogs)} dogs from {rescue_name}')

    except Exception as e:
        print(f'Error accessing spreadsheet: {repr(e)}')
        return []
    return dogs
