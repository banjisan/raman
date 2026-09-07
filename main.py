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

# 라면 데이터베이스 (기존 8종 + 이전 추가 7종 = 총 15종 및 부가 정보 포함)
noodle_db = {
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800&auto=format&fit=crop&q=80",
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 면과 섞은 뒤, 트러플 오일을 몇 방울 떨어뜨리면 고급 파스타 풍미가 완성됩니다.",
        "spicy": "⚪ (안 매움)",
        "timer": "5분 00초",
    },
    "신라면": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다.",
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 30초",
    },
    "불닭볶음면": {
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80",
        "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
        "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다.",
        "spicy": "🌶️🌶️🌶️🌶️ (아주 매움)",
        "timer": "5분 00초",
    },
    "너구리": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&auto=format&fit=crop&q=80",
        "combination": "다진 마늘 반 스푼 + 송송 썬 대파",
        "description": "오동통한 면발에 마늘과 대파의 알싸함이 더해져 해장에 제격인 깊고 시원한 국물이 완성됩니다.",
        "spicy": "🌶️🌶️ (보통)",
        "timer": "5분 00초",
    },
    "진라면(매운맛)": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=800&auto=format&fit=crop&q=80",
        "combination": "순두부 반 모 + 후추 약간",
        "description": "SNS에서 대유행한 조합! 순두부를 넣고 끓여 매운맛은 순해지고 국물 맛은 훨씬 깊어집니다.",
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 00초",
    },
    "안성탕면": {
        "image": "https://images.unsplash.com/photo-1547928576-a4a33237cbc3?w=800&auto=format&fit=crop&q=80",
        "combination": "계란 푼 국물 + 밥 한 공기",
        "description": "구수한 된장 베이스 국물이라 계란을 살살 풀어 끓인 뒤, 국물에 밥을 말아먹을 때 진가를 발휘합니다.",
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 30초",
    },
    "틈새라면": {
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800&auto=format&fit=crop&q=80",
        "combination": "콩나물 한 움큼 + 떡사리",
        "description": "극강의 매운맛에 아삭한 콩나물 식감과 쫄깃한 떡을 추가하면 매운 짬뽕 스타일의 요리로 변신합니다.",
        "spicy": "🌶️🌶️🌶️🌶️ (아주 매움)",
        "timer": "3분 30초",
    },
    "팔도비빔면": {
        "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTNExjSlIcPp-yPVjSF_h20fNib8-A_Nvc5_YXeL9Yhk8L7UfNuk49PJmjhxuLj336-5Wg_EROayB0zhVY",
        "combination": "대패삼겹살(또는 골뱅이) + 오이채",
        "description": "매콤달콤한 비빔면 소스에 바삭하게 구운 대패삼겹살을 감싸 먹으면 조화가 완벽합니다.",
        "spicy": "🌶️ (약간 매움)",
        "timer": "3분 00초",
    },
    "신라면 블랙": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combination": "모둠 버섯(표고/팽이) + 슬라이스 마늘",
        "description": "사골 국물 베이스 특유의 진한 풍미에 쫄깃한 버섯과 알싸한 마늘 향이 어우러져 깊은 맛을 냅니다.",
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 30초",
    },
    "열라면": {
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800&auto=format&fit=crop&q=80",
        "combination": "순두부 반 모 + 계란 노른자 + 후추 팍팍",
        "description": "원조 '열순두부' 조합! 화끈하고 칼칼한 국물에 순두부와 노른자가 더해져 최고의 얼큰함을 선사합니다.",
        "spicy": "🌶️🌶️🌶️ (매움)",
        "timer": "4분 00초",
    },
    "튀김우동": {
        "image": "https://images.unsplash.com/photo-1618841557871-b468f3ade310?w=800&auto=format&fit=crop&q=80",
        "combination": "어묵 꼬치 + 쑥갓 + 고춧가루 약간",
        "description": "가쓰오부시 우동 국물 맛을 일식 전문점 스타일로 업그레이드합니다.",
        "spicy": "⚪ (안 매움)",
        "timer": "4분 00초",
    },
    "육개장 사발면": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&auto=format&fit=crop&q=80",
        "combination": "단무지 + 얇게 썬 청양고추",
        "description": "얇고 쫄깃한 면발에 청양고추로 칼칼함을 살리고 새콤한 단무지와 함께 먹으면 추억의 맛을 느낄 수 있습니다.",
        "spicy": "🌶️ (약간 매움)",
        "timer": "3분 00초",
    },
    "삼양라면": {
        "image": "https://images.unsplash.com/photo-1547928576-a4a33237cbc3?w=800&auto=format&fit=crop&q=80",
        "combination": "비엔나 소시지 + 케첩 한 티스푼",
        "description": "특유의 부대찌개풍 육수에 소시지를 넣으면 풍미가 향상되며 감칠맛 나는 국물이 완성됩니다.",
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 00초",
    },
    "오징어짬뽕": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combination": "냉동 오징어/새우 + 고추기름",
        "description": "해산물을 추가하고 마지막에 고추기름을 두르면 중화요리집 불향 가득한 짬뽕 국물이 완성됩니다.",
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 30초",
    },
    "꼬꼬면": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=800&auto=format&fit=crop&q=80",
        "combination": "닭가슴살 통조림 + 청양고추",
        "description": "담백한 닭육수에 찢은 닭가슴살과 청양고추를 더해 깊고 칼칼한 삼계탕 풍미를 선사합니다.",
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 00초",
    },
}

