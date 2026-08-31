import streamlit as st

# 페이지 제목 설정
st.title("🍜 나만의 라면꿀조합 추천기")
st.write("좋아하는 라면을 선택하시면 가장 잘 어울리는 조합을 추천해 드립니다!")

# 라면별 추천 조합 데이터 정의
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
