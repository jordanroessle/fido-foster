# Foster Dog Scraper

A web scraper that aggregates foster dog listings from multiple rescue organizations and displays them on a Squarespace website.

## Project Structure

```
fido-foster-scrap/
├── .github/
│   └── workflows/
│       └── scrape-dogs.yml          # GitHub Action for daily scraping
├── scraper/
│   ├── scrape_dogs.py               # Main scraper script
│   ├── requirements.txt             # Python dependencies
│   └── rescues/
│       ├── __init__.py
│       ├── paws_of_coronado_scraper.py
│       └── cantu_foundation.py
├── docs/                            # GitHub Pages website
│   ├── index.html                   # Dog listing page
│   ├── style.css                    # Styling
│   └── app.js                       # Frontend logic
├── .gitignore
└── README.md
```
