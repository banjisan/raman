import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="라면 꿀조합 추천기", page_icon="🍜", layout="wide")

st.title("🍜 라면 꿀조합 추천기")
st.write("원하시는 라면 카드 아래 버튼을 누르면 추천 조합 상세 정보와 음성 안내가 제공됩니다.")

# 세션 상태 초기화
if "selected_noodle" not in st.session_state:
    st.session_state.selected_noodle = None
if "speak_target" not in st.session_state:
    st.session_state.speak_target = None

# 라면 데이터베이스 (짜파게티: 짜장 볶음라면 이미지 반영)
noodle_db = {
    "짜파게티": {
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&auto=format&fit=crop&q=80",
        "combination": "트러플 오일 + 반숙 계란 후라이",
        "description": "반숙 노른자를 터뜨려 면과 섞은 뒤, 트러플 오일을 몇 방울 떨어뜨리면 고급 파스타 풍미가 완성됩니다."
    },
    "신라면": {
        "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800&auto=format&fit=crop&q=80",
        "combination": "체다치즈 + 계란 노른자",
        "description": "매콤한 국물에 치즈가 녹아들어 부드럽고 녹진해지며, 계란 노른자로 고소함이 더해집니다."
    },
    "불닭볶음면": {
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80",
        "combination": "콘치즈 (옥수수콘 + 모짜렐라 치즈)",
        "description": "톡톡 터지는 옥수수 식감과 고소한 모짜렐라가 불닭의 강렬한 매운맛을 달콤하게 잡아줍니다."
    },
    "너구리": {
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&auto=format&fit=crop&q=80",
        "combination": "다진 마늘 반 스푼 + 송송 썬 대파",
        "description": "오동통한 면발에 마늘과 대파의 알싸함이 더해져 해장에 제격인 깊고 시원한 국물이 완성됩니다."
    },
    "진라면(매운맛)": {
        "image": "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=800&auto=format&fit=crop&q=80",
        "combination": "순두부 반 모 + 후추 약간",
        "description": "SNS에서 대유행한 조합! 순두부를 넣고 끓여 매운맛은 순해지고 국물 맛은 훨씬 깊어집니다."
    },
    "안성탕면": {
        "image": "https://images.unsplash.com/photo-1547928576-a4a33237cbc3?w=800&auto=format&fit=crop&q=80",
        "combination": "계란 푼 국물 + 밥 한 공기",
        "description": "구수한 된장 베이스 국물이라 계란을 살살 풀어 끓인 뒤, 국물에 밥을 말아먹을 때 진가를 발휘합니다."
    },
    "틈새라면": {
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800&auto=format&fit=crop&q=80",
        "combination": "콩나물 한 움큼 + 떡사리",
        "description": "극강의 매운맛에 아삭한 콩나물 식감과 쫄깃한 떡을 추가하면 매운 짬뽕 스타일의 요리로 변신합니다."
    },
    "팔도비빔면": {
        "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTNExjSlIcPp-yPVjSF_h20fNib8-A_Nvc5_YXeL9Yhk8L7UfNuk49PJmjhxuLj336-5Wg_EROayB0zhVY",
        "combination": "대패삼겹살(또는 골뱅이) + 오이채",
        "description": "매콤달콤한 비빔면 소스에 바삭하게 구운 대패삼겹살을 감싸 먹으면 조화가 완벽합니다."
    }
}

# 라면 카탈로그 출력 (4열 그리드)
items = list(noodle_db.items())
cols_per_row = 4

for i in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    chunk = items[i:i + cols_per_row]
    
    for idx, (noodle_name, data) in enumerate(chunk):
        with cols[idx]:
            st.image(data["image"], caption=noodle_name, use_container_width=True)
            if st.button(f"👉 {noodle_name} 선택", key=f"btn_{noodle_name}", use_container_width=True):
                st.session_state.selected_noodle = noodle_name
                st.session_state.speak_target = noodle_name

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

# 선택된 라면 정보 및 상세 레시피 표시
if st.session_state.selected_noodle:
    selected = st.session_state.selected_noodle
    info = noodle_db[selected]
    
    st.subheader(f"✨ [{selected}] 꿀조합 상세보기")
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.image(info["image"], caption=selected, use_container_width=True)
        
    with col_right:
        st.markdown("### 🍯 추천 조합")
        st.success(f"**필요한 재료:** {info['combination']}")
        
        st.markdown("### 💡 레시피 포인트")
        st.info(info['description'])
else:
    st.info("👆 위 라면 카탈로그에서 원하시는 라면의 버튼을 눌러보세요!")
