import requests
from bs4 import BeautifulSoup


def pull_amazing_strays():
    '''
    Scrape foster dogs from Amazing Strays

    Returns:
        list: List of dictionaries containing dog information
    '''

    dogs = []

    url = 'https://www.amazingstraysrescue.org/available-dogs'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # print(soup)
        test = soup.find(text='FOSTERS NEEDED').parent
        print(test)
        # for animal in animals:
        #     dogs.append({
        #         'Name': name,
        #         'Breed': breed,
        #         'Age': age,
        #         'Gender': gender,
        #         'Weight': weight,
        #         'Description': description,
        #         'Image_URL': photo,
        #         'Rescue_Name': 'Amazing Strays',
        #         'Their_Id': dog_id
        #     })

        print(f'Scraped {len(dogs)} dogs from Amazing Strays')
    except Exception as e:
        print(f'Error scraping Amazing Strays: {e}')

    return dogs
