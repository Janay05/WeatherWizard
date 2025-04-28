#!/usr/bin/env python3
"""
Weather App - Entry Point
A Python-based Weather App with beautiful customTkinter UI and proper OOP architecture
that displays real-time weather information.
"""

import os
import sys
from weather_app import WeatherApp

if __name__ == "__main__":
    # Get API key from environment variable
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
    
    if not api_key:
        print("Warning: OPENWEATHERMAP_API_KEY is not set.")
        print("Please set the environment variable or the app will not function correctly.")
        print("You can get a free API key from https://openweathermap.org/api")
    
    # Start the Weather App
    app = WeatherApp(api_key)
    app.run()
