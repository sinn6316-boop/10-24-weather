# ui_helpers.py
# UI 관련 함수 (배경, 이모지, 테이블 스타일 등)

def get_background_image(weather_desc, temp):
    desc = weather_desc.lower()
    if '비' in desc or 'rain' in desc:
        return 'images/비.jpg'
    elif (
        '구름' in desc or 'cloud' in desc or '흐림' in desc or 'overcast' in desc or 'mist' in desc or '안개' in desc
    ):
        return 'images/구름.jpg'
    elif '맑음' in desc or 'clear' in desc:
        return 'images/맑음.jpg'
    elif temp is not None and temp >= 28:
        return 'images/더움.jpg'
    elif temp is not None and 17 <= temp < 28:
        return 'images/따스함.jpg'
    elif temp is not None and temp < 17:
        return 'images/쌀쌀함.jpg'
    else:
        return 'images/맑음.jpg'

def get_weather_emoji(desc):
    desc = desc.lower()
    if '비' in desc or 'rain' in desc:
        return '🌧️'
    elif '구름' in desc or 'cloud' in desc:
        return '☁️'
    elif '맑음' in desc or 'clear' in desc:
        return '☀️'
    elif '눈' in desc or 'snow' in desc:
        return '❄️'
    elif '흐림' in desc or 'overcast' in desc:
        return '🌫️'
    else:
        return ''
