import json
import os
import time
from email_template import generate_email_html

# Manual Content for Sunday
data = {
    "meta": {
        "date": "2026-02-08",
        "theme": "Sunday Reflection (일요일의 사색)",
        "generated_at": time.time()
    },
    "main_quote": "We are such stuff As dreams are made on, and our little life Is rounded with a sleep.\n(우리는 꿈과 같은 존재이며, 우리의 짧은 인생은 잠으로 끝나는구나.)",
    "source": "The Tempest (폭풍우), Prospero",
    "insight": "프로스페로는 마법의 힘을 내려놓으며 인생의 덧없음을 이야기합니다. 우리가 집착하는 모든 부귀영화와 갈등도 결국 꿈처럼 사라질 것임을 깨닫는 순간, 마음의 평화가 찾아옵니다. 한 주 동안 쌓인 걱정과 스트레스를 '꿈'이라고 생각하고 흘려보내세요.",
    "second_act": "맥베스 역시 '인생은 걸어 다니는 그림자'라고 말했지만, 그의 어조는 허무와 절망에 가깝습니다. 반면 프로스페로의 독백은 '수용'과 '화해'를 담고 있습니다. 같은 허무함이라도 그것을 받아들이는 태도에 따라 삶의 온도가 달라집니다.",
    "weekly_preview": "월요일에는 헨리 5세와 함께 '위기를 기회로 바꾸는 리더십'을 탐구합니다."
}

# 1. Update JSON
json_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_issue.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("✅ JSON Updated")

# 2. Update Email HTML
html_body = generate_email_html(data)
html_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_email.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_body)
print("✅ Email HTML Generated")
