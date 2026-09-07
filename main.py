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
if "recipe_indexes" not in st.session_state:
    st.session_state.recipe_indexes = {}

if "votes" not in st.session_state:
    st.session_state.votes = {
        "짜파게티": 120,
        "신라면": 95,
        "불닭볶음면": 150,
        "너구리": 80,
        "진라면(매운맛)": 110,
        "안성탕면": 65,
        "틈새라면": 70,
        "팔도비빔면": 130,
        "신라면 블랙": 85,
        "열라면": 140,
        "튀김우동": 60,
        "육개장 사발면": 75,
        "삼양라면": 50,
        "오징어짬뽕": 55,
        "꼬꼬면": 45,
    }

noodle_db = {
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "트러플 오일 + 반숙 계란 후라이",
                "description": "반숙 노른자를 터뜨려 면과 섞은 뒤, 트러플 오일을 몇 방울 떨어뜨리면 고급 파스타 풍미가 완성됩니다.",
            },
            {
                "combination": "체다치즈 2장 + 고춧가루 약간",
                "description": "진한 치즈가 꾸덕함을 더해주고, 약간의 고춧가루가 느끼함을 잡아줍니다.",
            },
            {
                "combination": "파김치 + 파채",
                "description": "알싸한 파김치와 파채가 짜장의 단맛과 어우러져 완벽한 느끼함 제로 조합을 완성합니다.",
            },
        ],
        "spicy": "⚪ (안 매움)",
        "timer": "5분 00초",
    },
    "신라면": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "체다치즈 + 계란 노른자",
                "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다.",
            },
            {
                "combination": "우유 200ml + 청양고추",
                "description": "물 대신 우유를 넣어 끓이면 로제 파스타처럼 부드러우면서도 매콤한 신라면 투움바가 됩니다.",
            },
            {
                "combination": "숙주나물 + 차돌박이",
                "description": "아삭한 숙주와 차돌박이 기름이 국물에 베어 고급 짬뽕 느낌을 제공합니다.",
            },
        ],
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 30초",
    },
    "불닭볶음면": {
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
                "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다.",
            },
            {
                "combination": "삼각김밥 + 스트링치즈",
                "description": "남은 양념에 참치마요 삼각김밥과 스트링치즈를 넣어 비벼 먹는 최고의 마무리를 자랑합니다.",
            },
            {
                "combination": "마요네즈 1스푼 + 설탕 약간",
                "description": "고소하고 달콤한 마요네즈가 매운맛을 완화시켜 감칠맛을 폭발시킵니다.",
            },
        ],
        "spicy": "🌶️🌶️🌶️🌶️ (아주 매움)",
        "timer": "5분 00초",
    },
    "너구리": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "다진 마늘 반 스푼 + 송송 썬 대파",
                "description": "오동통한 면발에 마늘과 대파의 알싸함이 더해져 해장에 제격인 깊고 시원한 국물이 완성됩니다.",
            },
            {
                "combination": "짜파게티 1봉지 (짜파구리)",
                "description": "너구리의 매콤한 해물 맛과 짜파게티의 고소함이 섞인 입증된 꿀조합입니다.",
            },
        ],
        "spicy": "🌶️🌶️ (보통)",
        "timer": "5분 00초",
    },
    "진라면(매운맛)": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "순두부 반 모 + 후추 약간",
                "description": "SNS에서 대유행한 조합! 순두부를 넣고 끓여 매운맛은 순해지고 국물 맛은 훨씬 깊어집니다.",
            },
            {
                "combination": "식초 3방울 + 계란 풀기",
                "description": "불을 끄기 직전 식초 몇 방울을 넣으면 국물의 감칠맛이 살아나고 면발이 더 탱글해집니다.",
            },
        ],
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 00초",
    },
    "안성탕면": {
        "image": "https://images.unsplash.com/photo-1547928576-a4a33237cbc3?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "계란 푼 국물 + 밥 한 공기",
                "description": "구수한 된장 베이스 국물이라 계란을 살살 풀어 끓인 뒤, 국물에 밥을 말아먹을 때 진가를 발휘합니다.",
            },
            {
                "combination": "굴 한 움큼 + 무채",
                "description": "시원한 무채와 제철 굴을 더해주면 시원하고 깊은 해물탕 맛이 납니다.",
            },
        ],
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 30초",
    },
    "틈새라면": {
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "콩나물 한 움큼 + 떡사리",
                "description": "극강의 매운맛에 아삭한 콩나물 식감과 쫄깃한 떡을 추가하면 매운 짬뽕 스타일의 요리로 변신합니다.",
            }
        ],
        "spicy": "🌶️🌶️🌶️🌶️ (아주 매움)",
        "timer": "3분 30초",
    },
    "팔도비빔면": {
        "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTNExjSlIcPp-yPVjSF_h20fNib8-A_Nvc5_YXeL9Yhk8L7UfNuk49PJmjhxuLj336-5Wg_EROayB0zhVY",
        "combinations": [
            {
                "combination": "대패삼겹살(또는 골뱅이) + 오이채",
                "description": "매콤달콤한 비빔면 소스에 바삭하게 구운 대패삼겹살을 감싸 먹으면 조화가 완벽합니다.",
            },
            {
                "combination": "참기름 한 스푼 + 만두 튀김",
                "description": "바삭한 군만두와 매콤한 비빔면의 조합은 실패가 없는 별미입니다.",
            },
        ],
        "spicy": "🌶️ (약간 매움)",
        "timer": "3분 00초",
    },
    "신라면 블랙": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "모둠 버섯(표고/팽이) + 슬라이스 마늘",
                "description": "사골 국물 베이스 특유의 진한 풍미에 쫄깃한 버섯과 알싸한 마늘 향이 어우러져 깊은 맛을 냅니다.",
            }
        ],
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 30초",
    },
    "열라면": {
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "순두부 반 모 + 계란 노른자 + 후추 팍팍",
                "description": "원조 '열순두부' 조합! 화끈하고 칼칼한 국물에 순두부와 노른자가 더해져 최고의 얼큰함을 선사합니다.",
            }
        ],
        "spicy": "🌶️🌶️🌶️ (매움)",
        "timer": "4분 00초",
    },
    # 🖼️ [수정] 튀김우동 이미지 고화질 이미지 URL 적용
    "튀김우동": {
        "image": "https://images.unsplash.com/photo-1618841557871-b468f3ade310?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "어묵 꼬치 + 쑥갓 + 고춧가루 약간",
                "description": "가쓰오부시 우동 국물 맛을 일식 전문점 스타일로 업그레이드합니다.",
            },
            {
                "combination": "새우튀김 + 게살 크래미",
                "description": "바삭한 새우튀김과 게살을 얹어 더욱 푸짐한 모둠 튀김우동을 즐길 수 있습니다.",
            },
        ],
        "spicy": "⚪ (안 매움)",
        "timer": "4분 00초",
    },
    "육개장 사발면": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "단무지 + 얇게 썬 청양고추",
                "description": "얇고 쫄깃한 면발에 청양고추로 칼칼함을 살리고 새콤한 단무지와 함께 먹으면 추억의 맛을 느낄 수 있습니다.",
            }
        ],
        "spicy": "🌶️ (약간 매움)",
        "timer": "3분 00초",
    },
    "삼양라면": {
        "image": "https://images.unsplash.com/photo-1547928576-a4a33237cbc3?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "비엔나 소시지 + 케첩 한 티스푼",
                "description": "특유의 부대찌개풍 육수에 소시지를 넣으면 풍미가 향상되며 감칠맛 나는 국물이 완성됩니다.",
            }
        ],
        "spicy": "🌶️ (약간 매움)",
        "timer": "4분 30초",
    },
    "오징어짬뽕": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "냉동 오징어/새우 + 고추기름",
                "description": "해산물을 추가하고 마지막에 고추기름을 두르면 중화요리집 불향 가득한 짬뽕 국물이 완성됩니다.",
            }
        ],
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 30초",
    },
    "꼬꼬면": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=800&auto=format&fit=crop&q=80",
        "combinations": [
            {
                "combination": "닭가슴살 통조림 + 청양고추",
                "description": "담백한 닭육수에 찢은 닭가슴살과 청양고추를 더해 깊고 칼칼한 삼계탕 풍미를 선사합니다.",
            }
        ],
        "spicy": "🌶️🌶️ (보통)",
        "timer": "4분 00초",
    },
}

