import streamlit as st

# 페이지 설정
st.set_page_config(page_title="라면 꿀조합 추천기", page_icon="🍜", layout="wide")

st.title("🍜 라면 꿀조합 추천기")
st.write("원하시는 라면 카드 아래 버튼을 누르면 추천 조합 상세 정보가 나타납니다.")

# 세션 상태 초기화 (클릭한 라면 기억)
if "selected_noodle" not in st.session_state:
    st.session_state.selected_noodle = None

# 라면 데이터베이스 (이미지 파일 경로 및 조합 데이터)
noodle_db = {
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=500",
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 면과 섞은 뒤, 트러플 오일을 몇 방울 떨어뜨리면 고급 파스타 풍미가 완성됩니다."
    },
    "신라면": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다."
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
    }
}

# 4열 그리드 상단 라면 카탈로그
cols = st.columns(len(noodle_db))
for idx, (noodle_name, data) in enumerate(noodle_db.items()):
    with cols[idx]:
        st.image(data["image"], caption=noodle_name, use_container_width=True)
        # 이미지 아래 버튼 생성
        if st.button(f"👉 {noodle_name} 선택", key=f"btn_{noodle_name}", use_container_width=True):
            st.session_state.selected_noodle = noodle_name

st.divider()

# 선택된 라면 조합 출력 영역
if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]
    
    st.subheader(f"✨ [{selected}] 꿀조합 상세보기")
    
    # 2열 분할: [왼쪽 1 : 오른쪽 2 비율]
    col_left, col_right = st.columns([1, 2])
    
    # 왼쪽: 라면 이미지
    with col_left:
        st.image(info["image"], caption=selected, use_container_width=True)
        
    # 오른쪽: 꿀조합 상세 설명
    with col_right:
        st.markdown(f"### 🍯 추천 조합")
        st.success(f"**필요한 재료:** {info['combination']}")
        
        st.markdown(f"### 💡 레시피 포인트")
        st.info(info['description'])
else:
    st.info("👆 위 라면 카탈로그에서 원하시는 라면의 버튼을 눌러보세요!")
