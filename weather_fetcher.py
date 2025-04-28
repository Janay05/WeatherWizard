"""
Weather Fetcher Module
This module contains the WeatherFetcher class that handles API calls to fetch weather data.
"""

import requests
import datetime
from typing import Dict, Any

from weather_data import WeatherData

class WeatherFetcher:
    """Class to handle API calls to fetch weather data"""
    
    def __init__(self, api_key: str):
        """Initialize the WeatherFetcher
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self._api_key = api_key
        self._base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str) -> WeatherData:
        """Get current weather data for a city
        
        Args:
            city: City name to search for
            
        Returns:
            WeatherData object containing weather information
            
        Raises:
            Exception: If city not found or API error occurs
        """
        if not self._api_key:
            raise Exception("API key is not set. Please set the OPENWEATHERMAP_API_KEY environment variable.")
        
        try:
            # Make API request
            url = f"{self._base_url}/weather"
            params = {
                "q": city,
                "appid": self._api_key,
                "units": "metric"  # Use metric units (Celsius)
            }
            
            response = requests.get(url, params=params)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data)
            elif response.status_code == 404:
                raise Exception(f"City '{city}' not found. Please check the spelling and try again.")
            else:
                raise Exception(f"API Error: {response.status_code} - {response.reason}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching weather data: {str(e)}")
    
    def _parse_weather_data(self, data: Dict[str, Any]) -> WeatherData:
        """Parse API response and create a WeatherData object
        
        Args:
            data: JSON data from API response
            
        Returns:
            WeatherData object containing weather information
        """
        # Extract needed data from response
        city = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "Unknown")
        temperature = round(data.get("main", {}).get("temp", 0))
        feels_like = round(data.get("main", {}).get("feels_like", 0))
        humidity = data.get("main", {}).get("humidity", 0)
        pressure = data.get("main", {}).get("pressure", 0)
        
        # Weather description and icon
        weather = data.get("weather", [{}])[0]
        description = weather.get("description", "Unknown")
        icon = weather.get("icon", "01d")
        
        # Wind speed
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Get current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Create and return WeatherData object
        return WeatherData(
            city=city,
            country=country,
            temperature=temperature,
            feels_like=feels_like,
            description=description,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            icon=icon,
            last_updated=current_time
        )
