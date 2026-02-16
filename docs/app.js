// Configuration
const CONFIG = {
    SHEET_URL: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSci-XCd0ne906VzOafwYm2k4P6i32G5dhZNUkvT0qxYGSmjOCpD5VIZ4rVB_fxuuNvBLjf8stmKbBu/pub?gid=0&single=true&output=tsv'
};

let allDogs = [];

const SMALL_WEIGHT_CUTOFF = 25;
const MEDIUM_WEIGHT_CUTOFF = 50;
const LARGE_WEIGHT_CUTOFF = 75;
const FOSTER_MATCHING_URL = 'https://www.fidofostercommunity.org/fostermatchingform';

// Load and display dogs
async function loadDogs() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');

    try {
        loadingEl.style.display = 'block';
        errorEl.style.display = 'none';

        const response = await fetch(CONFIG.SHEET_URL);
        if (!response.ok) throw new Error('Failed to fetch data');

        const csvText = await response.text();
        allDogs = parseCSV(csvText);

        populateFilters();
        displayDogs(allDogs);

        loadingEl.style.display = 'none';
    } catch (error) {
        console.error('Error loading dogs:', error);
        loadingEl.style.display = 'none';
        errorEl.textContent = 'Failed to load dogs. Please try again later.';
        errorEl.style.display = 'block';
    }
}

// Parse CSV data (now TSV format)
function parseCSV(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split('\t').map(h => h.trim());
    const dogs = [];

    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;

        const values = lines[i].split('\t');
        const dog = {};

        headers.forEach((header, index) => {
            dog[header] = values[index] ? values[index].trim() : '';
        });

        dogs.push(dog)
    }

    return dogs;
}

// Display dogs in grid
function displayDogs(dogs) {
    const gridEl = document.getElementById('dogs-grid');

    if (dogs.length === 0) {
        gridEl.innerHTML = '<p style="text-align: center; width: 100%; padding: 40px;">No dogs found.</p>';
        return;
    }

    gridEl.innerHTML = dogs.map(dog => createDogCard(dog)).join('');

    requestAnimationFrame(() => hideUnnecessaryShowMoreButtons());
}

// Create HTML for dog card
function createDogCard(dog) {
    const imageHTML = dog.Image_URL
        ? `<img src="${dog.Image_URL}" alt="${dog.Name}" class="dog-image">`
        : `<div class="dog-image placeholder">🐕</div>`;

    return `
        <div class="dog-card">
            ${imageHTML}
            <div class="dog-info">
                <h2 class="dog-name">${dog.Name || 'Unknown'}</h2>
                ${dog.Breed ? `<div class="dog-detail"><strong>Breed:</strong> ${dog.Breed}</div>` : ''}
                ${dog.Age ? `<div class="dog-detail"><strong>Age:</strong> ${dog.Age}</div>` : ''}
                ${dog.Gender ? `<div class="dog-detail"><strong>Gender:</strong> ${dog.Gender}</div>` : ''}
                ${dog.Weight ? `<div class="dog-detail"><strong>Weight:</strong> ${dog.Weight} lbs</div>` : ''}
                ${dog.Rescue_Name ? `<div class="dog-detail-underline"><strong>Rescue:</strong> ${dog.Rescue_Name}</div>` : ''}
                <div class="dog-description truncated">${dog.Description ? dog.Description.replaceAll('$$', '<br>') : `Contact us for further information on ${dog.Name}'s personality`}</div>
                <button class="show-more-btn" onclick="toggleDescription(this)">Show more</button>
                <a href="${FOSTER_MATCHING_URL}" target="_blank" class="foster-button-link"><span class="foster-button">Foster ${dog.Name}</span></a>
            </div>
        </div>
    `;
}

// Populate filter dropdowns
function populateFilters() {
    const rescueFilter = document.getElementById('rescue-filter');
    const rescues = [...new Set(allDogs.map(dog => dog.Rescue_Name).filter(Boolean))];

    rescues.forEach(rescue => {
        const option = document.createElement('option');
        option.value = rescue;
        option.textContent = rescue;
        rescueFilter.appendChild(option);
    });
}

// Filter dogs based on search and filters
function filterDogs() {
    const genderFilter = document.getElementById('gender-filter').value
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const weightFilter = document.getElementById('weight-filter').value;
    const rescueFilter = document.getElementById('rescue-filter').value;

    const filtered = allDogs.filter(dog => {
        const matchesGender = !genderFilter || dog.Gender === genderFilter;

        const matchesSearch = !searchTerm ||
            dog.Name.toLowerCase().includes(searchTerm) ||
            dog.Breed.toLowerCase().includes(searchTerm) ||
            dog.Description.toLowerCase().includes(searchTerm);

        const matchesRescue = !rescueFilter || dog.Rescue_Name === rescueFilter;

        const weight = parseInt(dog.Weight)
        let matchesWeight;
        switch (weightFilter) {
            case 'Small':
                matchesWeight = weight <= SMALL_WEIGHT_CUTOFF;
                break;
            case 'Medium':
                matchesWeight = weight <= MEDIUM_WEIGHT_CUTOFF && weight > SMALL_WEIGHT_CUTOFF;
                break;
            case 'Large':
                matchesWeight = weight <= LARGE_WEIGHT_CUTOFF && weight > MEDIUM_WEIGHT_CUTOFF;
                break;
            case 'X-Large':
                matchesWeight = weight > LARGE_WEIGHT_CUTOFF;
                break;
            default:
                matchesWeight = true;
                break;
        }

        return matchesGender && matchesSearch && matchesWeight && matchesRescue;
    });

    displayDogs(filtered);
}

// Event listeners
document.getElementById('gender-filter').addEventListener('change', filterDogs)
document.getElementById('search').addEventListener('input', filterDogs);
document.getElementById('weight-filter').addEventListener('change', filterDogs);
document.getElementById('rescue-filter').addEventListener('change', filterDogs);

function toggleDescription(btn) {
    const description = btn.previousElementSibling;
    const isExpanded = description.classList.contains('expanded');

    if (isExpanded) {
        description.classList.remove('expanded');
        description.classList.add('truncated');
        btn.textContent = 'Show more';
    } else {
        description.classList.remove('truncated');
        description.classList.add('expanded');
        btn.textContent = 'Show less';
    }
}

function hideUnnecessaryShowMoreButtons() {
    document.querySelectorAll('.dog-description.truncated').forEach(desc => {
        const btn = desc.nextElementSibling;
        if (btn && btn.classList.contains('show-more-btn')) {
            // Check if content is actually truncated
            if (desc.scrollHeight <= desc.clientHeight) {
                btn.style.display = 'none';
            } else {
                btn.style.display = 'block';
            }
        }
    });
}

// Load dogs on page load
loadDogs();
