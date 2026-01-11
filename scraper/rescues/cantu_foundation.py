import requests
from bs4 import BeautifulSoup


def pull_cantu_foundation():
    '''
    Scrape foster dogs from Cantu Foundation

    Returns:
        list: List of dictionaries containing dog information
    '''

    dogs = []

    # The actual dog listings are in this iframe
    url = 'https://www.thecantufoundation.org/foster'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        animals = soup.find_all('div',class_='sqs-gallery-design-autogrid-slide')
        for animal in animals:
            title_link = animal.find('a', class_='summary-title-link')
            name = title_link.text.strip().title()

            # Extract ID from URL (e.g., '/fosterdogs/dotty' -> 'dotty')
            dog_url = title_link['href']
            dog_id = dog_url.split('/')[-1]

            photo = animal.find('img')['data-src']
            more_info = animal.find('div', class_='summary-excerpt').text
            # Remove zero-width characters
            for char in ['\u200b', '\u200c', '\u200d', '\u200e', '\u200f']:
                more_info = more_info.replace(char, '')
            more_info = more_info.strip()

            # Parse the more_info text
            age = ''
            gender = ''
            size = ''
            breed = ''
            description = ''

            # Split from the end backwards to avoid issues with missing fields
            if 'More about me:' in more_info:
                first_split = more_info.split('More about me:', 1)
                description = first_split[1].strip()
                fields_text = first_split[0]
            else:
                fields_text = more_info

            if 'Breed:' in fields_text:
                second_split = fields_text.split('Breed:', 1)
                breed = second_split[1].strip().title()
                fields_text = second_split[0]

            if 'Size:' in fields_text:
                third_split = fields_text.split('Size:', 1)
                size = third_split[1].strip()
                fields_text = third_split[0]

            if 'Gender:' in fields_text:
                fourth_split = fields_text.split('Gender:', 1)
                gender = fourth_split[1].strip().title()
                fields_text = fourth_split[0]

            if 'Age:' in fields_text:
                fifth_split = fields_text.split('Age:', 1)
                age = fifth_split[1].strip()

            dogs.append({
                'Name': name,
                'Breed': breed,
                'Age': age,
                'Gender': gender,
                'Size': size,
                'Description': description,
                'Image_URL': photo,
                'Rescue_Name': 'Cantu Foundation',
                'Their_Id': dog_id
            })


    except Exception as e:
        print(f'Error scraping Cantu Foundation: {e}')

    return dogs
