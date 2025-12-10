import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from datetime import datetime
from rescues.rescue_a_scraper import scrape_rescue_a
# from rescues.rescue_b_scraper import scrape_rescue_b  # Add more as needed


def get_google_sheet():
    """Authenticate and return the Google Sheet."""
    # Load credentials from environment variable (GitHub Secret)
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')

    if not creds_json:
        raise ValueError("GOOGLE_CREDENTIALS environment variable not set")

    creds_dict = json.loads(creds_json)

    # Authenticate
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Open your sheet (by name)
    # TODO: Replace with your actual Google Sheet name
    sheet = client.open("Foster Dogs Database").sheet1
    return sheet


def update_sheet_with_dogs(sheet, dogs):
    """Update Google Sheet with scraped dog data."""
    # Get existing data to avoid duplicates
    existing_dogs = sheet.get_all_records()
    existing_names = {dog.get('Name', '') for dog in existing_dogs}

    new_dogs_count = 0
    updated_dogs_count = 0

    for dog in dogs:
        dog['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if dog['Name'] not in existing_names:
            # Add new dog
            sheet.append_row([
                dog.get('Name', ''),
                dog.get('Breed', ''),
                dog.get('Age', ''),
                dog.get('Gender', ''),
                dog.get('Size', ''),
                dog.get('Location', ''),
                dog.get('Description', ''),
                dog.get('Image_URL', ''),
                dog.get('Rescue_Name', ''),
                dog.get('Available', 'Yes'),
                dog.get('Last_Updated', '')
            ])
            new_dogs_count += 1
        else:
            # TODO: Implement update logic for existing dogs if needed
            updated_dogs_count += 1

    print(f"Added {new_dogs_count} new dogs")
    print(f"Found {updated_dogs_count} existing dogs")


def main():
    """Main scraping workflow."""
    print("Starting foster dog scraper...")

    # Get Google Sheet
    sheet = get_google_sheet()

    # Scrape from all rescue sources
    all_dogs = []

    # Rescue A
    print("Scraping Rescue A...")
    dogs_a = scrape_rescue_a()
    all_dogs.extend(dogs_a)

    # Add more rescues here
    # print("Scraping Rescue B...")
    # dogs_b = scrape_rescue_b()
    # all_dogs.extend(dogs_b)

    print(f"Total dogs scraped: {len(all_dogs)}")

    # Update sheet
    if all_dogs:
        update_sheet_with_dogs(sheet, all_dogs)
        print("Sheet updated successfully!")
    else:
        print("No dogs found to update")


if __name__ == "__main__":
    main()