# 🔍 상단 검색 및 🎲 오늘 뭐 먹지? 기능
col_search, col_random = st.columns([3, 1])

with col_random:
    if st.button("🎲 오늘 뭐 먹지? (랜덤)", use_container_width=True):
        random_choice = random.choice(list(noodle_db.keys()))
        st.session_state.selected_noodle = random_choice
        st.session_state.speak_target = random_choice

with col_search:
    search_query = st.text_input(
        "🔍 라면 이름 또는 재료를 검색해보세요!",
        "",
        label_visibility="collapsed",
        placeholder="🔍 라면 이름 또는 재료를 검색해보세요! (예: 치즈, 마늘, 비빔면)",
    )

# 검색어에 따른 필터링
filtered_items = [
    (name, data)
    for name, data in noodle_db.items()
    if search_query.strip().lower() in name.lower()
    or search_query.strip().lower() in data["combination"].lower()
]

# 카탈로그 출력 (4열)
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
else:
    st.warning(
        "🔍 검색 결과가 없습니다. 다른 라면 이름이나 재료를 검색해보세요!"
    )

# 브라우저 Web Speech API를 활용한 음성 재생
if st.session_state.speak_target:
    target_name = st.session_state.speak_target
    tts_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance('{target_name}');
                utterance.lang = 'ko-KR';
                utterance.pitch = 1.4;
                utterance.rate = 1.2;
                window.speechSynthesis.speak(utterance);
            }}
        </script>
    """
    components.html(tts_code, height=0)
    st.session_state.speak_target = None

st.divider()

# 선택된 라면 상세 보기
if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]

    st.subheader(f"✨ [{selected}] 꿀조합 상세보기")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.image(info["image"], caption=selected, use_container_width=True)

    with col_right:
        st.write(f"🔥 **맵기 단계:** {info.get('spicy', '정보 없음')}")
        st.write(f"⏱️ **권장 조리시간:** {info.get('timer', '정보 없음')}")

        st.markdown("### 🍯 추천 조합")
        st.success(f"**필요한 재료:** {info['combination']}")

        st.markdown("### 💡 레시피 포인트")
        st.info(info["description"])
else:
    st.info("👆 위 라면 카탈로그에서 원하시는 라면의 버튼을 눌러보세요!")

st.divider()

# 나만의 꿀조합 제보 폼
with st.expander("➕ 나만의 꿀조합 제보하기"):
    with st.form("recipe_form"):
        user_noodle = st.text_input("라면 이름")
        user_ingredients = st.text_input("추천 재료")
        user_recipe = st.text_area("조리 팁")
        submitted = st.form_submit_button("제출하기")
        if submitted:
            st.success("감사합니다! 검토 후 데이터베이스에 반영하겠습니다.")
