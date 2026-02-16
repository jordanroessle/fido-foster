import os

import requests
from bs4 import BeautifulSoup


def pull_amazing_strays():
    '''
    Scrape foster dogs from Amazing Strays

    Returns:
        list: List of dictionaries containing dog information
    '''

    dogs = []

    api_url = 'https://api.monday.com/v2'
    soup_url = 'https://www.amazingstraysrescue.org/available-dogs'
    api_key = os.getenv('AMAZING_STRAYS_TOKEN')
    headers = {"Authorization" : api_key, "Content-Type": "application/json"}

    try:
        query = """query {
                        boards(ids: 5132337088) {
                            tempFostersGroup: groups(ids: "new_group71968") {
                                items_page(
                                    query_params: {
                                        rules: [{ column_id: "status", compare_value: [4], operator: not_any_of }]
                                    }
                                ) {
                                    items {
                                        name
                                        }
                                    }
                                }
                                needsFoster: items_page(
                                    query_params: {
                                        rules: [{ column_id: "status", compare_value: [14, 18], operator: any_of }]
                                    }
                                ) {
                                    items {
                                        name
                                    }
                                }
                            }
                        }"""
        data = {'query' : query}
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()

        current_dogs = []
        temp_needed = response.json()['data']['boards'][0]['tempFostersGroup'][0]['items_page']['items']
        other_dogs = response.json()['data']['boards'][0]['needsFoster']['items']

        current_dogs.extend(temp_needed)
        current_dogs.extend(other_dogs)

        soup_html = requests.get(soup_url, timeout=10)
        soup_html.raise_for_status()
        for dog in current_dogs:
            name_to_search = dog.get('name', '').split(' ')[0]
            result = get_dog_info(soup_html.content, name_to_search)
            if result:
                print(result)
            print(dog)
            break


        print(f'Scraped {len(dogs)} dogs from Amazing Strays')
    except Exception as e:
        print(f'Error scraping Amazing Strays: {e}')

    return dogs



def get_dog_info(html, dog_name):
    soup = BeautifulSoup(html, 'html.parser')

    # Find the title element containing the dog's name
    title_elem = soup.find('div', {'data-hook': 'item-title'}, string=lambda t: t and t.strip().startswith(dog_name))

    if not title_elem:
        # Try finding the span inside
        title_span = soup.find('span', string=dog_name)
        if title_span:
            title_elem = title_span.find_parent('div', {'data-hook': 'item-title'})

    if not title_elem:
        return get_dog_from_adopt_list(soup, dog_name)

    # Extract full name from the title element
    full_name = title_elem.get_text(strip=True)

    # Get the container
    container = title_elem.find_parent('div', class_='gallery-item-container')

    # Get the image
    img = container.find('img', {'data-hook': 'gallery-item-image-img'})
    image_url = img['src'] if img else None

    # Get the description
    desc_elem = container.find('div', {'data-hook': 'item-description'})
    description = desc_elem.get_text(strip=True) if desc_elem else None

    return {
        'name': full_name,
        'image': image_url,
        'description': description
    }


def get_dog_from_adopt_list(soup, dog_name):
    '''
    Fallback function to get dog image from get dog from adopt list
    '''

    # Find img with alt text starting with dog name
    img = soup.find('img', alt=lambda a: a and a.lower().startswith(dog_name.lower()))

    if not img:
        return None

    image_url = img.get('src')

    # Extract full name from alt text (e.g., "Georgie May's preview photo" -> "Georgie May")
    alt_text = img.get('alt', '')
    full_name = alt_text.replace("'s preview photo", '').strip()

    return {
        'name': full_name,
        'image': image_url,
        'description': None
    }
