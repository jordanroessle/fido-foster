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
            # Dogs only
            if animal.get('Type', '') != 'Dog':
                continue
            if animal.get('InFoster', ''):
                continue

            dog = {
                'Name': animal.get('Name', ''),
                'Breed': animal.get('Breed', ''),
                'Age': unix_to_age(animal.get('DOBUnixTime', 0)),
                'Gender': animal.get('Sex', ''),
                'Weight': animal.get('CurrentWeightPounds', '').split('.', 1)[0],
                'Description': animal.get('Description', ''),
                'Image_URL': animal.get('CoverPhoto', ''),
                'Rescue_Name': 'Paws of Coronado',
                'Their_Id': animal.get('ID', '')
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
