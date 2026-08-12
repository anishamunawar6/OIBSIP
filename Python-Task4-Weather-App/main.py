import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
from collections import defaultdict
import os
from dotenv import load_dotenv


# =========================
# API SETTINGS
# =========================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"


# =========================
# GLOBAL SETTINGS
# =========================

unit = "metric"
current_data = None
forecast_data = None


# =========================
# WEATHER FUNCTIONS
# =========================

def get_weather():

    global current_data, forecast_data

    city = city_entry.get().strip()

    # Empty input validation
    if not city:
        show_error("Please enter a city name.")
        return

    # API key validation
    if not API_KEY:
        show_error("API key not found. Check your .env file.")
        return

    status_label.config(
        text="Fetching weather...",
        fg="#6C4AB6"
    )

    root.update_idletasks()

    try:

        params = {
            "q": city,
            "appid": API_KEY,
            "units": unit
        }

        # Current weather
        response = requests.get(
            CURRENT_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            show_error(
                "City not found. Please check the city name."
            )
            return

        if response.status_code == 401:
            show_error(
                "Invalid API key. Please check your API key."
            )
            return

        response.raise_for_status()

        current_data = response.json()

        # Forecast
        forecast_response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        if forecast_response.status_code == 401:
            show_error("Invalid API key.")
            return

        forecast_response.raise_for_status()

        forecast_data = forecast_response.json()

        # Display data
        display_current_weather()
        display_hourly_forecast()
        display_daily_forecast()

        status_label.config(
            text="Weather updated successfully.",
            fg="#6C4AB6"
        )

    except requests.exceptions.Timeout:

        show_error(
            "Request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        show_error(
            "Network error. Please check your internet connection."
        )

    except requests.exceptions.RequestException:

        show_error(
            "Unable to fetch weather data."
        )

    except Exception:

        show_error(
            "Something went wrong."
        )


# =========================
# CURRENT WEATHER
# =========================

def display_current_weather():

    city = current_data["name"]
    country = current_data["sys"]["country"]

    temperature = current_data["main"]["temp"]
    feels_like = current_data["main"]["feels_like"]
    humidity = current_data["main"]["humidity"]
    wind_speed = current_data["wind"]["speed"]

    condition = current_data["weather"][0]["description"]
    icon_code = current_data["weather"][0]["icon"]

    unit_symbol = "°C" if unit == "metric" else "°F"

    city_label.config(
        text=f"{city}, {country}"
    )

    temperature_label.config(
        text=f"{temperature:.1f}{unit_symbol}"
    )

    condition_label.config(
        text=condition.title()
    )

    details_label.config(
        text=(
            f"Feels like: {feels_like:.1f}{unit_symbol}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
    )

    load_weather_icon(icon_code)


# =========================
# WEATHER ICON
# =========================

def load_weather_icon(icon_code):

    try:

        url = ICON_URL.format(icon_code)

        response = requests.get(
            url,
            timeout=10
        )

        image = Image.open(
            BytesIO(response.content)
        )

        # Smaller icon to save space
        image = image.resize(
            (65, 65)
        )

        weather_icon = ImageTk.PhotoImage(
            image
        )

        icon_label.config(
            image=weather_icon
        )

        icon_label.image = weather_icon

    except Exception:

        icon_label.config(
            image=""
        )


# =========================
# HOURLY FORECAST
# =========================

def display_hourly_forecast():

    # Clear old cards
    for widget in hourly_frame.winfo_children():
        widget.destroy()

    if not forecast_data:
        return

    # First 6 forecast entries
    forecasts = forecast_data["list"][:6]

    for item in forecasts:

        time = datetime.fromtimestamp(
            item["dt"]
        ).strftime("%I %p")

        temperature = item["main"]["temp"]

        condition = item["weather"][0]["main"]

        unit_symbol = (
            "°C"
            if unit == "metric"
            else "°F"
        )

        card = tk.Frame(
            hourly_frame,
            bg="#F5F1FF",
            padx=8,
            pady=6
        )

        card.pack(
            side="left",
            padx=3
        )

        tk.Label(
            card,
            text=time,
            font=("Segoe UI", 8, "bold"),
            bg="#F5F1FF",
            fg="#333333"
        ).pack()

        tk.Label(
            card,
            text=f"{temperature:.0f}{unit_symbol}",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F1FF",
            fg="#6C4AB6"
        ).pack()

        tk.Label(
            card,
            text=condition,
            font=("Segoe UI", 7),
            bg="#F5F1FF",
            fg="#555555"
        ).pack()


# =========================
# DAILY FORECAST
# =========================

def display_daily_forecast():

    # Clear old cards
    for widget in daily_frame.winfo_children():
        widget.destroy()

    if not forecast_data:
        return

    daily_data = defaultdict(list)

    # Group forecast by date
    for item in forecast_data["list"]:

        date = datetime.fromtimestamp(
            item["dt"]
        ).strftime("%Y-%m-%d")

        daily_data[date].append(item)

    # Maximum 5 days
    days = list(daily_data.items())[:5]

    for date, items in days:

        # Average temperature
        average_temp = sum(
            item["main"]["temp"]
            for item in items
        ) / len(items)

        weather = items[0]["weather"][0]

        condition = weather["main"]

        day_name = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%a")

        unit_symbol = (
            "°C"
            if unit == "metric"
            else "°F"
        )

        card = tk.Frame(
            daily_frame,
            bg="#F5F1FF",
            padx=12,
            pady=7
        )

        card.pack(
            side="left",
            padx=3
        )

        tk.Label(
            card,
            text=day_name,
            font=("Segoe UI", 9, "bold"),
            bg="#F5F1FF",
            fg="#333333"
        ).pack()

        tk.Label(
            card,
            text=f"{average_temp:.0f}{unit_symbol}",
            font=("Segoe UI", 11, "bold"),
            bg="#F5F1FF",
            fg="#6C4AB6"
        ).pack()

        tk.Label(
            card,
            text=condition,
            font=("Segoe UI", 7),
            bg="#F5F1FF",
            fg="#555555"
        ).pack()


# =========================
# UNIT TOGGLE
# =========================

def toggle_unit():

    global unit

    if unit == "metric":

        unit = "imperial"

        unit_button.config(
            text="Switch to °C"
        )

    else:

        unit = "metric"

        unit_button.config(
            text="Switch to °F"
        )

    if city_entry.get().strip():
        get_weather()


# =========================
# ERROR MESSAGE
# =========================

def show_error(message):

    status_label.config(
        text=message,
        fg="#C0392B"
    )

    root.after(
        4000,
        lambda: status_label.config(
            fg="#6C4AB6"
        )
    )


# =========================
# GUI
# =========================

root = tk.Tk()

root.title("Weather App")

# Compact window
root.geometry("850x700")

root.configure(
    bg="#ECE8FF"
)

root.resizable(
    False,
    False
)


# =========================
# TITLE
# =========================

tk.Label(
    root,
    text="🌤 Weather App",
    font=("Segoe UI", 24, "bold"),
    bg="#ECE8FF",
    fg="#6C4AB6"
).pack(
    pady=(12, 2)
)

tk.Label(
    root,
    text="Check real-time weather and forecasts",
    font=("Segoe UI", 9),
    bg="#ECE8FF",
    fg="#555555"
).pack(
    pady=(0, 8)
)


# =========================
# SEARCH AREA
# =========================

search_frame = tk.Frame(
    root,
    bg="#ECE8FF"
)

search_frame.pack(
    pady=3
)


city_entry = tk.Entry(
    search_frame,
    width=27,
    font=("Segoe UI", 11),
    bd=0,
    relief="flat"
)

city_entry.grid(
    row=0,
    column=0,
    padx=4,
    ipady=7
)


get_button = tk.Button(
    search_frame,
    text="Get Weather",
    command=get_weather,
    font=("Segoe UI", 9, "bold"),
    bg="#7B61FF",
    fg="white",
    activebackground="#6C4AB6",
    activeforeground="white",
    bd=0,
    padx=15,
    pady=7,
    cursor="hand2"
)

get_button.grid(
    row=0,
    column=1,
    padx=4
)


unit_button = tk.Button(
    search_frame,
    text="Switch to °F",
    command=toggle_unit,
    font=("Segoe UI", 9, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#222222",
    activeforeground="white",
    bd=0,
    padx=12,
    pady=7,
    cursor="hand2"
)

unit_button.grid(
    row=0,
    column=2,
    padx=4
)


# =========================
# STATUS
# =========================

status_label = tk.Label(
    root,
    text="Enter a city to get weather information.",
    font=("Segoe UI", 8),
    bg="#ECE8FF",
    fg="#6C4AB6"
)

status_label.pack(
    pady=4
)


# =========================
# CURRENT WEATHER CARD
# =========================

current_frame = tk.Frame(
    root,
    bg="white",
    padx=25,
    pady=7
)

current_frame.pack(
    padx=40,
    pady=4,
    fill="x"
)


city_label = tk.Label(
    current_frame,
    text="City",
    font=("Segoe UI", 17, "bold"),
    bg="white",
    fg="#333333"
)

city_label.pack()


icon_label = tk.Label(
    current_frame,
    bg="white"
)

icon_label.pack()


temperature_label = tk.Label(
    current_frame,
    text="--°C",
    font=("Segoe UI", 28, "bold"),
    bg="white",
    fg="#6C4AB6"
)

temperature_label.pack()


condition_label = tk.Label(
    current_frame,
    text="Weather condition",
    font=("Segoe UI", 11),
    bg="white",
    fg="#555555"
)

condition_label.pack(
    pady=2
)


details_label = tk.Label(
    current_frame,
    text="Humidity: --\nWind Speed: --",
    font=("Segoe UI", 9),
    bg="white",
    fg="#555555",
    justify="center"
)

details_label.pack(
    pady=2
)


# =========================
# HOURLY FORECAST
# =========================

tk.Label(
    root,
    text="Next 6 Hours",
    font=("Segoe UI", 12, "bold"),
    bg="#ECE8FF",
    fg="#333333"
).pack(
    pady=(5, 2)
)


hourly_frame = tk.Frame(
    root,
    bg="#ECE8FF"
)

hourly_frame.pack()


# =========================
# DAILY FORECAST
# =========================

tk.Label(
    root,
    text="5-Day Forecast",
    font=("Segoe UI", 12, "bold"),
    bg="#ECE8FF",
    fg="#333333"
).pack(
    pady=(6, 2)
)


daily_frame = tk.Frame(
    root,
    bg="#ECE8FF"
)

daily_frame.pack()


# =========================
# START APP
# =========================

root.mainloop()