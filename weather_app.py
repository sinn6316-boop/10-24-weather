import os

import streamlit as st
# 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
st.markdown('<h1 style="font-weight:900; font-family:Comic Sans MS, Arial, sans-serif; color:#4FC3F7;">내일 뭐 입지? 전국 날씨 예보 🌦️</h1>', unsafe_allow_html=True)

def get_background_image(weather_desc, temp):
    desc = weather_desc.lower()
    # 구름 관련 설명 확장
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
import streamlit as st
import requests
import pandas as pd
import geocoder
region_map = {
    "서울": {
        "강남구": "Gangnam-gu", "송파구": "Songpa-gu", "강서구": "Gangseo-gu", "마포구": "Mapo-gu", "종로구": "Jongno-gu", "서초구": "Seocho-gu", "영등포구": "Yeongdeungpo-gu", "동작구": "Dongjak-gu", "성동구": "Seongdong-gu", "노원구": "Nowon-gu", "중구": "Jung-gu", "은평구": "Eunpyeong-gu", "서대문구": "Seodaemun-gu", "강북구": "Gangbuk-gu", "도봉구": "Dobong-gu", "금천구": "Geumcheon-gu", "관악구": "Gwanak-gu", "광진구": "Gwangjin-gu", "구로구": "Guro-gu", "양천구": "Yangcheon-gu", "성북구": "Seongbuk-gu", "동대문구": "Dongdaemun-gu", "중랑구": "Jungnang-gu", "강동구": "Gangdong-gu"
    },
    "인천": {
        "연수구": "Yeonsu-gu", "남동구": "Namdong-gu", "부평구": "Bupyeong-gu", "서구": "Seo-gu", "중구": "Jung-gu", "동구": "Dong-gu", "계양구": "Gyeyang-gu", "미추홀구": "Michuhol-gu", "강화군": "Ganghwa-gun", "옹진군": "Ongjin-gun"
    },
    "충청남도": {
        "천안시": "Cheonan", "공주시": "Gongju", "보령시": "Boryeong", "아산시": "Asan", "서산시": "Seosan", "논산시": "Nonsan", "계룡시": "Gyeryong", "당진시": "Dangjin", "금산군": "Geumsan-gun", "부여군": "Buyeo-gun", "서천군": "Seocheon-gun", "청양군": "Cheongyang-gun", "홍성군": "Hongseong-gun", "예산군": "Yesan-gun", "태안군": "Taean-gun"
    },
    "전라북도": {
        "전주시": "Jeonju", "군산시": "Gunsan", "익산시": "Iksan", "정읍시": "Jeongeup", "남원시": "Namwon", "김제시": "Gimje", "완주군": "Wanju-gun", "진안군": "Jinan-gun", "무주군": "Muju-gun", "장수군": "Jangsu-gun", "임실군": "Imsil-gun", "순창군": "Sunchang-gun", "고창군": "Gochang-gun", "부안군": "Buan-gun"
    },
    "전라남도": {
        "목포시": "Mokpo", "여수시": "Yeosu", "순천시": "Suncheon", "나주시": "Naju", "광양시": "Gwangyang", "담양군": "Damyang-gun", "곡성군": "Gokseong-gun", "구례군": "Gurye-gun", "고흥군": "Goheung-gun", "보성군": "Boseong-gun", "화순군": "Hwasun-gun", "장흥군": "Jangheung-gun", "강진군": "Gangjin-gun", "해남군": "Haenam-gun", "영암군": "Yeongam-gun", "무안군": "Muan-gun", "함평군": "Hampyeong-gun", "영광군": "Yeonggwang-gun", "장성군": "Jangseong-gun", "완도군": "Wando-gun", "진도군": "Jindo-gun", "신안군": "Shinan-gun"
    },
    "경상북도": {
        "포항시": "Pohang", "경주시": "Gyeongju", "김천시": "Gimcheon", "안동시": "Andong", "구미시": "Gumi", "영주시": "Yeongju", "영천시": "Yeongcheon", "상주시": "Sangju", "문경시": "Mungyeong", "경산시": "Gyeongsan", "군위군": "Gunwi-gun", "의성군": "Uiseong-gun", "청송군": "Cheongsong-gun", "영양군": "Yeongyang-gun", "영덕군": "Yeongdeok-gun", "청도군": "Cheongdo-gun", "고령군": "Goryeong-gun", "성주군": "Seongju-gun", "칠곡군": "Chilgok-gun", "예천군": "Yecheon-gun", "봉화군": "Bonghwa-gun", "울진군": "Uljin-gun", "울릉군": "Ulleung-gun"
    },
    "경상남도": {
        "창원시": "Changwon", "진주시": "Jinju", "통영시": "Tongyeong", "사천시": "Sacheon", "김해시": "Gimhae", "밀양시": "Miryang", "거제시": "Geoje", "양산시": "Yangsan", "의령군": "Uiryeong-gun", "함안군": "Haman-gun", "창녕군": "Changnyeong-gun", "고성군": "Goseong-gun", "남해군": "Namhae-gun", "하동군": "Hadong-gun", "산청군": "Sancheong-gun", "함양군": "Hamyang-gun", "거창군": "Geochang-gun", "합천군": "Hapcheon-gun"
    },
    "제주도": {
        "제주시": "Jeju", "서귀포시": "Seogwipo"
        }
                # CSS for background and weather box is injected via st.markdown string above
            """, unsafe_allow_html=True)
            emoji = get_weather_emoji(weather_desc)
            # 강수량 정보 추출
            rain_amount = 0
            rain_emoji = ''
            if 'rain' in data and ('1h' in data['rain'] or '3h' in data['rain']):
                rain_amount = data['rain'].get('1h', data['rain'].get('3h', 0))
                rain_emoji = '🌧️' if rain_amount > 0 else ''
            # 날씨 + 강수량 표시
            weather_line = f"날씨: {weather_desc} {emoji}"
            if rain_amount > 0:
                weather_line += f" / 강수량: {rain_amount}mm {rain_emoji}"
            st.markdown(f"<div class='weather-box'>", unsafe_allow_html=True)
            st.subheader(f"{city_label}의 현재 날씨")
            # 날씨 이미지 표시 (st.image로 변경)
            if bg_img:
                st.image(bg_img, width=120)
            st.write(weather_line)
            st.write(f"풍속: {data['wind']['speed']} m/s")
            # main 데이터프레임 변환 및 표 출력
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
                main_kor = {}
                for k, v in main.items():
                    main_kor[key_map.get(k, k)] = v
                df = pd.DataFrame([main_kor])
                st.write("주요 정보:")
                df['날씨'] = f"{weather_desc} {emoji}"
                df = df.rename(columns={
                    'temp': '온도(°C)',
                    'feels_like': '체감온도(°C)',
                    'temp_min': '최저온도(°C)',
                    'temp_max': '최고온도(°C)',
                    'humidity': '습도(%)',
                    'rain_1h': '강수량(1시간, mm)',
                    'snow_1h': '적설량(1시간, mm)',
                    'pressure': '기압(hPa)',
                    'sea_level': '해수면 기압'
                })
                cols = list(df.columns)
                # '지상 기압' 및 grnd_level 컬럼 제거
                for col_to_remove in ['지상 기압', 'grnd_level']:
                    if col_to_remove in cols:
                        cols.remove(col_to_remove)
                # '날씨'를 '기압(hPa)' 앞에, '기압(hPa)'을 '습도(%)' 뒤로 이동
                if '날씨' in cols and '기압(hPa)' in cols and '습도(%)' in cols:
                    cols.remove('날씨')
                    cols.remove('기압(hPa)')
                    humid_idx = cols.index('습도(%)')
                    cols.insert(humid_idx + 1, '기압(hPa)')
                    idx = cols.index('기압(hPa)')
                    cols.insert(idx, '날씨')
                    df = df[cols]
                # 온도와 습도 값에 이모지 및 파란색 스타일 추가
                def blue_temp(val):
                    if pd.notnull(val):
                        return f'<span style="color:#0074D9;font-weight:bold;">{val}🌡️</span>'
                    return val
                def blue_hum(val):
                    if pd.notnull(val):
                        return f'{val}💧'
                    return val
                styled_df = df.copy()
                if '온도(°C)' in styled_df.columns:
                    styled_df['온도(°C)'] = styled_df['온도(°C)'].apply(blue_temp)
                if '습도(%)' in styled_df.columns:
                    styled_df['습도(%)'] = styled_df['습도(%)'].apply(blue_hum)
                # 옷차림 추천에 이모지와 귀여운 글씨체 적용
                def cute_clothes(val):
                    emoji = get_clothes_emoji(val)
                    return f'<span style="font-family:Comic Sans MS, Arial,sans-serif;font-size:15px;color:#FFB300;font-weight:bold;">{val} {emoji}</span>' if pd.notnull(val) else val
                temp = main.get('temp')
                clothes = get_clothes_recommendation(temp) if temp is not None else None
                if clothes:
                    st.markdown(f'<div style="font-family:Comic Sans MS, Arial,sans-serif;font-size:18px;color:#FFB300;font-weight:bold;background:#FFF3CD;border-radius:8px;padding:10px;margin-bottom:10px;">옷차림 추천: {clothes} {get_clothes_emoji(clothes)}</div>', unsafe_allow_html=True)
                # 표에 적용
                if '옷차림 추천' in styled_df.columns:
                    styled_df['옷차림 추천'] = styled_df['옷차림 추천'].apply(cute_clothes)
                # 표 가로 길이 늘리고 글씨 크기 줄이기 (CSS 적용)
                st.markdown('''
<style>
.wide-table table {
    width: 100% !important;
    table-layout: auto !important;
}
.wide-table td, .wide-table th {
    font-size: 13px !important;
                    white-space: nowrap !important;
                }
                .wide-table td.weather-col {
                    text-align: center !important;
                }
                </style>
                """, unsafe_allow_html=True)
                # 모든 셀 중간 정렬
                def center_all_cells_html(df):
                    html = df.to_html(escape=False, index=False)
                    import re
                    html = re.sub(r'<td>', '<td style="text-align:center;">', html)
                    return html
                st.write(f'<div class="wide-table">{center_all_cells_html(styled_df)}</div>', unsafe_allow_html=True)
            else:
                st.write("main 데이터가 없습니다.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요.")

