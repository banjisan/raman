import random
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="라면 꿀조합 추천기", page_icon="🍜", layout="wide"
)

st.title("🍜 라면 꿀조합 추천기")
st.write(
    "원하시는 라면 카드 아래 버튼을 누르면 추천 조합 상세 정보와 음성 안내가 제공됩니다."
)

# 세션 상태 초기화
if "selected_noodle" not in st.session_state:
    st.session_state.selected_noodle = None
if "speak_target" not in st.session_state:
    st.session_state.speak_target = None

# 라면 데이터베이스 (매운맛, 조리타입 속성 추가)
noodle_db = {
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800&auto=format&fit=crop&q=80",
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 면과 섞은 뒤, 트러플 오일을 몇 방울 떨어뜨리면 고급 파스타 풍미가 완성됩니다.",
        "spicy": "🌶️ (안 매움)",
        "type": "볶음/비빔",
        "timer": 300,
    },
    "신라면": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다.",
        "spicy": "🌶️🌶️ (보통)",
        "type": "국물",
        "timer": 270,
    },
    "불닭볶음면": {
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80",
        "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
        "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다.",
        "spicy": "🌶️🌶️🌶️🌶️ (아주 매움)",
        "type": "볶음/비빔",
        "timer": 300,
    },
    "튀김우동": {
        "image": "https://images.unsplash.com/photo-1618841557871-b468f3ade310?w=800&auto=format&fit=crop&q=80",
        "combination": "어묵 꼬치 + 쑥갓 + 고춧가루 약간",
        "description": "단짠 가쓰오부시 국물에 쫄깃한 어묵과 향긋한 쑥갓을 더하면 일식 우동 전문점 스타일로 업그레이드됩니다.",
        "spicy": "⚪ (순한맛)",
        "type": "국물",
        "timer": 240,
    },
}

# 🎲 [추가기능 1] 랜덤 뽑기 버튼
col_search, col_random = st.columns([3, 1])
with col_random:
    if st.button("🎲 오늘 뭐 먹지? (랜덤 추천)", use_container_width=True):
        random_choice = random.choice(list(noodle_db.keys()))
        st.session_state.selected_noodle = random_choice
        st.session_state.speak_target = random_choice

with col_search:
    search_query = st.text_input(
        "🔍 라면 이름 또는 재료를 검색해보세요!", "", label_visibility="collapsed"
    )

# 검색 및 카탈로그 출력
filtered_items = [
    (name, data)
    for name, data in noodle_db.items()
    if search_query.strip().lower() in name.lower()
    or search_query.strip().lower() in data["combination"].lower()
]

if filtered_items:
    cols_per_row = 4
    for i in range(0, len(filtered_items), cols_per_row):
        cols = st.columns(cols_per_row)
        chunk = filtered_items[i : i + cols_per_row]

        for idx, (noodle_name, data) in enumerate(chunk):
            with cols[idx]:
                st.image(
                    data["image"], caption=noodle_name, use_container_width=True
                )
                if st.button(
                    f"👉 {noodle_name} 선택",
                    key=f"btn_{noodle_name}",
                    use_container_width=True,
                ):
                    st.session_state.selected_noodle = noodle_name
                    st.session_state.speak_target = noodle_name

# TTS 음성 재생
if st.session_state.speak_target:
    target_name = st.session_state.speak_target
    tts_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance('{target_name}');
                utterance.lang = 'ko-KR';
                window.speechSynthesis.speak(utterance);
            }}
        </script>
    """
    components.html(tts_code, height=0)
    st.session_state.speak_target = None

st.divider()

# 상세 페이지
if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]

    st.subheader(f"✨ [{selected}] 꿀조합 상세보기")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.image(info["image"], caption=selected, use_container_width=True)

    with col_right:
        # [추가기능 2] 매운맛 정보 표시
        st.write(f"**🔥 맵기 단계:** {info.get('spicy', '정보 없음')}")
        st.markdown("### 🍯 추천 조합")
        st.success(f"**필요한 재료:** {info['combination']}")

        st.markdown("### 💡 레시피 포인트")
        st.info(info["description"])

        # [추가기능 3] 타이머 안내
        st.markdown(
            f"⏱️ **권장 조리 시간:** {info.get('timer', 240) // 60}분 {info.get('timer', 240) % 60}초"
        )

st.divider()

# [추가기능 4] 사용자 나만의 조합 제보 폼
with st.expander("➕ 나만의 꿀조합 제보하기"):
    with st.form("recipe_form"):
        user_noodle = st.text_input("라면 이름")
        user_ingredients = st.text_input("추천 재료")
        user_recipe = st.text_area("조리 팁")
        submitted = st.form_submit_button("제출하기")
        if submitted:
            st.success("감사합니다! 검토 후 라면 데이터베이스에 반영됩니다.")
