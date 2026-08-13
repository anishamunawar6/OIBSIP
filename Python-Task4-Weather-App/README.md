# Weather App

A Python-based GUI Weather Application that fetches and displays real-time weather information using the OpenWeatherMap API.

## Features

- Search weather by city name
- Display current temperature in °C and °F
- Display weather condition and description
- Display humidity percentage
- Display wind speed
- Display feels-like temperature
- Display weather condition icons
- Display next 6-hour forecast
- Display 5-day forecast
- Celsius / Fahrenheit toggle
- Invalid city error handling
- Invalid API key error handling
- Network timeout and connection error handling
- Secure API key using `.env`

## Technologies Used

- Python
- Tkinter
- Requests
- Pillow
- python-dotenv
- OpenWeatherMap API

## Project Structure

- main.py — Main Weather App application
- .env — API key configuration
- .gitignore — Files excluded from GitHub
- requirements.txt — Required Python packages
- README.md — Project documentation

## Installation

Install the required packages:

pip install requests Pillow python-dotenv

## API Key Setup

Create an account on OpenWeatherMap and generate an API key.

Create a `.env` file in the project folder and add:

OPENWEATHER_API_KEY=your_api_key_here

Never share your API key publicly or upload the `.env` file to GitHub.

## How to Run

Run the following command:

python main.py

Enter a city name in the search box and click the "Get Weather" button.

## Project Objective

The objective of this project is to build a Python application that fetches and displays real-time weather data for a user-specified location using a weather API.

## Task

Task 4 – Basic Weather App

Developed as part of the Python Programming Internship at Oasis Infobyte.

## Author

Anisha Munawar

GitHub: https://github.com/anishamunawar6