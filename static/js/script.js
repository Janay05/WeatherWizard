// DOM Elements
const weatherForm = document.getElementById('weather-form');
const cityInput = document.getElementById('city-input');
const welcomeScreen = document.getElementById('welcome-screen');
const loadingScreen = document.getElementById('loading-screen');
const errorScreen = document.getElementById('error-screen');
const weatherCard = document.getElementById('weather-card');
const errorMessage = document.getElementById('error-message');
const tryAgainButton = document.getElementById('try-again-button');

// Weather data elements
const locationElement = document.getElementById('location');
const temperatureElement = document.getElementById('temperature');
const weatherIconImg = document.getElementById('weather-icon-img');
const weatherDescription = document.getElementById('weather-description');
const feelsLikeElement = document.getElementById('feels-like');
const humidityElement = document.getElementById('humidity');
const windSpeedElement = document.getElementById('wind-speed');
const pressureElement = document.getElementById('pressure');
const lastUpdatedElement = document.getElementById('last-updated');

// Event Listeners
weatherForm.addEventListener('submit', handleSearch);
tryAgainButton.addEventListener('click', showWelcomeScreen);

/**
 * Handle search form submission
 * @param {Event} event - The form submit event
 */
function handleSearch(event) {
    event.preventDefault();
    
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    showLoadingScreen();
    fetchWeatherData(city);
}

/**
 * Fetch weather data from the API
 * @param {string} city - The city name to search for
 */
function fetchWeatherData(city) {
    const formData = new FormData();
    formData.append('city', city);
    
    fetch('/weather', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayWeatherData(data);
        } else {
            showError(data.error || 'An unknown error occurred');
        }
    })
    .catch(error => {
        showError('Failed to fetch weather data: ' + error.message);
    });
}

/**
 * Display weather data in the UI
 * @param {Object} data - Weather data from the API
 */
function displayWeatherData(data) {
    // Clear any previous weather effects
    clearWeatherEffects();
    
    // Set location
    locationElement.textContent = `${data.city}, ${data.country}`;
    
    // Set temperature
    temperatureElement.textContent = `${data.temperature}`;
    
    // Set weather icon
    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    weatherIconImg.src = iconUrl;
    weatherIconImg.alt = data.description;
    
    // Set weather description
    weatherDescription.textContent = data.description;
    
    // Set details
    feelsLikeElement.textContent = `${data.feels_like}°C`;
    humidityElement.textContent = `${data.humidity}%`;
    windSpeedElement.textContent = `${data.wind_speed} m/s`;
    pressureElement.textContent = `${data.pressure} hPa`;
    
    // Set last updated
    lastUpdatedElement.textContent = `Last updated: ${data.last_updated}`;
    
    // Add fade-in animation
    weatherCard.classList.add('animate__animated', 'animate__fadeIn');
    
    // Show weather card
    hideAllScreens();
    weatherCard.style.display = 'block';
    
    // Set a dynamic background and styling based on temperature and weather
    setBackgroundColorByTemperature(data.temperature, data.description);
}

/**
 * Clear any previously added weather effects
 */
function clearWeatherEffects() {
    // Remove effects containers if they exist
    const effectContainers = document.querySelectorAll('.rain-container, .snow-container, .fog-container, .stars-container');
    effectContainers.forEach(container => container.remove());
    
    // Reset body color
    document.body.style.color = '';
}

/**
 * Sets styles based on temperature and weather conditions
 * @param {number} temp - Temperature in Celsius
 * @param {string} description - Weather description
 */
