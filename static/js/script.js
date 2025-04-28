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
    // Set location
    locationElement.textContent = `${data.city}, ${data.country}`;
    
    // Set temperature
    temperatureElement.textContent = `${data.temperature}°C`;
    
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
    
    // Set a dynamic background color based on temperature
    setBackgroundColorByTemperature(data.temperature);
}

/**
 * Sets a background color for weather card based on temperature
 * @param {number} temp - Temperature in Celsius
 */
function setBackgroundColorByTemperature(temp) {
    let bgColor;
    
    if (temp <= 0) {
        // Cold - blue
        bgColor = 'rgba(200, 232, 255, 0.7)';
    } else if (temp <= 10) {
        // Cool - light blue
        bgColor = 'rgba(220, 240, 255, 0.7)';
    } else if (temp <= 20) {
        // Mild - light green
        bgColor = 'rgba(230, 255, 230, 0.7)';
    } else if (temp <= 30) {
        // Warm - light orange
        bgColor = 'rgba(255, 240, 220, 0.7)';
    } else {
        // Hot - light red
        bgColor = 'rgba(255, 225, 220, 0.7)';
    }
    
    document.querySelector('.main-weather-card').style.backgroundColor = bgColor;
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