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

# 사용자 API 키 직접 할당
API_KEY = "41d0805b0340385a400c764781eb7d0f"

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
        selected_region = st.selectbox("지역 선택", region_list)
        subregion_list = list(region_map[selected_region].keys())
        selected_subregion = st.selectbox("도시/구 선택", subregion_list)
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
                emoji = get_weather_emoji(weather_desc)
                rain_amount = data.get('rain', {}).get('1h', 0)
                st.subheader(f"{selected_subregion}의 현재 날씨")
                info = {
                    '온도(°C)': temp if temp is not None else "정보 없음",
                    '체감온도(°C)': feels_like if feels_like is not None else "정보 없음",
                    '습도(%)': humidity if humidity is not None else "정보 없음",
                    '날씨': f"{weather_desc} {emoji}" if weather_desc else "정보 없음",
                    '강수량(1시간, mm)': rain_amount if rain_amount is not None else "정보 없음"
                }
                df = pd.DataFrame([info])
                st.write("주요 정보:")
                st.dataframe(df)
                st.markdown("</div>", unsafe_allow_html=True)
elif menu == "주간날씨":
    with st.form(key="weather_form_week"):
        region_list = list(region_map.keys())
        selected_region = st.selectbox("지역 선택", region_list)
        subregion_list = list(region_map[selected_region].keys())
        selected_subregion = st.selectbox("도시/구 선택", subregion_list)
        submitted_week = st.form_submit_button("완료")
    if submitted_week:
        city_en = region_map[selected_region][selected_subregion]
        if not API_KEY:
            st.write("API 키가 없습니다. 환경 변수 또는 secrets에 API 키를 설정하세요.")
        else:
            weather_data = fetch_weather(city_en, API_KEY)
            if weather_data and 'coord' in weather_data:
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                forecast_data = fetch_forecast(lat, lon, API_KEY)
                if forecast_data and 'list' in forecast_data:
                    st.subheader(f"{selected_subregion}의 주간 날씨 예보")
                    # 예보 데이터에서 주요 정보만 추출하여 표로 표시
                    forecast_list = []
                    for item in forecast_data['list']:
                        forecast_list.append({
                            '날짜': item['dt_txt'],
                            '온도(°C)': item['main']['temp'],
                            '체감온도(°C)': item['main']['feels_like'],
                            '습도(%)': item['main']['humidity'],
                            '날씨': item['weather'][0]['description'],
                            '강수량(mm)': item.get('rain', {}).get('3h', 0)
                        })
                    df = pd.DataFrame(forecast_list)
                    st.dataframe(df)
                else:
                    st.write("주간 날씨 정보를 가져올 수 없습니다.")
            else:
                st.write("해당 지역의 좌표 정보를 가져올 수 없습니다.")
