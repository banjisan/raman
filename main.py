import streamlit as st

# 페이지 제목 설정
st.title("🍜 나만의 라면꿀조합 추천기")
st.write("좋아하는 라면을 선택하시면 가장 잘 어울리는 조합을 추천해 드립니다!")

# 라면별 추천 조합 데이터 정의 (추가된 라면 목록)
noodle_db = {
    "신라면": {
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다."
    },
    "짜파게티": {
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 섞은 뒤 트러플 오일을 살짝 더하면 고급 스파게티 풍미를 느낄 수 있습니다."
    },
    "불닭볶음면": {
        "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
        "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다."
    },
    "너구리": {
        "combination": "다진 마늘 반 스푼 + 송송 썬 대파",
        "description": "오동통한 면발에 마늘과 대파의 알싸함이 더해져 해장에 제격인 깊고 시원한 국물이 완성됩니다."
    },
    "진라면 순한맛": {
        "combination": "우유 + 순후추",
        "description": "물 대신 우유를 넣고 후추를 뿌려 끓이면 부드럽고 고소한 크림 파스타 스타일로 변신합니다."
    },
    "팔도비빔면": {
        "combination": "골뱅이 + 대패삼겹살 + 오이 채",
        "description": "매콤달콤한 비빔면에 쫄깃한 골뱅이와 바삭하게 구운 삼겹살을 얹어 완벽한 야식 메뉴로 만듭니다."
    },
    "안성탕면": {
        "combination": "파김치 + 떡국떡",
        "description": "구수한 된장베이스 국물에 쫀득한 떡을 넣고 푹 익은 파김치를 싸 먹으면 깔끔한 감칠맛이 납니다."
    },
    "열라면": {
        "combination": "순두부 반 모 + 다진 마늘",
        "description": "화끈하게 매운 국물에 순두부를 넣어 부드러운 순두부찌개 느낌으로 즐길 수 있습니다."
    },
    "틈새라면": {
        "combination": "숙주나물 + 우삼겹",
        "description": "아삭한 숙주와 고소한 우삼겹을 더해 얼큰하고 시원한 일본식 카라라멘 느낌을 냅니다."
    },
    "삼양라면": {
        "combination": "비엔나 소시지 + 케찹 한 티스푼",
        "description": "특유의 햄 향이 나는 국물에 소시지를 넣으면 짭조름한 부대찌개 스타일로 업그레이드됩니다."
    }
}

# 셀렉트박스로 라면 선택
selected_noodle = st.selectbox(
    "어떤 라면을 끓이실 건가요?",
    options=list(noodle_db.keys())
)

st.divider()

# 선택한 라면에 맞는 조합 출력
if selected_noodle:
    info = noodle_db[selected_noodle]
    st.subheader(f"✨ {selected_noodle} 추천 조합")
    st.success(f"**추천 재료:** {info['combination']}")
    st.info(f"**맛 포인트:** {info['description']}")
