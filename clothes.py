# clothes.py
# 온도별 옷차림 추천 및 관련 함수

def get_clothes_recommendation(temp):
    if temp is None:
        return "정보 없음"
    if temp >= 28:
        return "민소매, 반팔, 반바지, 원피스"
    elif temp >= 23:
        return "반팔, 얇은 셔츠, 얇은 바지, 면바지"
    elif temp >= 20:
        return "긴팔, 얇은 가디건, 면바지"
    elif temp >= 17:
        return "얇은 니트, 맨투맨, 가디건, 청바지"
    elif temp >= 12:
        return "자켓, 가디건, 야상, 청바지, 면바지"
    elif temp >= 9:
        return "자켓, 트렌치코트, 야상, 니트, 청바지"
    elif temp >= 5:
        return "코트, 가죽자켓, 히트텍, 니트, 청바지"
    else:
        return "패딩, 두꺼운 코트, 목도리, 기모바지"

def get_clothes_emoji(recommendation):
    # 옷차림별 이모지 매핑
    if "패딩" in recommendation or "코트" in recommendation:
        return "🧥"
    elif "반팔" in recommendation or "민소매" in recommendation:
        return "👕"
    elif "니트" in recommendation or "가디건" in recommendation:
        return "🧶"
    elif "원피스" in recommendation:
        return "👗"
    elif "청바지" in recommendation or "바지" in recommendation:
        return "👖"
    else:
        return "👚"
