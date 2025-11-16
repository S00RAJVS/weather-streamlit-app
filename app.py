import streamlit as st
import requests
from fuzzywuzzy import process
import json

API_KEY = "your api key"  # Replace with your OpenWeather API key


# Load city list from JSON file
@st.cache_data
def load_cities():
    with open("/home/acer/Documents/weather fetching api/1/cities.json", "r") as f:
        return json.load(f)

CITY_LIST = load_cities()


def get_closest_city(user_input):
    """Return closest matching city for spelling mistakes."""
    match, score = process.extractOne(user_input, CITY_LIST)
    return match if score > 60 else None


def get_weather(city):
    """Fetch weather data from OpenWeather API."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params, timeout=5)
    response.raise_for_status()
    return response.json()


# ------------------ STREAMLIT UI ------------------

st.set_page_config(page_title="Smart Weather App", page_icon="⛅")

st.title("🌍 Smart Weather Search ")
st.write("Type any city 😎")

user_input = st.text_input("Enter city", "")

if user_input:
    corrected_city = get_closest_city(user_input.title())

    if corrected_city and corrected_city.lower() != user_input.lower():
        st.warning(f"Did you mean **{corrected_city}**?")
        city_to_use = corrected_city
    else:
        city_to_use = user_input.title()

    try:
        data = get_weather(city_to_use)

        st.success(f"🌦 Weather in {city_to_use}")

        st.metric("🌡 Temperature", f"{data['main']['temp']}°C")
        st.write(f"**☁ Condition:** {data['weather'][0]['description'].capitalize()}")
        st.write(f"**💧 Humidity:** {data['main']['humidity']}%")
        st.write(f"**💨 Wind Speed:** {data['wind']['speed']} m/s")

    except Exception as e:
        st.error("⚠️ Error fetching weather. Check API key or city name.")
