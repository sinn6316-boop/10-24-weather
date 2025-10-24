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

# 메뉴 복원: 사이드바에 메뉴 추가

region_list = list(region_map.keys())
selected_region = st.selectbox("지역 선택", region_list, key="main_region")
subregion_list = list(region_map[selected_region].keys())
selected_subregion = st.selectbox("도시/구 선택", subregion_list, key="main_subregion")
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

        elif menu == "오늘의 옷차림":
            st.subheader(f"{selected_subregion} 오늘의 옷차림 추천")
            clothes = get_clothes_recommendation(temp) if temp is not None else None
            if clothes:
                st.markdown(f'<div style="font-family:Comic Sans MS, Arial,sans-serif;font-size:22px;color:#FFB300;font-weight:bold;background:#FFF3CD;border-radius:8px;padding:16px;margin-bottom:10px;">{clothes} {get_clothes_emoji(clothes)}</div>', unsafe_allow_html=True)
            else:
                st.info("기온 정보가 부족해 옷차림 추천이 어렵습니다.")

        elif menu == "주간날씨":
            st.subheader(f"{selected_subregion}의 주간 날씨 (최대 5일치)")
            # 주간 예보: OpenWeather의 forecast API 사용
            # 도시의 위도/경도 정보가 필요하므로, 현재 날씨 데이터에서 추출
            if 'coord' in data:
                lat, lon = data['coord']['lat'], data['coord']['lon']
                forecast = fetch_forecast(lat, lon, API_KEY)
                if forecast and 'list' in forecast:
                    # 3시간 단위 예보를 날짜별로 집계
                    import datetime
                    from collections import defaultdict
                    daily = defaultdict(list)
                    for entry in forecast['list']:
                        dt = datetime.datetime.fromtimestamp(entry['dt'])
                        date_str = dt.strftime('%Y-%m-%d')
                        daily[date_str].append(entry)
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
                                    st.write("<b>주요 정보</b>", unsafe_allow_html=True)
                                    # 표 디자인 개선: 가운데 정렬, 폰트/컬러 적용
                                    st.dataframe(df.style.set_properties(**{
                                        'text-align': 'center',
                                        'font-family': 'Comic Sans MS, Arial, sans-serif',
                                        'font-size': '18px',
                                        'color': '#1976D2',
                                        'background': '#E3F2FD'
                                    }))
                                st.markdown("</div>", unsafe_allow_html=True)

                            elif menu == "오늘의 옷차림":
                                st.subheader(f"{selected_subregion} 오늘의 옷차림 추천")
                                clothes = get_clothes_recommendation(temp) if temp is not None else None
                                if clothes:
                                    st.markdown(f'<div style="font-family:Comic Sans MS, Arial,sans-serif;font-size:22px;color:#FFB300;font-weight:bold;background:#FFF3CD;border-radius:8px;padding:16px;margin-bottom:10px;">{clothes} {get_clothes_emoji(clothes)}</div>', unsafe_allow_html=True)
                                else:
                                    st.info("기온 정보가 부족해 옷차림 추천이 어렵습니다.")

                            elif menu == "주간날씨":
                                st.subheader(f"{selected_subregion}의 주간 날씨 (최대 5일치)")
                                # 주간 예보: OpenWeather의 forecast API 사용
                                if 'coord' in data:
                                    lat, lon = data['coord']['lat'], data['coord']['lon']
                                    forecast = fetch_forecast(lat, lon, API_KEY)
                                    if forecast and 'list' in forecast:
                                        import datetime
                                        from collections import defaultdict
                                        daily = defaultdict(list)
                                        for entry in forecast['list']:
                                            dt = datetime.datetime.fromtimestamp(entry['dt'])
                                            date_str = dt.strftime('%Y-%m-%d')
                                            daily[date_str].append(entry)
                                        # 최대 5일치만 출력
                                        for i, (date, entries) in enumerate(daily.items()):
                                            if i >= 5:
                                                break
                                            temps = [e['main']['temp'] for e in entries if 'main' in e]
                                            feels = [e['main']['feels_like'] for e in entries if 'main' in e]
                                            descs = [e['weather'][0]['description'] for e in entries if 'weather' in e and e['weather']]
                                            avg_temp = round(sum(temps)/len(temps), 1) if temps else None
                                            avg_feels = round(sum(feels)/len(feels), 1) if feels else None
                                            most_desc = max(set(descs), key=descs.count) if descs else ''
                                            emoji = get_weather_emoji(most_desc)
                                            clothes = get_clothes_recommendation(avg_temp) if avg_temp is not None else None
                                            # 표 디자인: 날짜, 날씨, 평균기온, 체감, 옷차림
                                            st.markdown(f"<div style='margin-bottom:10px;padding:10px;border-radius:8px;background:#E3F2FD;'>"
                                                        f"<b>{date}</b> {emoji}<br>"
                                                        f"평균기온: <b>{avg_temp}°C</b>, 체감: <b>{avg_feels}°C</b><br>"
                                                        f"날씨: <b>{most_desc}</b><br>"
                                                        f"옷차림 추천: <b>{clothes} {get_clothes_emoji(clothes)}</b>"
                                                        f"</div>", unsafe_allow_html=True)
                                    else:
                                        st.info("주간 예보 데이터를 가져올 수 없습니다.")
                                else:
                                    st.info("위치 정보가 부족해 주간 예보를 가져올 수 없습니다.")
                        else:
                            st.error("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요.")
                    else:
                        st.error("API 키가 설정되지 않았습니다. .env 또는 secrets.toml을 확인하세요.")