function setBackgroundColorByTemperature(temp, description = '') {
    // Set background gradient for main page based on time of day
    const hour = new Date().getHours();
    const bgWrapper = document.querySelector('.weather-bg-wrapper');
    
    // Time-based background
    if (hour >= 5 && hour < 8) {
        // Dawn
        bgWrapper.style.background = 'linear-gradient(135deg, #ffcf77 0%, #f68084 100%)';
    } else if (hour >= 8 && hour < 17) {
        // Day
        bgWrapper.style.background = 'var(--gradient-day)';
    } else if (hour >= 17 && hour < 20) {
        // Sunset
        bgWrapper.style.background = 'var(--gradient-sunset)';
    } else {
        // Night
        bgWrapper.style.background = 'var(--gradient-night)';
        document.body.style.color = '#f8f9fa';
    }
    
    // Weather condition-based adjustments
    const lowerDesc = description.toLowerCase();
    if (lowerDesc.includes('rain') || lowerDesc.includes('drizzle') || lowerDesc.includes('shower')) {
        bgWrapper.style.background = 'linear-gradient(to bottom, #929ead 0%, #5a6a81 100%)';
        addRainEffect();
    } else if (lowerDesc.includes('snow')) {
        bgWrapper.style.background = 'linear-gradient(to bottom, #e0eafc 0%, #cfdef3 100%)';
        addSnowEffect();
    } else if (lowerDesc.includes('thunder') || lowerDesc.includes('storm')) {
        bgWrapper.style.background = 'linear-gradient(to bottom, #292E49 0%, #536976 100%)';
        document.body.style.color = '#f8f9fa';
    } else if (lowerDesc.includes('fog') || lowerDesc.includes('mist') || lowerDesc.includes('haze')) {
        bgWrapper.style.background = 'linear-gradient(to bottom, #d9dee5 0%, #b3becf 100%)';
        addFogEffect();
    } else if (lowerDesc.includes('clear') && (hour < 5 || hour >= 20)) {
        // Clear night
        bgWrapper.style.background = 'linear-gradient(to bottom, #0f2027 0%, #203a43 50%, #2c5364 100%)';
        document.body.style.color = '#f8f9fa';
        addStarsEffect();
    }
    
    // Temperature-based styling for the weather card
    let mainCardStyle, detailsCardStyle;
    
    if (temp <= 0) {
        // Cold
        mainCardStyle = {
            background: 'linear-gradient(120deg, rgba(224, 242, 255, 0.9), rgba(191, 228, 255, 0.9))',
            boxShadow: '0 10px 25px rgba(11, 70, 168, 0.15)'
        };
        detailsCardStyle = {
            background: 'linear-gradient(120deg, rgba(224, 242, 255, 0.8), rgba(191, 228, 255, 0.8))'
        };
        document.documentElement.style.setProperty('--primary-color', '#2c7be5');
    } else if (temp <= 10) {
        // Cool
        mainCardStyle = {
            background: 'linear-gradient(120deg, rgba(228, 243, 255, 0.9), rgba(202, 234, 255, 0.9))',
            boxShadow: '0 10px 25px rgba(27, 107, 212, 0.12)'
        };
        detailsCardStyle = {
            background: 'linear-gradient(120deg, rgba(228, 243, 255, 0.8), rgba(202, 234, 255, 0.8))'
        };
        document.documentElement.style.setProperty('--primary-color', '#3a86ff');
    } else if (temp <= 20) {
        // Mild
        mainCardStyle = {
            background: 'linear-gradient(120deg, rgba(230, 255, 230, 0.9), rgba(210, 245, 210, 0.9))',
            boxShadow: '0 10px 25px rgba(34, 139, 34, 0.12)'
        };
        detailsCardStyle = {
            background: 'linear-gradient(120deg, rgba(230, 255, 230, 0.8), rgba(210, 245, 210, 0.8))'
        };
        document.documentElement.style.setProperty('--primary-color', '#38b000');
    } else if (temp <= 30) {
        // Warm
        mainCardStyle = {
            background: 'linear-gradient(120deg, rgba(255, 245, 220, 0.9), rgba(252, 235, 190, 0.9))',
            boxShadow: '0 10px 25px rgba(223, 136, 31, 0.12)'
        };
        detailsCardStyle = {
            background: 'linear-gradient(120deg, rgba(255, 245, 220, 0.8), rgba(252, 235, 190, 0.8))'
        };
        document.documentElement.style.setProperty('--primary-color', '#ff9900');
    } else {
        // Hot
        mainCardStyle = {
            background: 'linear-gradient(120deg, rgba(255, 230, 220, 0.9), rgba(252, 210, 200, 0.9))',
            boxShadow: '0 10px 25px rgba(223, 71, 31, 0.15)'
        };
        detailsCardStyle = {
            background: 'linear-gradient(120deg, rgba(255, 230, 220, 0.8), rgba(252, 210, 200, 0.8))'
        };
        document.documentElement.style.setProperty('--primary-color', '#ff5a5f');
    }
    
    // Apply styles to cards
    const mainWeatherCard = document.querySelector('.main-weather-card');
    const weatherDetailsCard = document.querySelector('.weather-details-card');
    
    Object.assign(mainWeatherCard.style, mainCardStyle);
    Object.assign(weatherDetailsCard.style, detailsCardStyle);
}

