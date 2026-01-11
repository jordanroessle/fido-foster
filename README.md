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
│       └── paws_of_coronado_scraper.py
├── docs/                            # GitHub Pages website
│   ├── index.html                   # Dog listing page
│   ├── style.css                    # Styling
│   └── app.js                       # Frontend logic
├── .gitignore
└── README.md
```

## Setup Instructions

### 4. Enable GitHub Pages

1. Go to Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main`, folder: `/docs`
4. Your site will be live at: `https://yourusername.github.io/fido-foster-scrap/`

### 6. Add Rescue Scrapers

1. For each rescue organization, create a new scraper in `scraper/rescues/`
2. Copy the template from `rescue_a_scraper.py`
3. Update the URL and HTML selectors for that rescue's website
4. Import and call it in `scraper/scrape_dogs.py`

Example:
```python
from rescues.rescue_b_scraper import scrape_rescue_b

# In main():
dogs_b = scrape_rescue_b()
all_dogs.extend(dogs_b)
```

## Running the Scraper

### Manually (for testing)

```bash
# Install dependencies
pip install -r scraper/requirements.txt

# Set credentials (for local testing)
export GOOGLE_CREDENTIALS='<paste your JSON here>'
export PAWS_OF_CORONADO_TOKEN=

# Run scraper
python scraper/scrape_dogs.py
```

### Automatic (GitHub Actions)

- Runs daily at 8 AM UTC automatically
- Can also trigger manually from the Actions tab

## Embedding in Squarespace

1. Get your GitHub Pages URL (e.g., `https://yourusername.github.io/fido-foster-scrap/`)
2. In Squarespace, add an **Embed Block**
3. Use an iframe:
   ```html
   <iframe src="https://yourusername.github.io/fido-foster-scrap/"
           width="100%"
           height="800"
           frameborder="0">
   </iframe>
   ```

## Customization

### Styling
- Edit `docs/style.css` to match your Squarespace theme
- Colors, fonts, card layout can all be customized

### Filters
- The display page includes search and filters by default
- You can add more filters in `docs/index.html` and `docs/app.js`


## Troubleshooting

### Scraper not running
- Check the Actions tab in GitHub for error logs
- Verify `GOOGLE_CREDENTIALS` secret is set correctly
- Make sure the service account has access to the sheet

### Dogs not displaying
- Check that the Google Sheet CSV is published and public
- Verify the CSV URL in `docs/app.js` is correct
- Open browser console for JavaScript errors

### Need to update a dog manually
- Edit directly in the Google Sheet
- Changes appear on next page load (CSV updates automatically)

## Security Notes

- **NEVER** commit the JSON credentials file to Git
- Keep the `.gitignore` file in place
- Only store credentials in GitHub Secrets
- The Google Sheet should be private (only shared with the service account)
- The published CSV is public - don't include sensitive data
