from utils.google_sheet import get_google_spreadsheet


def pull_mother_of_dragons():
    '''
    Scrape foster dogs from Mother of Dragons Rescue.

    Returns:
        list: List of dictionaries containing dog information
    '''

    rescue_name = 'Mother of Dragons'
    dogs = []
    spreadsheet_name = 'Mother of Dragons Foster Dog List'

    try:
        spreadsheet = get_google_spreadsheet(spreadsheet_name)
        print(f'Successfully accessed spreadsheet: {spreadsheet_name}')
        worksheet = spreadsheet.sheet1
        rows = worksheet.get_all_records()
        for row in rows:
            dog = {
                'Name': row.get('Name', ''),
                'Breed': row.get('Breed', ''),
                'Age': row.get('Age', ''),
                'Gender': row.get('Gender', ''),
                'Weight': row.get('Weight', ''),
                'Description': row.get('Description / Bio', '').replace('\n', '$$'),
                'Image_URL': row.get('Image', ''),
                'Rescue_Name': rescue_name,
                'Their_Id': f'{row.get("Name", "")}_{row.get("Breed", "")}'
            }
            dogs.append(dog)

        print(f'Scraped {len(dogs)} dogs from {rescue_name}')

    except Exception as e:
        print(f'Error accessing spreadsheet: {repr(e)}')
        return []
    return dogs
