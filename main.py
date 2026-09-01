<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>라면 이름 부르기</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 50px;
    }
    .ramen-btn {
      font-size: 18px;
      padding: 12px 24px;
      margin: 10px;
      cursor: pointer;
      border: none;
      border-radius: 8px;
      background-color: #ff6b6b;
      color: white;
      font-weight: bold;
      transition: transform 0.1s;
    }
    .ramen-btn:hover {
      background-color: #ee5253;
    }
    .ramen-btn:active {
      transform: scale(0.95);
    }
  </style>
</head>
<body>

  <h1>🍜 라면 이름을 눌러보세요!</h1>
  
  <!-- 라면 버튼 (틈새라면 제외) -->
  <button class="ramen-btn" onclick="speakRamen('신라면', 1.4, 1.3)">신라면</button>
  <button class="ramen-btn" onclick="speakRamen('진라면', 1.6, 0.9)">진라면</button>
  <button class="ramen-btn" onclick="speakRamen('너구리', 0.8, 1.4)">너구리</button>
  <button class="ramen-btn" onclick="speakRamen('안성탕면', 1.5, 1.1)">안성탕면</button>
  <button class="ramen-btn" onclick="speakRamen('짜파게티', 1.2, 1.5)">짜파게티</button>
  <button class="ramen-btn" onclick="speakRamen('불닭볶음면', 1.8, 1.2)">불닭볶음면</button>

  <script>
    function speakRamen(name, pitch, rate) {
      // 웹 브라우저 음성 합성 기능 지원 확인
      if ('speechSynthesis' in window) {
        // 기존에 재생 중인 음성이 있다면 중지
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(name);
        utterance.lang = 'ko-KR'; // 한국어 설정
        utterance.pitch = pitch;  // 음높이 (0.5 ~ 2, 높을수록 신나는 톤)
        utterance.rate = rate;    // 말하기 속도 (0.5 ~ 2, 높을수록 빠름)

        window.speechSynthesis.speak(utterance);
      } else {
        alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
      }
    }
  </script>

</body>
</html>
