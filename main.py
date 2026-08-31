import streamlit as st

# 페이지 설정
st.set_page_config(page_title="라면 꿀조합 추천기", page_icon="🍜", layout="wide")

st.title("🍜 라면 꿀조합 추천기")
st.write("원하시는 라면 이미지 아래 **[조합 보기]** 버튼을 누르면 추천 조합을 알려드립니다!")

# 세션 상태 초기화 (클릭한 라면 정보 저장)
if "selected_noodle" not in st.session_state:
    st.session_state.selected_noodle = None

# 라면 데이터베이스 (이미지 URL 및 조합 정보)
# ※ 온라인 이미지 URL 대신 'images/shin.jpg'와 같은 프로젝트 내 파일 경로를 직접 넣으셔도 됩니다.
noodle_db = {
    "신라면": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다."
    },
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=500",
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 섞은 뒤 트러플 오일을 살짝 더하면 고급 스파게티 풍미를 느낄 수 있습니다."
    },
    "불닭볶음면": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=500",
        "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
        "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다."
    },
    "너구리": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=500",
        "combination": "다진 마늘 반 스푼 + 송송 썬 대파",
        "description": "오동통한 면발에 마늘과 대파의 알싸함이 더해져 해장에 제격인 깊고 시원한 국물이 완성됩니다."
    },
    "진라면 순한맛": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
        "combination": "우유 + 순후추",
        "description": "물 대신 우유를 넣고 후추를 뿌려 끓이면 부드럽고 고소한 크림 파스타 스타일로 변신합니다."
    },
    "팔도비빔면": {
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500",
        "combination": "골뱅이 + 대패삼겹살 + 오이 채",
        "description": "매콤달콤한 비빔면에 쫄깃한 골뱅이와 바삭하게 구운 삼겹살을 얹어 완벽한 야식 메뉴로 만듭니다."
    },
    "열라면": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=500",
        "combination": "순두부 반 모 + 다진 마늘",
        "description": "화끈하게 매운 국물에 순두부를 넣어 부드러운 순두부찌개 느낌으로 즐길 수 있습니다."
    },
    "틈새라면": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=500",
        "combination": "숙주나물 + 우삼겹",
        "description": "아삭한 숙주와 고소한 우삼겹을 더해 얼큰하고 시원한 일본식 카라라멘 느낌을 냅니다."
    }
}

# 4열 그리드 배치
cols = st.columns(4)
noodle_list = list(noodle_db.keys())

for idx, noodle_name in enumerate(noodle_list):
    col = cols[idx % 4]
    with col:
        # 라면 이미지 출력
        st.image(noodle_db[noodle_name]["image"], caption=noodle_name, use_container_width=True)
        # 이미지 아래 클릭 버튼
        if st.button(f"👉 {noodle_name} 조합 보기", key=f"btn_{noodle_name}", use_container_width=True):
            st.session_state.selected_noodle = noodle_name

st.divider()

# 선택된 라면 조합 상세 보기
if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]
    
    st.subheader(f"✨ [{selected}] 추천 꿀조합")
    
    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(info["image"], use_container_width=True)
    with col_info:
        st.success(f"**추천 재료:** {info['combination']}")
        st.info(f"**맛 포인트:** {info['description']}")
else:
    st.info("👆 위 라면 카드에서 원하시는 라면의 버튼을 선택해 보세요!")
