# weather_api.py
# 날씨 API 요청 및 관련 함수
import requests

def fetch_weather(city_en, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    # 자동 보정: 도시명에 ','가 없으면 지역명을 붙여서 재검색
    if ',' not in city_en:
        # 예: Seoul,Gangnam-gu 또는 Busan,Haeundae-gu
        # 지역명 추출 (시/도)
        # city_en이 'Gangnam-gu'라면, 서울 등 상위 지역명을 붙여서 재검색
        # 실제로는 호출부에서 지역명과 도시명을 모두 알 수 있으므로, city_en을 튜플로 받을 수 있음
        # 여기서는 city_en이 '지역,도시' 형태가 아니면 None 반환
        return None
    else:
        # ','가 있으면 그래도 실패 시 None 반환
        return None

def fetch_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
