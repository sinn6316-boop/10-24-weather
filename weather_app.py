import os
import datetime
import streamlit as st
import pandas as pd
# Import feature modules
from region_map import region_map
from weather_api import fetch_weather, fetch_forecast
from clothes import get_clothes_recommendation, get_clothes_emoji
from ui_helpers import get_background_image, get_weather_emoji


# 사이드바 메뉴 복원

# Restore visually rich sidebar menu buttons
st.sidebar.markdown('''
<style>
.sidebar-menu-card {
    background: #e3f2fd;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    padding: 32px 18px 24px 18px;
    margin-bottom: 24px;
}
.sidebar-menu-title {
    font-size: 28px;
    font-weight: 800;
    color: #1976d2;
    margin-bottom: 18px;
    text-align: center;
    letter-spacing: 1px;
}
.sidebar-menu-list {
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.sidebar-menu-item {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    padding: 16px 12px;
    font-size: 20px;
    font-weight: 600;
    color: #1976d2;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
    border: none;
}
.sidebar-menu-item:hover {
    background: #bbdefb;
    color: #0d47a1;
}
.sidebar-menu-icon {
    font-size: 26px;
    margin-right: 12px;
}
</style>
<div class="sidebar-menu-card">
    <div class="sidebar-menu-title">메뉴</div>
    <div class="sidebar-menu-list">
        <div class="sidebar-menu-item">🌤️ 오늘날씨</div>
        <div class="sidebar-menu-item">📅 주간날씨</div>
        <div class="sidebar-menu-item">👕 오늘의 옷차림</div>
    </div>
</div>
''', unsafe_allow_html=True)

# Streamlit button logic for menu switching
# Use session state for menu selection
menu_options = ["오늘날씨", "주간날씨", "오늘의 옷차림"]
menu_icons = ["🌤️", "📅", "👕"]
if "menu" not in st.session_state:
    st.session_state.menu = menu_options[0]
for i, option in enumerate(menu_options):
    if st.sidebar.button(f"{menu_icons[i]} {option}", key=f"menu_btn_{i}"):
        st.session_state.menu = option
menu = st.session_state.menu
# 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
st.markdown('<h1 style="font-weight:900; font-family:Comic Sans MS, Arial, sans-serif; color:#4FC3F7;">내일 뭐 입지? 전국 날씨 예보 🌦️</h1>', unsafe_allow_html=True)

# ...existing code...

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
    st.markdown('''
<style>
.modern-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 18px;
    background: #fff;
    border-radius: 18px;
    overflow: hidden;
}
.modern-table th {
    background: #1976d2;
    color: #fff;
    font-weight: 700;
    padding: 18px 12px;
    border-bottom: 2px solid #1565c0;
}
.modern-table td {
    text-align: center;
    padding: 16px 10px;
    border-bottom: 1px solid #e3e3e3;
    transition: background 0.2s;
}
.modern-table tr:hover td {
    background: #e3f2fd;
}
.modern-table tr:last-child td {
    border-bottom: none;
}
</style>
''', unsafe_allow_html=True)
    table_html = '<table class="modern-table">'
    table_html += '<tr><th>온도 구간</th><th>추천 옷차림</th></tr>'
    for row in temp_clothes:
        table_html += f'<tr><td style="color:{row["color"]}; font-weight:bold;">{row["구간"]}</td>'
        table_html += f'<td style="color:{row["color"]};">{row["추천"]}</td></tr>'
    table_html += '</table>'
    st.markdown(table_html, unsafe_allow_html=True)
