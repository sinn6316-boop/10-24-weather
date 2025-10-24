# weather_api.py
# 날씨 API 요청 및 관련 함수
import requests

def fetch_weather(city_en, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
