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
    "경기도": {
        "수원시": "Suwon", "고양시": "Goyang", "성남시": "Seongnam", "용인시": "Yongin", "부천시": "Bucheon", "안양시": "Anyang", "평택시": "Pyeongtaek", "의정부시": "Uijeongbu", "광명시": "Gwangmyeong", "하남시": "Hanam", "남양주시": "Namyangju", "파주시": "Paju", "시흥시": "Siheung", "김포시": "Gimpo", "광주시": "Gwangju", "군포시": "Gunpo", "오산시": "Osan", "이천시": "Icheon", "안성시": "Anseong", "구리시": "Guri", "안산시": "Ansan", "양주시": "Yangju", "포천시": "Pocheon", "동두천시": "Dongducheon", "여주시": "Yeoju", "연천군": "Yeoncheon-gun", "가평군": "Gapyeong-gun", "양평군": "Yangpyeong-gun"
    },
    "부산": {
        "해운대구": "Haeundae-gu", "수영구": "Suyeong-gu", "동래구": "Dongnae-gu", "부산진구": "Busanjin-gu", "남구": "Nam-gu", "북구": "Buk-gu", "사하구": "Saha-gu", "서구": "Seo-gu", "동구": "Dong-gu", "중구": "Jung-gu", "영도구": "Yeongdo-gu", "금정구": "Geumjeong-gu", "강서구": "Gangseo-gu", "연제구": "Yeonje-gu", "기장군": "Gijang-gun"
    },
    "대구": {
        "수성구": "Suseong-gu", "동구": "Dong-gu", "서구": "Seo-gu", "남구": "Nam-gu", "북구": "Buk-gu", "중구": "Jung-gu", "달서구": "Dalseo-gu", "달성군": "Dalseong-gun"
    },
    "광주": {
        "동구": "Dong-gu", "서구": "Seo-gu", "남구": "Nam-gu", "북구": "Buk-gu", "광산구": "Gwangsan-gu"
    },
    "대전": {
        "동구": "Dong-gu", "중구": "Jung-gu", "서구": "Seo-gu", "유성구": "Yuseong-gu", "대덕구": "Daedeok-gu"
    },
    "울산": {
        "중구": "Jung-gu", "남구": "Nam-gu", "동구": "Dong-gu", "북구": "Buk-gu", "울주군": "Ulju-gun"
    },
    "세종": {
        "세종시": "Sejong"
    },
    "강원도": {
        "춘천시": "Chuncheon", "원주시": "Wonju", "강릉시": "Gangneung", "동해시": "Donghae", "태백시": "Taebaek", "속초시": "Sokcho", "삼척시": "Samcheok", "홍천군": "Hongcheon-gun", "횡성군": "Hoengseong-gun", "영월군": "Yeongwol-gun", "평창군": "Pyeongchang-gun", "정선군": "Jeongseon-gun", "철원군": "Cheorwon-gun", "화천군": "Hwacheon-gun", "양구군": "Yanggu-gun", "인제군": "Inje-gun", "고성군": "Goseong-gun", "양양군": "Yangyang-gun"
    },
    "충청북도": {
        "청주시": "Cheongju", "충주시": "Chungju", "제천시": "Jecheon", "보은군": "Boeun-gun", "옥천군": "Okcheon-gun", "영동군": "Yeongdong-gun", "증평군": "Jeungpyeong-gun", "진천군": "Jincheon-gun", "괴산군": "Goesan-gun", "음성군": "Eumseong-gun", "단양군": "Danyang-gun"
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
}


# 환경변수에서 API 키 불러오기
import datetime
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 상단 제목은 위에서 이미 선언됨
st.sidebar.title("메뉴")
menu = st.sidebar.selectbox("메뉴 선택", ["오늘 날씨", "주간 날씨", "온도별 옷차림"])
if menu != "온도별 옷차림":
    st.write("한국 주요 도시를 선택하거나 직접 입력하세요.")
    region_list = list(region_map.keys())
    selected_region = st.selectbox("지역 선택", region_list)
    subregion_list = list(region_map[selected_region].keys())
    selected_subregion = st.selectbox(f"{selected_region} 내 구/시 선택", subregion_list)
    custom_city = st.text_input("직접 도시 입력 (한글)", "")
    use_location = st.checkbox("현재 위치 기준으로 보기 (IP 기반)")