elif menu == "오늘날씨":
            region_list = list(region_map.keys())
            selected_region = st.selectbox("지역 선택", region_list)
            subregion_list = list(region_map[selected_region].keys())
            selected_subregion = st.selectbox("도시/구 선택", subregion_list)
            submitted_today = st.button("완료")
                    # ...existing code...
            if submitted_today:
                city_en = region_map[selected_region][selected_subregion]
                city_query = f"{selected_region},{city_en}" if selected_region and city_en else city_en
                if API_KEY:
                    data = fetch_weather(city_query, API_KEY)
                    # 대구 구별: 정보가 없으면 대구 전체로 재검색
                    if selected_region == "대구" and not data:
                        data = fetch_weather("Daegu", API_KEY)
                        city_query = "Daegu"
                    elif not data:
                        data = fetch_weather(city_en, API_KEY)
                        city_query = city_en
                    if data:
                        weather_desc = data['weather'][0]['description']
                        temp = data['main'].get('temp') if 'main' in data else None
                        feels_like = data['main'].get('feels_like') if 'main' in data else None
                        humidity = data['main'].get('humidity') if 'main' in data else None
                        emoji = get_weather_emoji(weather_desc)
                        rain_amount = data.get('rain', {}).get('1h', 0)
                        today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                        st.markdown(
                            """
<div style='width:100%; min-width:400px; max-width:1600px; margin:0 auto; background:#eaf6ff; border-radius:48px; box-shadow:0 8px 32px rgba(0,0,0,0.10); padding:64px 48px;'>
    <div style='width:100%; height:80px; display:flex; align-items:center; justify-content:center; background:#1a4a7a; border-radius:24px 24px 0 0; margin-bottom:0;'>
        <span style='font-size:38px; font-weight:700; color:#fff;'>{today_str} {selected_subregion} 날씨</span>
    </div>
    <div style='display:flex; justify-content:center; align-items:stretch; gap:40px; padding-top:32px;'>
        <div style='flex:1; max-width:220px; background:#f7f7f7; border-radius:18px; padding:32px; text-align:center;'>
            <div style='font-size:80px;'>{emoji}</div>
            <div style='font-size:26px; margin-top:12px;'>날씨</div>
            <div style='font-size:34px; margin-top:12px;'>{weather_desc}</div>
        </div>
        <div style='flex:1; max-width:220px; background:#f7f7f7; border-radius:18px; padding:32px; text-align:center;'>
            <div style='font-size:80px;'>🌡️</div>
            <div style='font-size:80px;'>🌡️</div>
            <div style='font-size:26px; margin-top:12px;'>체감온도</div>
            <div style='font-size:34px; margin-top:12px;'>{feels_like}°C</div>
        </div>
        <div style='flex:1; max-width:220px; background:#f7f7f7; border-radius:18px; padding:32px; text-align:center;'>
            <div style='font-size:80px;'>💧</div>
            <div style='font-size:26px; margin-top:12px;'>습도</div>
            <div style='font-size:34px; margin-top:12px;'>{humidity}%</div>
        </div>
            <div style='flex:1; max-width:320px; background:#e0f7fa; border-radius:24px; padding:48px 32px; text-align:center;'>
                <div style='font-size:100px;'>🌧️</div>
                <div style='font-size:30px; margin-top:18px;'>강수량</div>
                <div style='font-size:40px; margin-top:18px;'>{rain_amount}mm</div>
            </div>
    </div>
</div>
""".format(
                            today_str=today_str,
                            selected_subregion=selected_subregion,
                            emoji=emoji,
                            weather_desc=weather_desc,
                            temp=temp if temp is not None else '정보 없음',
                            feels_like=feels_like if feels_like is not None else '정보 없음',
                            humidity=humidity if humidity is not None else '정보 없음',
                            rain_amount=rain_amount if rain_amount is not None else '정보 없음'
                        ), unsafe_allow_html=True)
elif menu == "주간날씨":
    region_list = list(region_map.keys())
    selected_region = st.selectbox("지역 선택", region_list)
    subregion_list = list(region_map[selected_region].keys())
    with st.form(key="weather_form_week"):
        selected_subregion = st.selectbox("도시/구 선택", subregion_list)
        submitted_week = st.form_submit_button("완료")
    if submitted_week:
        city_en = region_map[selected_region][selected_subregion]
        city_query = f"{selected_region},{city_en}" if selected_region and city_en else city_en
        if not API_KEY:
            st.write("API 키가 없습니다. 환경 변수 또는 secrets에 API 키를 설정하세요.")
        else:
            weather_data = fetch_weather(city_query, API_KEY)
            if weather_data and 'coord' in weather_data:
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                forecast_data = fetch_forecast(lat, lon, API_KEY)
                if forecast_data and 'list' in forecast_data:
                    st.subheader(f"{selected_subregion}의 주간 날씨 예보")
                    # 날짜별로 시간대별 표를 분리하여 출력
                    from collections import defaultdict
                    day_dict = defaultdict(list)
                    for item in forecast_data['list']:
                        date_str = item['dt_txt'].split(' ')[0]
                        desc = item['weather'][0]['description']
                        # 날씨 이모지
                        if '비' in desc or 'rain' in desc:
                            weather_emoji = '🌧️'
                        elif '구름' in desc or 'cloud' in desc:
                            weather_emoji = '☁️'
                        elif '맑음' in desc or 'clear' in desc:
                            weather_emoji = '☀️'
                        elif '눈' in desc or 'snow' in desc:
                            weather_emoji = '❄️'
                        elif '흐림' in desc or 'overcast' in desc:
                            weather_emoji = '🌫️'
                        else:
                            weather_emoji = ''
                        day_dict[date_str].append({
                            '시간': item['dt_txt'].split(' ')[1],
                            '온도(°C)': f"{item['main']['temp']} 🌡️",
                            '체감온도(°C)': f"{item['main']['feels_like']} 🌡️",
                            '습도(%)': f"{item['main']['humidity']} 💧",
                            '날씨': f"{desc} {weather_emoji}",
                            '강수량(mm)': f"{item.get('rain', {}).get('3h', 0)} 🌧️"
                        })
                    for date, rows in list(day_dict.items())[:5]:
                        st.markdown(f"### {date}")
                        df = pd.DataFrame(rows)
                        st.dataframe(df)
                else:
                    st.write("주간 날씨 정보를 가져올 수 없습니다.")
            else:
                st.write("해당 지역의 좌표 정보를 가져올 수 없습니다.")
