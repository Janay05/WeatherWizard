"""
App Styles Module
This module contains styling constants for the Weather App.
"""

# App title
APP_TITLE = "Weather App"

# Colors
COLOR_PRIMARY = "#1e88e5"  # Blue
COLOR_SECONDARY = "#0d47a1"  # Darker blue
COLOR_TEXT_PRIMARY = "#212121"  # Dark grey for primary text
COLOR_TEXT_SECONDARY = "#757575"  # Medium grey for secondary text
COLOR_BACKGROUND = "#f5f5f5"  # Light grey for background

# Font settings
FONT_FAMILY = "Helvetica"

# Spacing and sizing
PADDING = 10
CORNER_RADIUS = 15

# Weather condition mappings for potential enhancements
WEATHER_CONDITION_MAPPING = {
    "01d": "Clear sky (day)",
    "01n": "Clear sky (night)",
    "02d": "Few clouds (day)",
    "02n": "Few clouds (night)",
    "03d": "Scattered clouds",
    "03n": "Scattered clouds",
    "04d": "Broken clouds",
    "04n": "Broken clouds",
    "09d": "Shower rain",
    "09n": "Shower rain",
    "10d": "Rain (day)",
    "10n": "Rain (night)",
    "11d": "Thunderstorm",
    "11n": "Thunderstorm",
    "13d": "Snow",
    "13n": "Snow",
    "50d": "Mist",
    "50n": "Mist"
}

# Color mappings for different weather conditions for potential theme changes
WEATHER_COLOR_MAPPING = {
    "01d": "#FFB300",  # Sunny - amber
    "01n": "#1A237E",  # Clear night - indigo
    "02d": "#90CAF9",  # Few clouds day - light blue
    "02n": "#303F9F",  # Few clouds night - indigo
    "03d": "#BBDEFB",  # Scattered clouds - blue
    "03n": "#455A64",  # Scattered clouds night - blue grey
    "04d": "#78909C",  # Broken clouds - blue grey
    "04n": "#37474F",  # Broken clouds night - blue grey
    "09d": "#4FC3F7",  # Shower rain - light blue
    "09n": "#0277BD",  # Shower rain night - blue
    "10d": "#039BE5",  # Rain - blue
    "10n": "#01579B",  # Rain night - blue
    "11d": "#5E35B1",  # Thunderstorm - deep purple
    "11n": "#4527A0",  # Thunderstorm night - deep purple
    "13d": "#E1F5FE",  # Snow - light blue
    "13n": "#B3E5FC",  # Snow night - light blue
    "50d": "#CFD8DC",  # Mist - blue grey
    "50n": "#B0BEC5"   # Mist night - blue grey
}