/**
 * Add rain effect to the background
 */
function addRainEffect() {
    const rainContainer = document.createElement('div');
    rainContainer.className = 'rain-container';
    rainContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    document.body.appendChild(rainContainer);
    
    for (let i = 0; i < 40; i++) {
        createRainDrop(rainContainer);
    }
}

/**
 * Create a raindrop element
 * @param {HTMLElement} container - Container for raindrops
 */
function createRainDrop(container) {
    const drop = document.createElement('div');
    const left = Math.random() * 100;
    const size = Math.random() * 1.5 + 0.5;
    const duration = Math.random() * 1 + 0.5;
    const delay = Math.random() * 5;
    
    drop.style.cssText = `
        position: absolute;
        left: ${left}%;
        top: -20px;
        width: 2px;
        height: ${8 * size}px;
        background-color: rgba(174, 194, 224, 0.6);
        border-radius: 5px;
        animation: rain ${duration}s linear ${delay}s infinite;
    `;
    
    if (!document.querySelector('style#rain-style')) {
        const style = document.createElement('style');
        style.id = 'rain-style';
        style.textContent = `
            @keyframes rain {
                0% { transform: translateY(-20px); opacity: 0; }
                50% { opacity: 1; }
                100% { transform: translateY(100vh); opacity: 0.3; }
            }
        `;
        document.head.appendChild(style);
    }
    
    container.appendChild(drop);
}

/**
 * Add snow effect to the background
 */
function addSnowEffect() {
    const snowContainer = document.createElement('div');
    snowContainer.className = 'snow-container';
    snowContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    document.body.appendChild(snowContainer);
    
    for (let i = 0; i < 50; i++) {
        createSnowflake(snowContainer);
    }
}

/**
 * Create a snowflake element
 * @param {HTMLElement} container - Container for snowflakes
 */
function createSnowflake(container) {
    const flake = document.createElement('div');
    const left = Math.random() * 100;
    const size = Math.random() * 3 + 1;
    const duration = Math.random() * 5 + 3;
    const delay = Math.random() * 5;
    
    flake.style.cssText = `
        position: absolute;
        left: ${left}%;
        top: -10px;
        width: ${size}px;
        height: ${size}px;
        background-color: white;
        border-radius: 50%;
        opacity: 0.8;
        animation: snow ${duration}s linear ${delay}s infinite;
    `;
    
    if (!document.querySelector('style#snow-style')) {
        const style = document.createElement('style');
        style.id = 'snow-style';
        style.textContent = `
            @keyframes snow {
                0% { transform: translateY(-10px) rotate(0deg); opacity: 0; }
                50% { opacity: 1; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0.3; }
            }
        `;
        document.head.appendChild(style);
    }
    
    container.appendChild(flake);
}

/**
 * Add fog effect to the background
 */
