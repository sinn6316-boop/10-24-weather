import os

import streamlit as st
# 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
st.markdown('<h1 style="font-weight:900; font-family:Comic Sans MS, Arial, sans-serif; color:#4FC3F7;">내일 뭐 입지? 전국 날씨 예보 🌦️</h1>', unsafe_allow_html=True)


# --- Main Streamlit App Logic ---
API_KEY = os.getenv("OPENWEATHER_API_KEY")

region_list = list(region_map.keys())
selected_region = st.selectbox("지역 선택", region_list)
subregion_list = list(region_map[selected_region].keys())
selected_subregion = st.selectbox("도시/구 선택", subregion_list)

city_en = region_map[selected_region][selected_subregion]

if API_KEY:
    data = fetch_weather(city_en, API_KEY)
    if data:
        weather_desc = data['weather'][0]['description']
        temp = data['main'].get('temp') if 'main' in data else None
        bg_img = get_background_image(weather_desc, temp)
        emoji = get_weather_emoji(weather_desc)
        rain_amount = data.get('rain', {}).get('1h', data.get('rain', {}).get('3h', 0)
        rain_emoji = '🌧️' if rain_amount > 0 else ''
        weather_line = f"날씨: {weather_desc} {emoji}"
        if rain_amount > 0:
            weather_line += f" / 강수량: {rain_amount}mm {rain_emoji}"
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
            # 표 스타일링 및 옷차림 추천
            temp = main.get('temp')
            clothes = get_clothes_recommendation(temp) if temp is not None else None
            if clothes:
                st.markdown(f'<div style="font-family:Comic Sans MS, Arial,sans-serif;font-size:18px;color:#FFB300;font-weight:bold;background:#FFF3CD;border-radius:8px;padding:10px;margin-bottom:10px;">옷차림 추천: {clothes} {get_clothes_emoji(clothes)}</div>', unsafe_allow_html=True)
            st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요.")
else:
    st.error("API 키가 설정되지 않았습니다. .env 또는 secrets.toml을 확인하세요.")
    # 온도별 옷차림 메뉴에서는 표만 표시, 날씨 기능 없음
    st.subheader("주간 날씨 (최대 5일치)")
    st.write("지역을 선택한 후 '주간 날씨 보기' 버튼을 눌러주세요.")
    if use_location:
        g = geocoder.ip('me')
        lat, lon = g.latlng if g.latlng else (37.5665, 126.9780)
    else:
        if custom_city:
            city_en = custom_city
        else:
            city_en = region_map[selected_region][selected_subregion]
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_en}&limit=1&appid={API_KEY}"
        geo_res = requests.get(geo_url)
        if geo_res.status_code == 200 and geo_res.json():
            geo_data = geo_res.json()[0]
            lat, lon = geo_data['lat'], geo_data['lon']
        else:
            lat, lon = 37.5665, 126.9780

    import os
    import streamlit as st
    import pandas as pd
    import geocoder
    # Import feature modules
    from region_map import region_map
    from weather_api import fetch_weather, fetch_forecast
    from clothes import get_clothes_recommendation, get_clothes_emoji
    from ui_helpers import get_background_image, get_weather_emoji

    # 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
            def blue_hum(val):

    # --- Main Streamlit App Logic ---
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    region_list = list(region_map.keys())
    selected_region = st.selectbox("지역 선택", region_list)
    subregion_list = list(region_map[selected_region].keys())
    selected_subregion = st.selectbox("도시/구 선택", subregion_list)

    city_en = region_map[selected_region][selected_subregion]

    if API_KEY:
        data = fetch_weather(city_en, API_KEY)
        if data:
            weather_desc = data['weather'][0]['description']
            temp = data['main'].get('temp') if 'main' in data else None
            bg_img = get_background_image(weather_desc, temp)
            emoji = get_weather_emoji(weather_desc)
        rain_amount = data.get('rain', {}).get('1h', data.get('rain', {}).get('3h', 0))
            rain_emoji = '🌧️' if rain_amount > 0 else ''
            weather_line = f"날씨: {weather_desc} {emoji}"
            if rain_amount > 0:
                weather_line += f" / 강수량: {rain_amount}mm {rain_emoji}"
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
                # 표 스타일링 및 옷차림 추천
                temp = main.get('temp')
                clothes = get_clothes_recommendation(temp) if temp is not None else None
                if clothes:
                    st.markdown(f'<div style="font-family:Comic Sans MS, Arial,sans-serif;font-size:18px;color:#FFB300;font-weight:bold;background:#FFF3CD;border-radius:8px;padding:10px;margin-bottom:10px;">옷차림 추천: {clothes} {get_clothes_emoji(clothes)}</div>', unsafe_allow_html=True)
                st.dataframe(df)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요.")
    else:
        st.error("API 키가 설정되지 않았습니다. .env 또는 secrets.toml을 확인하세요.")
                if pd.notnull(val):
                    # 이모지 1개만
                    return f'{str(val).replace("💧", "")}💧'
                return val
            def cute_clothes(val):
                emoji = get_clothes_emoji(val)
                return f'<span style="font-family:Comic Sans MS, Arial,sans-serif;font-size:15px;color:#FFB300;font-weight:bold;">{val} {emoji}</span>' if pd.notnull(val) else val
            styled_week = df_week.copy()
            if '기온(°C)' in styled_week.columns:
                styled_week['기온(°C)'] = styled_week['기온(°C)'].apply(blue_temp)
            if '습도(%)' in styled_week.columns:
                styled_week['습도(%)'] = styled_week['습도(%)'].apply(blue_hum)
            if '옷차림 추천' in styled_week.columns:
                styled_week['옷차림 추천'] = styled_week['옷차림 추천'].apply(cute_clothes)
            # 표 가로 길이 늘리고 글씨 크기 줄이기 (CSS 적용)
            st.markdown("""
            <style>
            .wide-table table {
                width: 100% !important;
                table-layout: auto !important;
            }
            .wide-table td, .wide-table th {
                font-size: 13px !important;
                white-space: nowrap !important;
            }
            </style>
            """, unsafe_allow_html=True)
            def center_all_cells_html(df):
                html = df.to_html(escape=False, index=False)
                import re
                html = re.sub(r'<td>', '<td style="text-align:center;">', html)
                return html
            st.write(f'<div class="wide-table">{center_all_cells_html(styled_week)}</div>', unsafe_allow_html=True)
        else:
            st.error("주간 날씨 정보를 가져올 수 없습니다.")


    # ...existing code...