def get_clothes_emoji(recommend):
    if "반팔" in recommend or "민소매" in recommend:
        return "👕🩳"
    elif "긴팔" in recommend or "니트" in recommend or "가디건" in recommend or "청바지" in recommend:
        return "👚👖"
    elif "자켓" in recommend or "코트" in recommend:
        return "🧥"
    elif "패딩" in recommend or "내복" in recommend or "방한용품" in recommend:
        return "🧥🧣"
    else:
        return "🧢"

def get_clothes_recommendation(temp):
    if temp >= 28:
        return "매우 더움: 반팔, 반바지, 민소매"
    elif temp >= 23:
        return "더움: 반팔, 얇은 셔츠, 반바지"
    elif temp >= 20:
        return "따뜻함: 긴팔, 얇은 가디건"
    elif temp >= 17:
        return "선선함: 얇은 니트, 가디건, 청바지"
    elif temp >= 12:
        return "조금 추움: 자켓, 가디건, 맨투맨"
    elif temp >= 9:
        return "추움: 코트, 가죽자켓, 히트텍"
    elif temp >= 5:
        return "매우 추움: 두꺼운 코트, 목도리"
    else:
        return "한파: 패딩, 내복, 방한용품"


# 함수 정의 이후, 최상위에서 메뉴 분기
# 온도별 옷차림 표 데이터 및 함수
def get_clothes_table():
    table = [
        {"온도 범위": "-10°C 이하", "옷차림": "패딩, 내복, 방한용품", "이모지": "🧥🧣"},
        {"온도 범위": "-9°C ~ 0°C", "옷차림": "두꺼운 코트, 목도리", "이모지": "🧥🧣"},
        {"온도 범위": "1°C ~ 4°C", "옷차림": "코트, 가죽자켓, 히트텍", "이모지": "🧥"},
        {"온도 범위": "5°C ~ 8°C", "옷차림": "자켓, 가디건, 맨투맨", "이모지": "🧥"},
        {"온도 범위": "9°C ~ 11°C", "옷차림": "얇은 니트, 가디건, 청바지", "이모지": "👚👖"},
        {"온도 범위": "12°C ~ 16°C", "옷차림": "긴팔, 얇은 가디건", "이모지": "👚👖"},
        {"온도 범위": "17°C ~ 19°C", "옷차림": "더움: 반팔, 얇은 셔츠, 반바지", "이모지": "👕🩳"},
        {"온도 범위": "20°C ~ 22°C", "옷차림": "매우 더움: 반팔, 반바지, 민소매", "이모지": "👕🩳"},
        {"온도 범위": "23°C 이상", "옷차림": "민소매, 반팔, 반바지", "이모지": "👕🩳"}
    ]
    df = pd.DataFrame(table)
    return df