function addFogEffect() {
    const fogContainer = document.createElement('div');
    fogContainer.className = 'fog-container';
    fogContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
        background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxmaWx0ZXIgaWQ9ImZvZyIgeD0iMCIgeT0iMCI+CiAgICA8ZmVUdXJidWxlbmNlIHR5cGU9ImZyYWN0YWxOb2lzZSIgYmFzZUZyZXF1ZW5jeT0iMC4wMSIgbnVtT2N0YXZlcz0iMyIgc3RpdGNoVGlsZXM9InN0aXRjaCIvPgogICAgPGZlQ29sb3JNYXRyaXggdHlwZT0ic2F0dXJhdGUiIHZhbHVlcz0iMCIvPgogICAgPGZlQ29tcG9zaXRlIG9wZXJhdG9yPSJhcml0aG1ldGljIiBrMT0iMCIgazI9IjAuMSIgazM9IjAuOSIgazQ9IjAuMSIvPgogIDwvZmlsdGVyPgogIDxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IndoaXRlIiBmaWx0ZXI9InVybCgjZm9nKSIgb3BhY2l0eT0iMC40Ii8+Cjwvc3ZnPg==');
        opacity: 0.8;
    `;
    document.body.appendChild(fogContainer);
}

/**
 * Add stars effect to the background (clear night)
 */
function addStarsEffect() {
    const starsContainer = document.createElement('div');
    starsContainer.className = 'stars-container';
    starsContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    document.body.appendChild(starsContainer);
    
    for (let i = 0; i < 100; i++) {
        createStar(starsContainer);
    }
}

/**
 * Create a star element
 * @param {HTMLElement} container - Container for stars
 */
function createStar(container) {
    const star = document.createElement('div');
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    const size = Math.random() * 2 + 1;
    const duration = Math.random() * 3 + 2;
    
    star.style.cssText = `
        position: absolute;
        left: ${left}%;
        top: ${top}%;
        width: ${size}px;
        height: ${size}px;
        background-color: white;
        border-radius: 50%;
        opacity: ${Math.random() * 0.5 + 0.5};
        animation: twinkle ${duration}s ease-in-out infinite;
    `;
    
    if (!document.querySelector('style#star-style')) {
        const style = document.createElement('style');
        style.id = 'star-style';
        style.textContent = `
            @keyframes twinkle {
                0%, 100% { opacity: 0.2; transform: scale(0.8); }
                50% { opacity: 1; transform: scale(1.2); }
            }
        `;
        document.head.appendChild(style);
    }
    
    container.appendChild(star);
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessage.textContent = message;
    hideAllScreens();
    errorScreen.style.display = 'block';
}

/**
 * Show welcome screen
 */
function showWelcomeScreen() {
    hideAllScreens();
    welcomeScreen.style.display = 'block';
}

/**
 * Show loading screen
 */
function showLoadingScreen() {
    hideAllScreens();
    loadingScreen.style.display = 'block';
}

/**
 * Hide all screens
 */
function hideAllScreens() {
    welcomeScreen.style.display = 'none';
    loadingScreen.style.display = 'none';
    errorScreen.style.display = 'none';
    weatherCard.style.display = 'none';
}

/**
 * Add a listener to enable search button only when input is not empty
 */
cityInput.addEventListener('input', function() {
    const searchButton = document.getElementById('search-button');
    if (this.value.trim() === '') {
        searchButton.disabled = true;
        searchButton.classList.add('btn-secondary');
        searchButton.classList.remove('btn-primary');
    } else {
        searchButton.disabled = false;
        searchButton.classList.add('btn-primary');
        searchButton.classList.remove('btn-secondary');
    }
});

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    showWelcomeScreen();
    
    // Initially disable search button if input is empty
    const searchButton = document.getElementById('search-button');
    if (cityInput.value.trim() === '') {
        searchButton.disabled = true;
        searchButton.classList.add('btn-secondary');
        searchButton.classList.remove('btn-primary');
    }
});