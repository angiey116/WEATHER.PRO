import requests
from database import WeatherObservation


def get_weather_observation(city_name, country_code="US"):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    geocode_params = {
        "name": city_name,
        "country": country_code,
        "count": 1
    }

    geocode_response = requests.get(geocode_url, params=geocode_params)
    geocode_data = geocode_response.json()

    if "results" not in geocode_data or len(geocode_data["results"]) == 0:
        print("City not found.")
        return None

    place = geocode_data["results"][0]
    latitude = place["latitude"]
    longitude = place["longitude"]
    city = place["name"]
    country = place["country"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()

    current_weather = weather_data["current_weather"]

    observation = WeatherObservation(
        city=city,
        country=country,
        latitude=latitude,
        longitude=longitude,
        temperature=current_weather["temperature"],
        windspeed=current_weather["windspeed"],
        elevation=weather_data.get("elevation", 0),
        observation_time=current_weather["time"]
    )

    return observation