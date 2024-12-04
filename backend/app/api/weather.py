from pydantic import BaseModel, ValidationError
from app.config import OPENWEATHERMAP_API_KEY
from pathlib import Path
import requests

# Base URLs
ONE_CALL_API_URL = "https://api.openweathermap.org/data/2.5/weather"
GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"


class WeatherQueryModel(BaseModel):
    """Model for weather query validation."""
    city: str
    units: str = "metric"  # Default to metric units
    exclude: str = "minutely,hourly"  # Exclude unnecessary data

    def validate_units(self):
        if self.units not in {"metric", "imperial", "standard"}:
            raise ValueError(f"Invalid units '{self.units}'. Must be one of 'metric', 'imperial', or 'standard'.")

    def validate(self):
        self.validate_units()


def make_request(endpoint: str, query_params: dict) -> dict:
    """General request function for Weather API."""
    full_url = endpoint

    # Make the request
    response = requests.get(url=full_url, params=query_params)

    # Parse request if valid
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"""
            Error {response.status_code} in make_request 
            for URL {full_url}
            with params {query_params}: {response.text}
        """)


def get_lat_lon(city_name: str):
    """Fetch latitude and longitude for a city using OpenWeather Geocoding API."""
    query_params = {
        "q": city_name,
        "limit": 1,
        "appid": OPENWEATHERMAP_API_KEY
    }
    result = make_request(endpoint=GEOCODING_API_URL, query_params=query_params)

    if result:
        location = result[0]
        return location["lat"], location["lon"]
    else:
        raise Exception(f"Geocoding API failed to find coordinates for city: {city_name}")


def query_weather(query: WeatherQueryModel):
    """Query weather using the One Call API based on the WeatherQueryModel."""
    # Validate input
    try:
        query.validate()
    except ValidationError as e:
        raise Exception(f"Invalid query parameters: {e}")

    # Get latitude and longitude for the city
    lat, lon = get_lat_lon(query.city)

    print(f"Querying weather for: city={query.city}, lat={lat}, lon={lon}, units={query.units}")

    # Call One Call API with latitude and longitude
    query_params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": query.units,
        "exclude": query.exclude
    }
    result = make_request(endpoint=ONE_CALL_API_URL, query_params=query_params)
    
    print(result)

    # Extract current weather data
    weather_description = (
        result.get("weather", [{}])[0].get("description", "No description available").capitalize()
    )
    temperature = result.get("main", {}).get("temp", "N/A")

    # Format and return the weather information
    return f"Current weather in {query.city}: {weather_description}, Temp: {temperature}°C"


if __name__ == "__main__":
    # Example usage
    query = WeatherQueryModel(city="Paris", units="metric", exclude="minutely,hourly")
    weather_info = query_weather(query)
    print(weather_info)
