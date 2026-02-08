import json
import os
import time
from email_template import generate_email_html

# User's Request Content (Monday Motivation)
data = {
    "title": "Monday Motivation (월요일의 리더십)",
    "intro": "한 주의 시작인 월요일, 업무와 학업의 무게가 무겁게 느껴지시나요? 오늘은 최악의 상황을 최고의 기회로 바꾼 리더, 헨리 5세의 목소리를 빌려 당신을 응원합니다.",
    "quote": {
        "text": "We few, we happy few, we band of brothers...",
        "translation": "우리는 소수다, 행복한 소수다, 우리는 형제들이다. 오늘 나와 함께 피를 흘리는 자는 나의 형제가 될 것이다.",
        "source": "헨리 5세 (Henry V), Act 4, Scene 3"
    },
    "insight": {
        "context": "아쟁쿠르 전투 직전, 잉글랜드 군은 프랑스 대군에 비해 수적으로 절대적인 열세였습니다. 병사들은 지쳤고 두려움에 떨고 있었죠.",
        "interpretation": "그때 헨리 5세는 상황을 완전히 재정의합니다. 그는 병사가 적은 것을 '불리함'이 아니라 '영광을 나눠 가질 사람이 적으니 더 큰 영광'이라고 말합니다.",
        "action": "이번 주, 감당하기 힘든 프로젝트나 과제 앞에 서 계신가요? '너무 힘들다'고 생각하는 대신, 이 힘든 일을 해냈을 때 얻게 될 '나만의 스토리'를 상상해 보세요."
    },
    "second_perspective": {
        "title": "🏛 또 다른 리더의 시선: 브루투스 (Julius Caesar)",
        "content": "성공만이 리더십의 전부는 아닙니다. 줄리어스 시저의 브루투스는 '한쪽 눈에는 명예를, 다른 쪽 눈에는 죽음을 놓아두시오'라고 말하며, 혼란 속에서도 신념을 지키는 내면의 힘을 보여줍니다."
    },
    "weekly_preview": [
        "화요일 (Tuesday Romance): 로미오와 줄리엣이 말하는 사랑의 맹세",
        "수요일 (Witty Wednesday): 헛소동 속 베네딕과 베아트리스의 유쾌한 설전",
        "목요일 (Thoughtful Thursday): 햄릿과 함께하는 존재론적 고민",
        "금요일 (Furious Friday): 리어왕이 선사하는 속 시원한 풍자"
    ],
    "meta": {
        "date": "2026-10-26",
        "theme": "Monday Motivation"
    }
}

# 1. Update JSON
json_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_issue.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("✅ JSON Updated with Demo Data")

# 2. Update Email HTML
html_body = generate_email_html(data)
html_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_email.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_body)
print(f"✅ Email HTML Generated at {html_path}")