if menu == "온도별 옷차림":
    st.subheader("온도별 옷차림")
    clothes_df = get_clothes_table()
    # 온도별 색상 매핑 (노랑~하늘색 그라데이션)
    temp_colors = [
        "#4FC3F7",  # -10°C 이하 (차가운 하늘색)
        "#81D4FA",  # -9~0°C
        "#B3E5FC",  # 1~4°C
        "#B2EBF2",  # 5~8°C
        "#FFE082",  # 9~11°C (연노랑)
        "#FFD54F",  # 12~16°C (노랑)
        "#FFCA28",  # 17~19°C (진노랑)
        "#FFB300",  # 20~22°C (따스한 노랑)
        "#FFA000"   # 23°C 이상 (따뜻한 오렌지)
    ]
    def style_row(row):
        idx = row.name
        color = temp_colors[idx] if idx < len(temp_colors) else "#FFB300"
        return [
            f'color:{color}; font-family:Comic Sans MS, Arial,sans-serif; font-size:16px; font-weight:bold;' for _ in row
        ]
    styled = clothes_df.style.apply(style_row, axis=1)
    st.markdown("""
    <style>
    .clothes-table table {
        width: 100% !important;
        table-layout: auto !important;
    }
    .clothes-table td, .clothes-table th {
        font-size: 16px !important;
        font-family: Comic Sans MS, Arial, sans-serif !important;
        font-weight: bold !important;
        white-space: nowrap !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.write(f'<div class="clothes-table">{styled.to_html(escape=False, index=False)}</div>', unsafe_allow_html=True)
# 온도별 옷차림 표 데이터 및 함수
def get_clothes_table():
    table = [
        {"온도 범위": "-10°C 이하", "옷차림": "패딩, 내복, 방한용품", "이모지": "🧥🧣"},
        {"온도 범위": "-9°C ~ 0°C", "옷차림": "두꺼운 코트, 목도리", "이모지": "🧥🧣"},
        {"온도 범위": "1°C ~ 4°C", "옷차림": "코트, 가죽자켓, 히트텍", "이모지": "🧥"},
        {"온도 범위": "5°C ~ 8°C", "옷차림": "자켓, 가디건, 맨투맨", "이모지": "🧥"},
        {"온도 범위": "9°C ~ 11°C", "옷차림": "얇은 니트, 가디건, 청바지", "이모지": "👚👖"},
        {"온도 범위": "12°C ~ 16°C", "옷차림": "긴팔, 얇은 가디건", "이모지": "👚👖"},
        {"온도 범위": "17°C ~ 19°C", "옷차림": "더움: 반팔, 얇은 셔츠, 반바지", "이모지": "👕🩳"},
        {"온도 범위": "20°C ~ 22°C", "옷차림": "매우 더움: 반팔, 반바지, 민소매", "이모지": "👕🩳"},
        {"온도 범위": "23°C 이상", "옷차림": "민소매, 반팔, 반바지", "이모지": "👕🩳"}
    ]
    df = pd.DataFrame(table)
    return df
if menu == "오늘 날씨":
    if st.button("날씨 보기"):
        if use_location:
            g = geocoder.ip('me')
            lat, lon = g.latlng if g.latlng else (37.5665, 126.9780)  # 기본값: 서울
            params = {
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "kr"
            }
            response = requests.get(BASE_URL, params=params)
            city_label = f"현재 위치({lat:.2f}, {lon:.2f})"
        else:
            if custom_city:
                city_kr = custom_city
                city_en = custom_city
            else:
                city_kr = f"{selected_region} {selected_subregion}"
                city_en = region_map[selected_region][selected_subregion]
            params = {
                "q": city_en,
                "appid": API_KEY,
                "units": "metric",
                "lang": "kr"
            }
            response = requests.get(BASE_URL, params=params)
            # 만약 구/군 단위 요청 실패 시, 시/도 단위로 재요청
            if response.status_code != 200:
                params["q"] = selected_region
                response = requests.get(BASE_URL, params=params)
                city_label = selected_region
                # 시/도 단위도 실패하면 대표 도시로 재요청
                if response.status_code != 200:
                    region_fallback = {
                        "경상북도": "Pohang",
                        "경상남도": "Changwon",
                        "강원도": "Chuncheon",
                        "충청북도": "Cheongju",
                        "충청남도": "Cheonan",
                        "전라북도": "Jeonju",
                        "전라남도": "Mokpo",
                        "제주도": "Jeju",
                        "경기도": "Suwon",
                        "서울": "Seoul",
                        "부산": "Busan",
                        "대구": "Daegu",
                        "인천": "Incheon",
                        "광주": "Gwangju",
                        "대전": "Daejeon",
                        "울산": "Ulsan",
                        "세종": "Sejong"
                    }
                    fallback_city = region_fallback.get(selected_region, "Seoul")
                    params["q"] = fallback_city
                    response = requests.get(BASE_URL, params=params)
                    city_label = fallback_city
            # 응답 데이터에서 실제 도시명 표시
            if response.status_code == 200:
                data = response.json()
                city_label = data.get('name', params["q"])
            else:
                city_label = params["q"]
        if response.status_code == 200:
            data = response.json()
            weather_desc = data['weather'][0]['description']
            temp = data['main'].get('temp') if 'main' in data else None
            bg_img = get_background_image(weather_desc, temp)
            # 배경 이미지 CSS 적용
            st.markdown(f"""
                <style>
                .stApp {{
                    background: url('{bg_img}') no-repeat center center fixed;
                    background-size: cover;
                }}
                .weather-box {{
                    background: rgba(255,255,255,0.85);
                    border-radius: 16px;
                    padding: 24px;
                    margin-bottom: 24px;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                }}
                </style>
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
