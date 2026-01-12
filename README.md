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

### 4. Enable GitHub Pages

1. Go to Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main`, folder: `/docs`
4. Your site will be live at: `https://yourusername.github.io/fido-foster-scrap/`

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
