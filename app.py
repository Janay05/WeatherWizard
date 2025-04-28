"""
Weather App - Web Version
A Python-based Weather App with a Flask web interface that displays real-time weather information
with beautiful UI, animations, and dynamic styling based on weather conditions.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from weather_fetcher import WeatherFetcher

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get API key from environment variable
api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
if not api_key:
    logger.warning("No OpenWeatherMap API key found! Please set the OPENWEATHERMAP_API_KEY environment variable.")

# Initialize WeatherFetcher
weather_fetcher = WeatherFetcher(api_key)

@app.route('/')
def index():
    """Render the main page"""
    if not api_key:
        logger.warning("Serving app without API key - searches will fail")
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    """API endpoint to get weather data"""
    if not api_key:
        return jsonify({
            'success': False,
            'error': 'OpenWeatherMap API key is not configured. Please set the OPENWEATHERMAP_API_KEY environment variable.'
        })
        
    city = request.form.get('city', '').strip()
    
    if not city:
        return jsonify({
            'success': False,
            'error': 'Please enter a city name'
        })
    
    try:
        logger.info(f"Fetching weather data for city: {city}")
        
        # Get weather data
        weather_data = weather_fetcher.get_current_weather(city)
        
        # Convert to dictionary for JSON response
        result = {
            'success': True,
            'city': weather_data.city,
            'country': weather_data.country,
            'temperature': weather_data.temperature,
            'feels_like': weather_data.feels_like,
            'description': weather_data.description.capitalize(),
            'humidity': weather_data.humidity,
            'pressure': weather_data.pressure,
            'wind_speed': weather_data.wind_speed,
            'icon': weather_data.icon,
            'last_updated': weather_data.last_updated
        }
        
        logger.info(f"Successfully retrieved weather data for {city}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Could not retrieve weather data: {str(e)}"
        })

if __name__ == '__main__':
    logger.info("Starting Weather App server...")
    logger.info(f"API Key configured: {'Yes' if api_key else 'No'}")
    app.run(host='0.0.0.0', port=5000, debug=True)