"""
Weather App - Main Application
This module contains the WeatherApp class that manages the UI and interactions.
"""

import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import io
import requests
from typing import Optional, Dict, Any, Tuple

from weather_fetcher import WeatherFetcher
from weather_data import WeatherData
from assets.app_styles import (
    APP_TITLE, 
    COLOR_PRIMARY, 
    COLOR_SECONDARY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BACKGROUND,
    FONT_FAMILY,
    PADDING,
    CORNER_RADIUS
)

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Use system setting for light/dark mode
ctk.set_default_color_theme("blue")

class WeatherApp:
    """Main Weather Application class"""
    
    def __init__(self, api_key: str):
        """Initialize the Weather App
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self._api_key = api_key
        self._weather_fetcher = WeatherFetcher(api_key)
        self._setup_root()
        self._create_widgets()
        self._setup_layout()
        
        # Variable to store current weather data
        self._current_weather: Optional[WeatherData] = None
        self._weather_icon: Optional[ImageTk.PhotoImage] = None
        
        # Set up initial state
        self._show_welcome_screen()
    
    def _setup_root(self) -> None:
        """Set up the root window"""
        self.root = ctk.CTk()
        self.root.title(APP_TITLE)
        self.root.geometry("700x550")
        self.root.minsize(600, 500)
        
        # Make the window responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Search frame
        self.root.grid_rowconfigure(1, weight=1)  # Content frame
    
    def _create_widgets(self) -> None:
        """Create all UI widgets"""
        # Create search frame
        self.search_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Create search bar
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Enter city name...",
            textvariable=self.search_var,
            height=40,
            font=(FONT_FAMILY, 14)
        )
        self.search_entry.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="ew")
        
        # Create search button
        self.search_button = ctk.CTkButton(
            self.search_frame, 
            text="Search",
            command=self._handle_search,
            height=40,
            font=(FONT_FAMILY, 14, "bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_SECONDARY
        )
        self.search_button.grid(row=0, column=1, padx=PADDING, pady=PADDING)
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=COLOR_BACKGROUND
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Add binding for Enter key
        self.search_entry.bind("<Return>", lambda event: self._handle_search())
    
    def _setup_layout(self) -> None:
        """Set up the initial layout"""
        # Will be populated when searching for weather
        pass
    
    def _show_welcome_screen(self) -> None:
        """Display the welcome screen"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add welcome message
        welcome_frame = ctk.CTkFrame(
            self.content_frame, 
            fg_color="transparent"
        )
        welcome_frame.grid(row=0, column=0, sticky="", padx=PADDING, pady=PADDING)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Weather App",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        welcome_label.grid(row=0, column=0, pady=(0, 10))
        
        instruction_label = ctk.CTkLabel(
            welcome_frame,
            text="Enter a city name in the search box above to get started",
            font=(FONT_FAMILY, 16),
            text_color=COLOR_TEXT_SECONDARY
        )
        instruction_label.grid(row=1, column=0, pady=(0, 20))
    
    def _show_loading_screen(self) -> None:
        """Display loading screen while fetching data"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add loading message
        loading_frame = ctk.CTkFrame(
            self.content_frame, 
            fg_color="transparent"
        )
        loading_frame.grid(row=0, column=0, sticky="", padx=PADDING, pady=PADDING)
        
        loading_label = ctk.CTkLabel(
            loading_frame,
            text="Loading weather data...",
            font=(FONT_FAMILY, 18),
            text_color=COLOR_TEXT_PRIMARY
        )
        loading_label.grid(row=0, column=0, pady=10)
        
        # Force update to show loading screen
        self.root.update()
    
    def _handle_search(self) -> None:
        """Handle search button click"""
        city = self.search_var.get().strip()
        
        if not city:
            messagebox.showwarning("Empty Search", "Please enter a city name")
            return
        
        # Show loading screen
        self._show_loading_screen()
        
        # Create a thread to fetch weather data
        thread = threading.Thread(
            target=self._fetch_weather_data,
            args=(city,)
        )
        thread.daemon = True
        thread.start()
    
    def _fetch_weather_data(self, city: str) -> None:
        """Fetch weather data in a separate thread
        
        Args:
            city: City name to search for
        """
        try:
            weather_data = self._weather_fetcher.get_current_weather(city)
            self._current_weather = weather_data
            
            # Fetch weather icon
            icon_url = f"https://openweathermap.org/img/wn/{weather_data.icon}@2x.png"
            response = requests.get(icon_url)
            
            if response.status_code == 200:
                img_data = io.BytesIO(response.content)
                img = Image.open(img_data)
                self._weather_icon = ImageTk.PhotoImage(img)
            
            # Update UI in the main thread
            self.root.after(0, self._display_weather_data)
            
        except Exception as e:
            # Update UI in the main thread
            self.root.after(0, lambda: self._show_error(str(e)))
    
    def _show_error(self, message: str) -> None:
        """Display error message
        
        Args:
            message: Error message to display
        """
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add error message
        error_frame = ctk.CTkFrame(
            self.content_frame, 
            fg_color="transparent"
        )
        error_frame.grid(row=0, column=0, sticky="", padx=PADDING, pady=PADDING)
        
        error_label = ctk.CTkLabel(
            error_frame,
            text="Error",
            font=(FONT_FAMILY, 24, "bold"),
            text_color="#E53935"  # Red color for error
        )
        error_label.grid(row=0, column=0, pady=(0, 10))
        
        error_message = ctk.CTkLabel(
            error_frame,
            text=message,
            font=(FONT_FAMILY, 16),
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=400
        )
        error_message.grid(row=1, column=0, pady=(0, 20))
        
        # Add try again button
        try_again_button = ctk.CTkButton(
            error_frame,
            text="Try Again",
            command=self._show_welcome_screen,
            height=40,
            font=(FONT_FAMILY, 14),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_SECONDARY
        )
        try_again_button.grid(row=2, column=0, pady=10)
    
    def _display_weather_data(self) -> None:
        """Display weather data in the UI"""
        if not self._current_weather:
            return
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create weather card
        weather_card = ctk.CTkFrame(
            self.content_frame,
            corner_radius=CORNER_RADIUS,
            fg_color="#FFFFFF" if ctk.get_appearance_mode() == "Light" else "#2B2B2B"
        )
        weather_card.grid(row=0, column=0, padx=PADDING*2, pady=PADDING*2, sticky="")
        
        # Location info
        location_frame = ctk.CTkFrame(
            weather_card,
            fg_color="transparent"
        )
        location_frame.grid(row=0, column=0, columnspan=2, padx=PADDING*2, pady=(PADDING*2, PADDING), sticky="ew")
        
        city_label = ctk.CTkLabel(
            location_frame,
            text=f"{self._current_weather.city}, {self._current_weather.country}",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        city_label.grid(row=0, column=0, sticky="w")
        
        # Temperature and icon
        temp_frame = ctk.CTkFrame(
            weather_card,
            fg_color="transparent"
        )
        temp_frame.grid(row=1, column=0, padx=PADDING*2, pady=PADDING, sticky="w")
        
        temp_label = ctk.CTkLabel(
            temp_frame,
            text=f"{self._current_weather.temperature}°C",
            font=(FONT_FAMILY, 40, "bold"),
            text_color=COLOR_PRIMARY
        )
        temp_label.grid(row=0, column=0, sticky="w")
        
        # Weather icon and description
        icon_frame = ctk.CTkFrame(
            weather_card,
            fg_color="transparent"
        )
        icon_frame.grid(row=1, column=1, padx=PADDING*2, pady=PADDING, sticky="e")
        
        if self._weather_icon:
            icon_label = tk.Label(
                icon_frame,
                image=self._weather_icon,
                bg=weather_card.cget("fg_color")
            )
            icon_label.grid(row=0, column=0)
        
        description_label = ctk.CTkLabel(
            icon_frame,
            text=self._current_weather.description.capitalize(),
            font=(FONT_FAMILY, 18),
            text_color=COLOR_TEXT_SECONDARY
        )
        description_label.grid(row=1, column=0)
        
        # Details frame
        details_frame = ctk.CTkFrame(
            weather_card,
            fg_color="transparent"
        )
        details_frame.grid(row=2, column=0, columnspan=2, padx=PADDING*2, pady=PADDING*2, sticky="ew")
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)
        
        # Feels like temperature
        feels_like_label = ctk.CTkLabel(
            details_frame,
            text="Feels like:",
            font=(FONT_FAMILY, 14),
            text_color=COLOR_TEXT_SECONDARY
        )
        feels_like_label.grid(row=0, column=0, pady=(PADDING, 0), sticky="w")
        
        feels_like_value = ctk.CTkLabel(
            details_frame,
            text=f"{self._current_weather.feels_like}°C",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        feels_like_value.grid(row=0, column=1, pady=(PADDING, 0), sticky="e")
        
        # Humidity
        humidity_label = ctk.CTkLabel(
            details_frame,
            text="Humidity:",
            font=(FONT_FAMILY, 14),
            text_color=COLOR_TEXT_SECONDARY
        )
        humidity_label.grid(row=1, column=0, pady=PADDING, sticky="w")
        
        humidity_value = ctk.CTkLabel(
            details_frame,
            text=f"{self._current_weather.humidity}%",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        humidity_value.grid(row=1, column=1, pady=PADDING, sticky="e")
        
        # Wind speed
        wind_label = ctk.CTkLabel(
            details_frame,
            text="Wind speed:",
            font=(FONT_FAMILY, 14),
            text_color=COLOR_TEXT_SECONDARY
        )
        wind_label.grid(row=2, column=0, pady=PADDING, sticky="w")
        
        wind_value = ctk.CTkLabel(
            details_frame,
            text=f"{self._current_weather.wind_speed} m/s",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        wind_value.grid(row=2, column=1, pady=PADDING, sticky="e")
        
        # Pressure
        pressure_label = ctk.CTkLabel(
            details_frame,
            text="Pressure:",
            font=(FONT_FAMILY, 14),
            text_color=COLOR_TEXT_SECONDARY
        )
        pressure_label.grid(row=3, column=0, pady=PADDING, sticky="w")
        
        pressure_value = ctk.CTkLabel(
            details_frame,
            text=f"{self._current_weather.pressure} hPa",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        pressure_value.grid(row=3, column=1, pady=PADDING, sticky="e")
        
        # Last updated
        updated_frame = ctk.CTkFrame(
            weather_card,
            fg_color="transparent"
        )
        updated_frame.grid(row=3, column=0, columnspan=2, padx=PADDING*2, pady=PADDING, sticky="ew")
        
        updated_label = ctk.CTkLabel(
            updated_frame,
            text=f"Last updated: {self._current_weather.last_updated}",
            font=(FONT_FAMILY, 12),
            text_color=COLOR_TEXT_SECONDARY
        )
        updated_label.grid(row=0, column=0)
    
    def run(self) -> None:
        """Run the application"""
        self.root.mainloop()
