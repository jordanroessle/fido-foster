// Configuration
const CONFIG = {
    SHEET_URL: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSci-XCd0ne906VzOafwYm2k4P6i32G5dhZNUkvT0qxYGSmjOCpD5VIZ4rVB_fxuuNvBLjf8stmKbBu/pub?gid=1773829289&single=true&output=tsv'
}
let allActivities = [];

// Load and display activities
async function loadActivities() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');

    try {
        loadingEl.style.display = 'block';
        errorEl.style.display = 'none';

        const response = await fetch(CONFIG.SHEET_URL);
        if (!response.ok) throw new Error('Failed to fetch data');

        const tsvText = await response.text();
        allActivities = parseTSV(tsvText);

        displayActivities(allActivities);

        loadingEl.style.display = 'none';
    } catch (error) {
        console.error('Error loading activities:', error);
        loadingEl.style.display = 'none';
        errorEl.textContent = 'Failed to load activities. Please try again later.';
        errorEl.style.display = 'block';
    }
}

// Parse TSV data
function parseTSV(tsv) {
    const lines = tsv.split('\n');
    const headers = lines[0].split('\t').map(h => h.trim());
    const activities = [];

    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;

        const values = lines[i].split('\t');
        const activity = {};

        headers.forEach((header, index) => {
            activity[header] = values[index] ? values[index].trim() : '';
        });

        activities.push(activity);
    }

    return activities;
}

// Display activities in grid
function displayActivities(activities) {
    const gridEl = document.getElementById('activities-grid');

    if (activities.length === 0) {
        gridEl.innerHTML = '<p style="text-align: center; width: 100%; padding: 40px;">No activities found.</p>';
        return;
    }

    gridEl.innerHTML = activities.map(activity => createActivityCard(activity)).join('');
}

// Create HTML for activity card
function createActivityCard(activity) {
    const imageHTML = activity.Image
        ? `<img src="${activity.Image}" alt="${activity.Name}" class="dog-image">`
        : `<div class="dog-image placeholder">${activity.Name}</div>`;

    return `
        <div class="dog-card">
            ${imageHTML}
            <div class="dog-info">
                <h2 class="dog-name">${activity.Name || 'Unknown'}</h2>
                ${activity.Business ? `<div class="dog-detail"><strong>Business:</strong> ${activity.Business}</div>` : ''}
                ${activity.City ? `<div class="dog-detail"><strong>City:</strong> ${activity.City}</div>` : ''}
                ${activity.Deal ? `<div class="dog-detail-underline"><strong>Deal:</strong> ${activity.Deal}</div>` : ''}
                ${activity.Description ? `<div class="dog-description">${activity.Description.replaceAll('$$', '<br>')}</div>` : ''}
            </div>
        </div>
    `;
}

// Load activities on page load
loadActivities();
