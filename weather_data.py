"""
Weather Data Module
This module contains the WeatherData class that structures and holds weather details.
"""

from dataclasses import dataclass

@dataclass
class WeatherData:
    """Class to structure and hold weather details
    
    Attributes:
        city: Name of the city
        country: Country code
        temperature: Current temperature in Celsius
        feels_like: How temperature feels like in Celsius
        description: Weather description (Clear, Cloudy, Rainy, etc.)
        humidity: Humidity percentage
        pressure: Atmospheric pressure in hPa
        wind_speed: Wind speed in m/s
        icon: Weather icon code from OpenWeatherMap
        last_updated: Time when data was last updated
    """
    city: str
    country: str
    temperature: int
    feels_like: int
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    icon: str
    last_updated: str
    
    def __str__(self) -> str:
        """Return string representation of weather data"""
        return (
            f"Weather in {self.city}, {self.country}:\n"
            f"Temperature: {self.temperature}°C (feels like {self.feels_like}°C)\n"
            f"Description: {self.description}\n"
            f"Humidity: {self.humidity}%\n"
            f"Wind Speed: {self.wind_speed} m/s\n"
            f"Pressure: {self.pressure} hPa\n"
            f"Last Updated: {self.last_updated}"
        )
