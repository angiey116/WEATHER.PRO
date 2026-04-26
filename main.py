import requests
from database import WeatherDatabase, WeatherObservation

db = WeatherDatabase(
    dbname="weather_project",
    user="postgres",
    password="cubbies1",)

def get_location(city: str, country_code: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "country": country_code,
        "count": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        print("No location found. Check city and country code.")
        return None

    first_result = data["results"][0]

    return {
        "city": first_result["name"],
        "country": first_result["country"],
        "latitude": first_result["latitude"],
        "longitude": first_result["longitude"]
    }

def get_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data["current_weather"]

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "elevation": data["elevation"],
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "observation_time": current["time"]
    }

def main():
    cities = [
        ("Chicago", "US"),
        ("New York", "US"),
        ("Los Angeles", "US"),
        ("London", "GB"),
        ("Paris", "FR"),
        ("Tokyo", "JP"),
        ("Sydney", "AU"),
        ("Toronto", "CA"),
        ("Rome", "IT"),
        ("Dubai", "AE")
]
    for city, country_code in cities:
        location = get_location(city, country_code)

        if location is None:
            continue

        weather = get_weather(location["latitude"], location["longitude"])

        result = {
            "city": location["city"],
            "country": location["country"],
            "latitude": weather["latitude"],
            "longitude": weather["longitude"],
            "temperature": weather["temperature"],
            "elevation": weather["elevation"],
            "windspeed": weather["windspeed"],
            "observation_time": weather["observation_time"]
        }
        
        observation = WeatherObservation(
            city=result["city"],
            country=result["country"],
            latitude=result["latitude"],
            longitude=result["longitude"],
            temperature=result["temperature"],
            windspeed=result["windspeed"],
            elevation=result["elevation"],
            observation_time=result["observation_time"]
        )
        db.insert_observation(observation)
        print(f"saved {result['city']}, {result['country']}")

if __name__ == "__main__":
    main()
    db.close()

