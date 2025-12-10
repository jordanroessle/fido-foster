// Configuration
const CONFIG = {
    // TODO: Replace with your published Google Sheet CSV URL
    // Instructions: File > Share > Publish to web > Select "Comma-separated values (.csv)"
    SHEET_URL: 'YOUR_GOOGLE_SHEET_CSV_URL_HERE'
};

let allDogs = [];

// Load and display dogs
async function loadDogs() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const gridEl = document.getElementById('dogs-grid');

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

// Parse CSV data
function parseCSV(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const dogs = [];

    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;

        const values = lines[i].split(',');
        const dog = {};

        headers.forEach((header, index) => {
            dog[header] = values[index] ? values[index].trim() : '';
        });

        // Only show available dogs
        if (dog.Available === 'Yes') {
            dogs.push(dog);
        }
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
                ${dog.Size ? `<div class="dog-detail"><strong>Size:</strong> ${dog.Size}</div>` : ''}
                ${dog.Location ? `<div class="dog-detail"><strong>Location:</strong> ${dog.Location}</div>` : ''}
                ${dog.Description ? `<div class="dog-description">${dog.Description}</div>` : ''}
                ${dog.Rescue_Name ? `<span class="rescue-badge">${dog.Rescue_Name}</span>` : ''}
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
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const sizeFilter = document.getElementById('size-filter').value;
    const rescueFilter = document.getElementById('rescue-filter').value;

    const filtered = allDogs.filter(dog => {
        const matchesSearch = !searchTerm ||
            dog.Name.toLowerCase().includes(searchTerm) ||
            dog.Breed.toLowerCase().includes(searchTerm) ||
            dog.Description.toLowerCase().includes(searchTerm);

        const matchesSize = !sizeFilter || dog.Size === sizeFilter;
        const matchesRescue = !rescueFilter || dog.Rescue_Name === rescueFilter;

        return matchesSearch && matchesSize && matchesRescue;
    });

    displayDogs(filtered);
}

// Event listeners
document.getElementById('search').addEventListener('input', filterDogs);
document.getElementById('size-filter').addEventListener('change', filterDogs);
document.getElementById('rescue-filter').addEventListener('change', filterDogs);

// Load dogs on page load
loadDogs();