if menu == "주간 날씨":
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
    if st.button("주간 날씨 보기"):
        # OpenWeather 무료 API는 5일치 3시간 간격 예보만 제공하므로, 일별 평균값으로 주간 날씨 생성
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
        forecast_res = requests.get(forecast_url)
        if forecast_res.status_code == 200:
            forecast_data = forecast_res.json()
            days_map = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            # 3시간 간격 데이터에서 날짜별로 그룹화
            from collections import defaultdict, Counter
            daily_data = defaultdict(list)
            for entry in forecast_data['list']:
                date_str = entry['dt_txt'][:10]
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description']
                daily_data[date_str].append((temp, desc))
            # 오늘 기준 5일치만 추출
            today = datetime.date.today()
            week_list = []
            for i, (date_str, values) in enumerate(list(daily_data.items())[:5]):
                temps = [v[0] for v in values]
                feels = []
                descs = [v[1] for v in values]
                # 강수량 집계
                rain_amounts = []
                humidities = []
                for entry in forecast_data['list']:
                    if entry['dt_txt'][:10] == date_str:
                        feels.append(entry['main'].get('feels_like'))
                        # OpenWeather 3시간 예보에서 rain 정보
                        rain = entry.get('rain', {})
                        rain_3h = rain.get('3h', 0)
                        rain_amounts.append(rain_3h)
                        # 습도 정보
                        if 'humidity' in entry['main']:
                            humidities.append(entry['main']['humidity'])
                avg_temp = round(sum(temps)/len(temps), 1)
                avg_feels = round(sum(feels)/len(feels), 1) if feels else None
                avg_hum = round(sum(humidities)/len(humidities), 1) if humidities else None
                most_desc = Counter(descs).most_common(1)[0][0]
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                weekday = days_map[date_obj.weekday()]
                clothes = get_clothes_recommendation(avg_temp)
                emoji = get_weather_emoji(most_desc)
                # 일별 강수량 합계 (mm)
                total_rain = round(sum(rain_amounts), 1) if rain_amounts else 0
                rain_emoji = '🌧️' if total_rain > 0 else ''
                week_list.append({
                    "요일": weekday,
                    "날짜": date_str,
                    "기온(°C)": avg_temp if avg_temp is not None else None,
                    "체감온도(°C)": avg_feels if avg_feels is not None else None,
                    "날씨": f"{most_desc} {emoji}",
                    "강수량(mm)": f"{total_rain} {rain_emoji}",
                    "습도(%)": f"{avg_hum}💧" if avg_hum is not None else None,
                    "옷차림 추천": clothes
                })
            # 안내 문구 삭제
            df_week = pd.DataFrame(week_list)
            # 5일간 기온 변화 그래프 추가
            st.line_chart(df_week.set_index('날짜')[['기온(°C)', '체감온도(°C)']])
            # 온도값 파란색, 습도 이모지 적용
            def blue_temp(val):
                if pd.notnull(val):
                    return f'<span style="color:#0074D9;font-weight:bold;">{val}</span>'
                return val
            def blue_hum(val):
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
