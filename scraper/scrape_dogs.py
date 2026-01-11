from dotenv import load_dotenv
from rescues.cantu_foundation import pull_cantu_foundation
from rescues.paws_of_coronado_scraper import pull_paws_of_coronado
from utils.google_sheet import get_google_sheet, update_sheet_with_dogs

load_dotenv()

def main():
    '''
    Main scraping workflow.
    '''
    print('Starting foster dog scraper...')

    # Get Google Sheet
    sheet = get_google_sheet()

    # Grab info from all rescue sources
    all_dogs = []

    # Paws of Coronado
    print('Pulling from Paws of Coronado')
    paws_dogs = pull_paws_of_coronado()
    all_dogs.extend(paws_dogs)

    # Cantu Foundation
    print('Pulling from Cantu Foundation')
    cantu_foundation_dogs = pull_cantu_foundation()
    all_dogs.extend(cantu_foundation_dogs)

    print(f'Total dogs info grabbed: {len(all_dogs)}')

    # # Update sheet
    if all_dogs:
        update_sheet_with_dogs(sheet, all_dogs)
        print('Sheet updated successfully!')
    else:
        print('No dogs found to update')


if __name__ == '__main__':
    main()
