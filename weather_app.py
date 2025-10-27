# ...existing code...
import os
import datetime
import streamlit as st
import pandas as pd
# Import feature modules
from region_map import region_map
from weather_api import fetch_weather, fetch_forecast
from clothes import get_clothes_recommendation, get_clothes_emoji
from ui_helpers import get_background_image, get_weather_emoji


# 귀여운 상단 제목 (굵고, 귀여운 글씨체, 날씨 이모지)
st.markdown('<h1 style="font-weight:900; font-family:Comic Sans MS, Arial, sans-serif; color:#4FC3F7;">내일 뭐 입지? 전국 날씨 예보 🌦️</h1>', unsafe_allow_html=True)

# 사용자 API 키 직접 할당
API_KEY = "41d0805b0340385a400c764781eb7d0f"

# 메뉴 선택 복원 (사이드바)
menu = st.sidebar.selectbox("메뉴 선택", ["오늘날씨", "주간날씨", "오늘의 옷차림"])

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
	if submitted_today:
		city_en = region_map[selected_region][selected_subregion]
		city_query = f"{selected_region},{city_en}" if selected_region and city_en else city_en
		if API_KEY:
			data = fetch_weather(city_query, API_KEY)
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

				# 아침 한마디 메시지 생성
				morning_msg = ""
				if temp is not None:
					try:
						t = float(temp)
						if t <= 0:
							morning_msg = "오늘은 많이 추워요! 따뜻하게 입고 감기 조심하세요 ☃️"
						elif t <= 10:
							morning_msg = "쌀쌀한 아침입니다. 옷 든든히 챙기고 힘내세요! 💪"
						elif t <= 20:
							morning_msg = "상쾌한 날씨! 오늘도 좋은 하루 보내세요 😊"
						elif t <= 27:
							morning_msg = "활기찬 하루 시작! 가벼운 옷차림으로 산뜻하게 출발하세요 🌤️"
						else:
							morning_msg = "더운 하루가 예상돼요! 시원하게 보내세요 ☀️"
					except Exception:
						morning_msg = "오늘도 힘내세요!"
				else:
					morning_msg = "오늘도 힘내세요!"

				st.info(morning_msg)
				st.markdown(
					f"""
<style>
@media (max-width: 600px) {{
	.weather-card {{
		padding: 16px 4px !important;
		border-radius: 18px !important;
	}}
	.weather-title {{
		font-size: 22px !important;
		height: 48px !important;
		border-radius: 12px 12px 0 0 !important;
	}}
	.weather-row {{
		flex-direction: column !important;
		gap: 12px !important;
		padding-top: 12px !important;
	}}
	.weather-block {{
		max-width: 100% !important;
		padding: 12px !important;
	}}
	.weather-emoji {{
		font-size: 38px !important;
	}}
	.weather-label {{
		font-size: 16px !important;
	}}
	.weather-value {{
		font-size: 20px !important;
	}}
}}
</style>
<div class='weather-card' style='width:100%; min-width:200px; max-width:600px; margin:0 auto; background:#eaf6ff; border-radius:48px; box-shadow:0 4px 16px rgba(0,0,0,0.10); padding:32px 12px;'>
	<div class='weather-title' style='width:100%; height:60px; display:flex; align-items:center; justify-content:center; background:#1565c0; border-radius:18px 18px 0 0; margin-bottom:0;'>
		<span style='font-size:28px; font-weight:700; color:#fff;'>{today_str} {selected_subregion} 날씨</span>
	</div>
	<div class='weather-row' style='display:flex; justify-content:center; align-items:stretch; gap:18px; padding-top:18px; flex-wrap:wrap;'>
		<div class='weather-block' style='flex:1; min-width:120px; max-width:160px; background:#f7f7f7; border-radius:12px; padding:18px; text-align:center;'>
			<div class='weather-emoji' style='font-size:48px;'>{emoji}</div>
			<div class='weather-label' style='font-size:18px; margin-top:8px;'>날씨</div>
			<div class='weather-value' style='font-size:22px; margin-top:8px;'>{weather_desc}</div>
		</div>
		<div class='weather-block' style='flex:1; min-width:120px; max-width:160px; background:#f7f7f7; border-radius:12px; padding:18px; text-align:center;'>
			<div class='weather-emoji' style='font-size:48px;'>🌡️</div>
			<div class='weather-label' style='font-size:18px; margin-top:8px;'>온도</div>
			<div class='weather-value' style='font-size:22px; margin-top:8px;'>{temp}°C</div>
		</div>
		<div class='weather-block' style='flex:1; min-width:120px; max-width:160px; background:#f7f7f7; border-radius:12px; padding:18px; text-align:center;'>
			<div class='weather-emoji' style='font-size:48px;'>🌡️</div>
			<div class='weather-label' style='font-size:18px; margin-top:8px;'>체감온도</div>
			<div class='weather-value' style='font-size:22px; margin-top:8px;'>{feels_like}°C</div>
		</div>
		<div class='weather-block' style='flex:1; min-width:120px; max-width:160px; background:#f7f7f7; border-radius:12px; padding:18px; text-align:center;'>
			<div class='weather-emoji' style='font-size:48px;'>💧</div>
			<div class='weather-label' style='font-size:18px; margin-top:8px;'>습도</div>
			<div class='weather-value' style='font-size:22px; margin-top:8px;'>{humidity}%</div>
		</div>
		<div class='weather-block' style='flex:1; min-width:120px; max-width:160px; background:#e0f7fa; border-radius:14px; padding:18px; text-align:center;'>
			<div class='weather-emoji' style='font-size:54px;'>🌧️</div>
			<div class='weather-label' style='font-size:18px; margin-top:8px;'>강수량</div>
			<div class='weather-value' style='font-size:22px; margin-top:8px;'>{rain_amount}mm</div>
		</div>
	</div>
</div>
""",
					unsafe_allow_html=True)
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
					from collections import defaultdict
					day_dict = defaultdict(list)
					for item in forecast_data['list']:
						date_str = item['dt_txt'].split(' ')[0]
						desc = item['weather'][0]['description']
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
import os
import datetime
import streamlit as st
import pandas as pd
# Import feature modules
from region_map import region_map
from weather_api import fetch_weather, fetch_forecast
from clothes import get_clothes_recommendation, get_clothes_emoji
from ui_helpers import get_background_image, get_weather_emoji
