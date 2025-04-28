"""
Weather App - Web Version
A Python-based Weather App with a Flask web interface that displays real-time weather information.
"""

import os
from flask import Flask, render_template, request, jsonify
from weather_fetcher import WeatherFetcher

app = Flask(__name__)

# Get API key from environment variable
api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")

# Initialize WeatherFetcher
weather_fetcher = WeatherFetcher(api_key)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    """API endpoint to get weather data"""
    city = request.form.get('city', '').strip()
    
    if not city:
        return jsonify({
            'success': False,
            'error': 'Please enter a city name'
        })
    
    try:
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
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)