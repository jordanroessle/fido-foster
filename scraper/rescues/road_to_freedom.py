import re

import requests
from bs4 import BeautifulSoup


def parse_description_info(description):
    '''
    Parse age, gender, and weight from description text.

    Handles formats like:
    - "My name is Ellie. I am a one and a half year old female who weighs 50 pounds."
    - "Ruby, one and a half, female, 20 pounds"

    Returns:
        dict: Dictionary with 'age', 'gender', and 'weight' keys
    '''
    info = {'age': '', 'gender': '', 'weight': ''}

    if not description:
        return info

    # Try to extract weight (e.g., "50 pounds", "20 pounds")
    weight_match = re.search(r'(\d+)\s*pounds?', description, re.IGNORECASE)
    if weight_match:
        info['weight'] = weight_match.group(1)

    # Try to extract gender
    if re.search(r'\bfemale\b', description, re.IGNORECASE):
        info['gender'] = 'Female'
    elif re.search(r'\bmale\b', description, re.IGNORECASE):
        info['gender'] = 'Male'

    # Try to extract age patterns
    # Matches: "one and a half year old", "2 year old", "3 years old", "one and a half," etc.
    age_pattern = r'(\w+\s+and\s+a\s+half|\d+(?:\.\d+)?)\s*(?:years?\s*old)?(?:,|\.|\s|$)'

    # Word to number mapping for common ages
    word_to_num = {
        'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
        'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10'
    }

    age_match = re.search(age_pattern, description, re.IGNORECASE)
    if age_match:
        age_text = age_match.group(1)
        # Handle "X and a half" format
        if 'and a half' in age_text.lower():
            # Extract the number part before "and a half"
            num_match = re.match(r'(\w+)\s+and\s+a\s+half', age_text, re.IGNORECASE)
            if num_match:
                num_part = num_match.group(1).lower()
                # Convert word to number if needed
                if num_part in word_to_num:
                    info['age'] = f"{word_to_num[num_part]}.5"
                elif num_part.isdigit():
                    info['age'] = f"{num_part}.5"
        else:
            # Check if it's a word number
            if age_text.lower() in word_to_num:
                info['age'] = word_to_num[age_text.lower()]
            else:
                info['age'] = age_text

    return info


def pull_road_to_freedom():
    '''
    Scrape foster dogs from Road To Freedom

    Returns:
        list: List of dictionaries containing dog information
    '''

    dogs = []

    url = 'https://roadtofreedomrescue.com/forever-foster-dogs/'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        animals = soup.find_all(class_='Bzl-dog-post')

        for animal in animals:
            # Extract name from the heading link
            name_elem = animal.find('div', class_='Bzl-dog-heading').find('a')
            name = name_elem.text.strip() if name_elem else ''

            # Extract ID from the data-name attribute or URL
            dog_id = animal.get('data-name', '').strip()
            if not dog_id and name_elem:
                # Fallback to extracting from URL
                url_href = name_elem.get('href', '')
                if url_href:
                    dog_id = url_href.rstrip('/').split('/')[-1]

            # Extract image URL
            img_elem = animal.find('div', class_='Bzl-dog-img').find('img') if animal.find('div', class_='Bzl-dog-img') else None
            image_url = img_elem.get('src', '') if img_elem else ''

            # Extract description
            description_elem = animal.find('div', class_='Bzl-dog-description')
            description = description_elem.find('p').text.strip() if description_elem and description_elem.find('p') else ''

            # Extract breed, gender, and age from meta section
            meta_div = animal.find('div', class_='Bzl-dog-meta')
            breed = ''
            gender = ''
            age = ''

            if meta_div:
                meta_rows = meta_div.find_all('div', class_='col-12')
                for row in meta_rows:
                    icon = row.find('i')
                    if icon:
                        if 'icon-dog-face' in icon.get('class', []):
                            breed = row.text.strip().replace('\n', '').strip()
                        elif 'icon-female-sign' in icon.get('class', []):
                            gender = 'Female'
                        elif 'icon-male-sign' in icon.get('class', []):
                            gender = 'Male'
                        elif 'icon-cake' in icon.get('class', []):
                            age = row.text.strip().replace('\n', '').strip()

            # Parse additional info from description
            desc_info = parse_description_info(description)

            # Use description info as fallback if meta info is missing
            if not gender and desc_info['gender']:
                gender = desc_info['gender']
            if (not age or age == '0  Days Old') and desc_info['age']:
                age = desc_info['age']

            weight = desc_info['weight']

            dogs.append({
                'Name': name,
                'Breed': breed,
                'Age': age,
                'Gender': gender,
                'Weight': weight,
                'Description': description,
                'Image_URL': image_url,
                'Rescue_Name': 'Road To Freedom',
                'Their_Id': dog_id
            })

        print(f'Scraped {len(dogs)} dogs from Road To Freedom')
    except Exception as e:
        print(f'Error scraping Road To Freedom: {e}')

    return dogs