col_search, col_random = st.columns([3, 1])

with col_random:
    if st.button("🎲 오늘 뭐 먹지? (랜덤)", use_container_width=True):
        random_choice = random.choice(list(noodle_db.keys()))
        st.session_state.selected_noodle = random_choice
        st.session_state.speak_target = random_choice

        comb_count = len(noodle_db[random_choice]["combinations"])
        st.session_state.recipe_indexes[random_choice] = random.randint(
            0, comb_count - 1
        )

with col_search:
    search_query = st.text_input(
        "🔍 라면 이름 또는 재료를 검색해보세요!",
        "",
        label_visibility="collapsed",
        placeholder="🔍 라면 이름 또는 재료를 검색해보세요! (예: 치즈, 마늘, 비빔면)",
    )

tab1, tab2 = st.tabs(["🍜 전체 라면 목록", "🏆 명예의 전당 (꿀조합 랭킹)"])

with tab1:
    filtered_items = [
        (name, data)
        for name, data in noodle_db.items()
        if search_query.strip().lower() in name.lower()
        or any(
            search_query.strip().lower() in c["combination"].lower()
            for c in data["combinations"]
        )
    ]

    if filtered_items:
        cols_per_row = 4
        for i in range(0, len(filtered_items), cols_per_row):
            cols = st.columns(cols_per_row)
            chunk = filtered_items[i : i + cols_per_row]

            for idx, (noodle_name, data) in enumerate(chunk):
                with cols[idx]:
                    st.image(
                        data["image"],
                        caption=noodle_name,
                        use_container_width=True,
                    )
                    vote_count = st.session_state.votes.get(noodle_name, 0)
                    st.caption(f"👍 추천수: **{vote_count}**표")

                    col_btn1, col_btn2 = st.columns([2, 1])
                    with col_btn1:
                        if st.button(
                            f"👉 선택",
                            key=f"btn_{noodle_name}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_noodle = noodle_name
                            st.session_state.speak_target = noodle_name

                            curr_idx = st.session_state.recipe_indexes.get(
                                noodle_name, -1
                            )
                            comb_count = len(data["combinations"])
                            st.session_state.recipe_indexes[noodle_name] = (
                                curr_idx + 1
                            ) % comb_count
                            st.rerun()

                    with col_btn2:
                        if st.button("👍", key=f"vote_{noodle_name}"):
                            st.session_state.votes[noodle_name] += 1
                            st.rerun()
    else:
        st.warning("🔍 검색 결과가 없습니다.")

with tab2:
    st.subheader("🏆 명예의 전당 (사용자 인기 꿀조합 랭킹)")
    st.write("사용자들이 직접 투표한 인기 꿀조합 순위입니다.")

    sorted_votes = sorted(
        st.session_state.votes.items(), key=lambda x: x[1], reverse=True
    )

    for rank, (noodle_name, vote_count) in enumerate(sorted_votes, start=1):
        info = noodle_db[noodle_name]
        idx = st.session_state.recipe_indexes.get(noodle_name, 0)
        curr_comb = info["combinations"][idx % len(info["combinations"])]

        if rank == 1:
            rank_badge = "🥇 1위"
        elif rank == 2:
            rank_badge = "🥈 2위"
        elif rank == 3:
            rank_badge = "🥉 3위"
        else:
            rank_badge = f"**{rank}위**"

        with st.container():
            col_rank, col_img, col_info, col_vote = st.columns([1, 1.5, 4, 1.5])

            with col_rank:
                st.markdown(f"### {rank_badge}")

            with col_img:
                st.image(info["image"], use_container_width=True)

            with col_info:
                st.markdown(f"#### {noodle_name}")
                st.write(f"🍯 **대표 조합:** {curr_comb['combination']}")
                st.caption(f"💡 {curr_comb['description']}")

            with col_vote:
                st.metric("투표수", f"{vote_count}표")
                if st.button(
                    "👍 투표하기",
                    key=f"rank_vote_{noodle_name}",
                    use_container_width=True,
                ):
                    st.session_state.votes[noodle_name] += 1
                    st.rerun()

        st.divider()

if st.session_state.speak_target:
    target_name = st.session_state.speak_target
    tts_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const text = '{target_name} 추천 조합입니다.';
                const utterance = new SpeechSynthesisUtterance(text);
                
                const speakWithVoice = () => {{
                    const voices = window.speechSynthesis.getVoices();
                    const korVoice = voices.find(v => v.lang.includes('ko') && (v.name.includes('Google') || v.name.includes('Yuna') || v.name.includes('Natural') || v.name.includes('Neural'))) 
                                  || voices.find(v => v.lang.includes('ko'));
                    
                    if (korVoice) {{
                        utterance.voice = korVoice;
                    }}
                    
                    utterance.lang = 'ko-KR';
                    utterance.pitch = 1.0;
                    utterance.rate = 0.95;
                    
                    window.speechSynthesis.speak(utterance);
                }};

                if (window.speechSynthesis.getVoices().length !== 0) {{
                    speakWithVoice();
                }} else {{
                    window.speechSynthesis.onvoiceschanged = speakWithVoice;
                }}
            }}
        </script>
    """
    components.html(tts_code, height=0)
    st.session_state.speak_target = None

if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]

    idx = st.session_state.recipe_indexes.get(selected, 0)
    comb_list = info["combinations"]
    current_comb = comb_list[idx % len(comb_list)]

    st.subheader(f"✨ [{selected}] 꿀조합 상세보기")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.image(info["image"], caption=selected, use_container_width=True)

    with col_right:
        st.write(f"🔥 **맵기 단계:** {info.get('spicy', '정보 없음')}")
        st.write(f"⏱️ **권장 조리시간:** {info.get('timer', '정보 없음')}")
        st.write(
            f"👍 **현재 추천수:** {st.session_state.votes.get(selected, 0)}표"
        )

        st.markdown("### 🍯 추천 조합")
        st.success(f"**필요한 재료:** {current_comb['combination']}")

        st.markdown("### 💡 레시피 포인트")
        st.info(current_comb["description"])

        if len(comb_list) > 1:
            if st.button("🔀 다른 꿀조합 보기", key="change_recipe_btn"):
                st.session_state.recipe_indexes[selected] = (
                    idx + 1
                ) % len(comb_list)
                st.rerun()

st.divider()

with st.expander("➕ 나만의 꿀조합 제보하기"):
    with st.form("recipe_form"):
        user_noodle = st.text_input("라면 이름")
        user_ingredients = st.text_input("추천 재료")
        user_recipe = st.text_area("조리 팁")
        submitted = st.form_submit_button("제출하기")
        if submitted:
            st.success("감사합니다! 검토 후 데이터베이스에 반영하겠습니다.")
