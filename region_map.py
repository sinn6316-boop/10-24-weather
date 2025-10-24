# region_map.py
# 전국 지역/도시 데이터 모듈

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
