# weather_api.py
# 날씨 API 요청 및 관련 함수
import requests

def fetch_weather(city_en, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    # 자동 보정: '지역,도시'로 실패하면 '도시'만 단독으로 재검색
    if ',' in city_en:
        city_only = city_en.split(',')[1].strip()
        url2 = f"https://api.openweathermap.org/data/2.5/weather?q={city_only}&appid={api_key}&units=metric&lang=kr"
        response2 = requests.get(url2)
        if response2.status_code == 200:
            return response2.json()
    return None

def fetch_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
