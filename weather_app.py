import os
import streamlit as st
import pandas as pd
# Import feature modules
from region_map import region_map
from weather_api import fetch_weather, fetch_forecast
from clothes import get_clothes_recommendation, get_clothes_emoji
from ui_helpers import get_background_image, get_weather_emoji


# 사이드바 메뉴 복원

st.sidebar.title("메뉴")
# 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
st.markdown('<h1 style="font-weight:900; font-family:Comic Sans MS, Arial, sans-serif; color:#4FC3F7;">내일 뭐 입지? 전국 날씨 예보 🌦️</h1>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("메뉴 선택", ["오늘날씨", "주간날씨", "오늘의 옷차림"], key="sidebar_menu")

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if menu == "오늘의 옷차림":
    st.subheader("온도별 옷차림 추천표")
    temp_clothes = [
        {"구간": "-10°C 이하", "추천": "패딩, 두꺼운 코트, 목도리, 기모바지", "color": "#4FC3F7"},
        {"구간": "-9°C ~ 0°C", "추천": "패딩, 코트, 니트, 기모바지", "color": "#64B5F6"},
        {"구간": "1°C ~ 4°C", "추천": "코트, 가죽자켓, 히트텍, 니트, 청바지", "color": "#90CAF9"},
        {"구간": "5°C ~ 8°C", "추천": "자켓, 트렌치코트, 야상, 니트, 청바지", "color": "#BBDEFB"},
        {"구간": "9°C ~ 11°C", "추천": "자켓, 가디건, 야상, 청바지, 면바지", "color": "#FFE082"},
        {"구간": "12°C ~ 16°C", "추천": "자켓, 가디건, 야상, 청바지, 면바지", "color": "#FFD54F"},
        {"구간": "17°C ~ 19°C", "추천": "얇은 니트, 맨투맨, 가디건, 청바지", "color": "#FFB300"},
        {"구간": "20°C ~ 22°C", "추천": "긴팔, 얇은 가디건, 면바지", "color": "#FFA000"},
        {"구간": "23°C ~ 27°C", "추천": "반팔, 얇은 셔츠, 얇은 바지, 면바지", "color": "#FF8F00"},
        {"구간": "28°C 이상", "추천": "민소매, 반팔, 반바지, 원피스", "color": "#FF6F00"}
    ]
    st.markdown('<style>.clothes-table td, .clothes-table th {text-align:center; font-family:Comic Sans MS, Arial,sans-serif; font-size:18px;}</style>', unsafe_allow_html=True)
    table_html = '<table class="clothes-table" style="width:100%; border-collapse:collapse;">'
    table_html += '<tr><th>온도 구간</th><th>추천 옷차림</th></tr>'
    for row in temp_clothes:
        table_html += f'<tr><td style="color:{row["color"]}; font-weight:bold;">{row["구간"]}</td>'
        table_html += f'<td style="color:{row["color"]};">{row["추천"]}</td></tr>'
    table_html += '</table>'
    st.markdown(table_html, unsafe_allow_html=True)
elif menu == "오늘날씨":
    with st.form(key="weather_form_today"):
        region_list = list(region_map.keys())
        selected_region = st.selectbox("지역 선택", region_list, key="main_region_today")
        subregion_list = list(region_map[selected_region].keys())
        selected_subregion = st.selectbox("도시/구 선택", subregion_list, key="main_subregion_today")
        submitted_today = st.form_submit_button("완료")
    if submitted_today:
        city_en = region_map[selected_region][selected_subregion]
        if API_KEY:
            data = fetch_weather(city_en, API_KEY)
            if data:
                weather_desc = data['weather'][0]['description']
                temp = data['main'].get('temp') if 'main' in data else None
                feels_like = data['main'].get('feels_like') if 'main' in data else None
                humidity = data['main'].get('humidity') if 'main' in data else None
                bg_img = get_background_image(weather_desc, temp)
                emoji = get_weather_emoji(weather_desc)
                rain_amount = data.get('rain', {}).get('1h', 0)
                st.markdown(f"<div class='weather-box'>", unsafe_allow_html=True)
                st.subheader(f"{selected_subregion}의 현재 날씨")
                if bg_img:
                    st.image(bg_img, width=120)
                info = {
                    '온도(°C)': temp,
                    '체감온도(°C)': feels_like,
                    '습도(%)': humidity,
                    '날씨': f"{weather_desc} {emoji}",
                    '강수량(1시간, mm)': rain_amount
                }
                df = pd.DataFrame([info])
                st.write("주요 정보:")
                st.dataframe(df)
                st.markdown("</div>", unsafe_allow_html=True)
            if menu == "오늘날씨":
                st.markdown(f"<div class='weather-box'>", unsafe_allow_html=True)
                st.subheader(f"{selected_subregion}의 현재 날씨")
                if bg_img:
                    st.image(bg_img, width=120)
                st.write(weather_line)
                st.write(f"풍속: {data['wind']['speed']} m/s")
                # 주요 정보 표
                if 'main' in data:
                    main = data['main']
                    key_map = {
                        'temp': '온도(°C)',
                        'feels_like': '체감온도(°C)',
                        'temp_min': '최저온도(°C)',
                        'temp_max': '최고온도(°C)',
                        'humidity': '습도(%)'
                    }
                    if 'rain' in data and '1h' in data['rain']:
                        main['rain_1h'] = data['rain']['1h']
                        key_map['rain_1h'] = '강수량(1시간, mm)'
                    if 'snow' in data and '1h' in data['snow']:
                        main['snow_1h'] = data['snow']['1h']
                        key_map['snow_1h'] = '적설량(1시간, mm)'
                    main_kor = {key_map.get(k, k): v for k, v in main.items()}
                    df = pd.DataFrame([main_kor])
                    st.write("주요 정보:")
                    df['날씨'] = f"{weather_desc} {emoji}"
                    st.dataframe(df)
                st.markdown("</div>", unsafe_allow_html=True)
elif menu == "주간날씨":
    with st.form(key="weather_form_week"):
        region_list = list(region_map.keys())
        selected_region = st.selectbox("지역 선택", region_list, key="main_region_week")
        subregion_list = list(region_map[selected_region].keys())
        selected_subregion = st.selectbox("도시/구 선택", subregion_list, key="main_subregion_week")
        submitted_week = st.form_submit_button("완료")
    if submitted_week:
        city_en = region_map[selected_region][selected_subregion]
        if API_KEY:
            forecast = fetch_forecast(city_en, API_KEY)
            if forecast:
                st.subheader(f"{selected_subregion}의 주간 날씨 예보")
                df = pd.DataFrame(forecast)
                st.dataframe(df)
            else:
                st.write("주간 날씨 정보를 가져올 수 없습니다.")
