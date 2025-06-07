import requests
from typing import Dict, Any


class WeatherService:
    def __init__(self):
        # Using Open-Meteo API (free, no API key required)
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"  # Corrected URL

    def _get_coordinates(self, city: str) -> tuple:
        """Get latitude and longitude for a city"""
        try:
            response = requests.get(self.geocoding_url, params={'name': city, 'count': 1})
            response.raise_for_status()
            data = response.json()

            if data.get('results'):
                result = data['results'][0]
                return result['latitude'], result['longitude']
            return None, None
        except:
            return None, None

    def get_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city using Open-Meteo API"""
        lat, lon = self._get_coordinates(city)

        if not lat or not lon:
            return self._get_mock_weather(city)

        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,weather_code',
                'timezone': 'auto'
            }

            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            data = response.json()

            current = data['current']
            weather_desc = self._get_weather_description(current['weather_code'])

            return {
                'city': city,
                'temperature': round(current['temperature_2m']),
                'description': weather_desc,
                'feels_like': round(current['temperature_2m']),  # Simplified
                'humidity': current['relative_humidity_2m']
            }
        except requests.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")
            return self._get_mock_weather(city)

    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to description"""
        descriptions = {
            0: 'clear sky', 1: 'mainly clear', 2: 'partly cloudy', 3: 'overcast',
            45: 'fog', 48: 'fog', 51: 'light drizzle', 53: 'drizzle', 55: 'heavy drizzle',
            61: 'light rain', 63: 'rain', 65: 'heavy rain', 71: 'light snow',
            73: 'snow', 75: 'heavy snow', 95: 'thunderstorm'
        }
        return descriptions.get(code, 'partly cloudy')

    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """Fallback mock weather data"""
        return {
            'city': city,
            'temperature': 20,
            'description': 'partly cloudy',
            'feels_like': 20,
            'humidity': 60
        }

    def suggest_dining_type(self, weather_data: Dict[str, Any]) -> str:
        """Suggest indoor or outdoor dining based on weather"""
        temp = weather_data['temperature']
        description = weather_data['description'].lower()

        if temp < 10 or temp > 35:
            return "indoor"
        elif any(word in description for word in ['rain', 'storm', 'snow']):
            return "indoor"
        else:
            return "outdoor"


""" example code:     

if __name__ == "__main__":
    weather_service = WeatherService()
    weather_data = weather_service.get_weather("Chandigarh")
    print(f"Weather: {weather_data}")
    print(f"Dining suggestion: {weather_service.suggest_dining_type(weather_data)}")

"""