# 🌦️ Weather Wizard

**Weather Wizard** is a Flask-based web application that allows users to fetch current weather information for any city using an open-source weather API. The app uses Object-Oriented Programming (OOP) principles and is deployed on [Render](https://render.com).


## 🚀 Features

* Get real-time weather data by city name
* Clean and intuitive web interface
* Uses OOP structure for better maintainability
* Deployed and hosted using Render


## 🛠️ Technologies Used

* Python (Flask)
* HTML, CSS
* Weather API (e.g., OpenWeatherMap or similar)
* Render (for deployment)


## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Janay05/WeatherWizard.git
   cd weather-wizard
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:

   * Create a `.env` file and add:

     ```
     WEATHER_API_KEY=your_api_key_here
     ```

4. Run the app:

   ```bash
   flask run
   ```

---

## 📁 Project Structure

```
weather-wizard/
│
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── weather.py        # OOP class to handle weather logic
├── .env
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

* `weather.py`: Contains the `WeatherApp` class that fetches data from the API.
* `app.py`: Main Flask app that handles routes and renders the UI.
* HTML/CSS files for the frontend interface.

---

## 🌍 Live Demo

Check it out live: [https://weatherwizard-856d.onrender.com])

---

## 📜 License

MIT License

---

