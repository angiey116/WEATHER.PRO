import requests

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
    city = "chicago"
    country_code = "US"

    location = get_location(city, country_code)
    if location is None:
        return

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

    print(result)

if __name__ == "__main__":
    main()
