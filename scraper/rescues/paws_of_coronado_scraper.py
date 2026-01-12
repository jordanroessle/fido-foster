import os
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta


def pull_paws_of_coronado():
    '''
    Scrape foster dogs from Paws of Coronado

    Returns:
        list: List of dictionaries containing dog information
    '''

    dogs = []
    url = 'https://new.shelterluv.com/api/v1/animals'
    token = os.getenv('PAWS_OF_CORONADO_TOKEN')

    try:
        response = requests.get(url, params={'status_type': 'in custody'}, timeout=10, headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()

        animals = response.json()['animals']

        for animal in animals:
            # Dogs only, skip in foster, skip Lifetime Care Program
            if animal.get('Type', '') != 'Dog' or animal.get('InFoster', '') or animal.get('Status', '') == 'Lifetime Care Program':
                continue

            # Build description from published attributes
            attributes = animal.get('Attributes', [])
            description = '$$'.join(
                attr.get('AttributeName', '')
                for attr in attributes
                if attr.get('Publish') == 'Yes' and attr.get('AttributeName')
            )
            dog = {
                'Name': animal.get('Name', ''),
                'Breed': animal.get('Breed', ''),
                'Age': unix_to_age(animal.get('DOBUnixTime', 0)),
                'Gender': animal.get('Sex', ''),
                'Weight': animal.get('CurrentWeightPounds', '').split('.', 1)[0],
                'Description': description,
                'Image_URL': animal.get('CoverPhoto', ''),
                'Rescue_Name': 'Paws of Coronado',
                'Their_Id': animal.get('Internal-ID', '')
            }
            dogs.append(dog)

        print(f'Scraped {len(dogs)} dogs from Paws of Coronado')

    except requests.RequestException as e:
        print(f'Error scraping Paws of Coronado: {e}')

    return dogs

def unix_to_age(unix_timestamp):
    '''
    Convert unix timestamp to age in Y/M/D format

    Args:
        unix_timestamp: Unix timestamp (seconds since epoch)

    Returns:
        str: Age in format 'XY/XM/XD'
    '''

    birth_date = datetime.fromtimestamp(unix_timestamp)
    now = datetime.now()
    diff = relativedelta(now, birth_date)

    return f'{diff.years}Y/{diff.months}M/{diff.days}D'
