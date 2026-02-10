import asyncio
import json
import uuid
import sys
import os
import time
from datetime import datetime

# Shakespeare Notebook ID
NOTEBOOK_ID = "19bde485-a9c1-4809-8884-e872b2b67b44"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../src/data/latest_issue.json")

# Daily Themes Configuration
THEMES = {
    0: { # Monday
        "name": "Monday Motivation (리더십과 동기부여)",
        "focus": "Henry V, Julius Caesar, Leadership, Courage",
        "description": "한 주를 시작하는 힘찬 에너지나 리더십에 관한 통찰. 불가능을 극복하는 용기."
    },
    1: { # Tuesday
        "name": "Tuesday Romance (사랑과 낭만)",
        "focus": "Sonnets, Romeo and Juliet, As You Like It, Love",
        "description": "아름다운 소네트나 연극 속 로맨틱한 대사. 사랑의 기쁨과 슬픔, 불변성."
    },
    2: { # Wednesday
        "name": "Witty Wednesday (위트와 해학)",
        "focus": "Falstaff (Henry IV), Much Ado About Nothing, Midsummer Night's Dream, Humor",
        "description": "재치 있는 말장난, 해학적인 캐릭터, 삶을 관조하는 유머와 농담."
    },
    3: { # Thursday
        "name": "Thoughtful Thursday (인생과 철학)",
        "focus": "Hamlet, Macbeth, The Tempest, Life and Death",
        "description": "삶, 죽음, 운명, 존재론적 고민에 대한 깊은 사색과 독백."
    },
    4: { # Friday
        "name": "Furious Friday (풍자와 카타르시스)",
        "focus": "King Lear, Troilus and Cressida, Timon of Athens, Satire, Curse",
        "description": "세상의 부조리에 대한 신랄한 비판, 창의적인 욕설, 속 시원한 풍자."
    },
    5: { # Saturday (Fallback to Wit)
        "name": "Weekend Wit (주말의 위트)",
        "focus": "Comedy of Errors, Twelfth Night",
        "description": "주말을 즐겁게 하는 가벼운 희극과 유머."
    },
    6: { # Sunday (Fallback to Philosophy)
        "name": "Sunday Reflection (일요일의 사색)",
        "focus": "The Tempest, Sonnets",
        "description": "한 주를 마무리하며 평온을 찾는 지혜."
    }
}

async def generate_issue():
    # Determine Theme based on current day (KST)
    from datetime import timedelta
    kst_now = datetime.utcnow() + timedelta(hours=9)
    weekday = kst_now.weekday()
    theme = THEMES.get(weekday, THEMES[0])
    
    # 1. Cloud-Specific Logic: Force Fallback in GitHub Actions
    # (Since NotebookLM auth isn't available in ephemeral CI runners)
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("🤖 [Gen] Detected GitHub Actions environment.")
        print("⚠️ [Gen] Skipping AI generation (no auth). Using High-Quality Fallback.")
        return create_fallback_issue(theme)

    # Use 'uv' from PATH based on OS
    uv_path = "uv" # In GitHub Actions, uv is installed to PATH
    
    print(f"Generate Issue for {theme['name']}...")

    try:
        cmd = [uv_path, "tool", "run", "--from", "notebooklm-mcp-server", "notebooklm-mcp"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    except FileNotFoundError:
        print("⚠️ 'uv' command not found. Using fallback content.")
        return create_fallback_issue(theme)

    async def read_response():
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line_str = line.decode().strip()
                if not line_str:
                    continue
                if not line_str.startswith('{'):
                    continue
                return json.loads(line_str)
        except Exception:
            return None

    async def send_request(method, params=None):
        req_id = str(uuid.uuid4())
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method
        }
        if params is not None:
            req["params"] = params
        
        msg = json.dumps(req) + "\n"
        process.stdin.write(msg.encode())
        await process.stdin.drain()
        return req_id

    try:
        # Initialize (might fail if auth is required and not present)
        # In cloud, this interaction is risky without stored credentials.
        # We will wrap this in a timeout/try block.
        print("   [Gen] Initializing MCP...")
        init_id = await send_request("notifications/initialized")
        
        # ... logic continues ...
        # Initialize
        init_id = await send_request("initialize", {
            "clientInfo": {"name": "kodari-generator", "version": "1.0"},
            "protocolVersion": "2024-11-05", 
            "capabilities": {}
        })

        while True:
            resp = await read_response()
            if resp and resp.get("id") == init_id:
                break
        
        await send_request("notifications/initialized")
        
        prompt = f"""
        당신은 'The Daily Bard'라는 셰익스피어 뉴스레터의 전문 에디터입니다.
        아래의 요일별 테마와 구조에 맞춰, 독자에게 깊은 울림을 주는 뉴스레터를 작성해주세요.

        [오늘의 테마: {theme['name']}]
        참고 작품/키워드: {theme['focus']}
        설명: {theme['description']}

        [작성 구조 (반드시 이 순서와 내용을 지킬 것)]
        1. **Header (도입부)**:
           - 독자의 감정을 터치하는 짧은 인사말.
           - 오늘 테마를 소개하며 독자의 호기심 자극.
        2. **Quote of the Day (오늘의 명대사)**:
           - 영어 원문과 한국어 번역 병기.
           - 출처 (작품명, 화자) 명시.
        3. **The Insight (통찰)**:
           - [Context]: 대사의 문학적/상황적 배경 설명.
           - [Reinterpretation]: 이를 현대적 관점에서 재해석.
           - [Application]: 독자가 이번 주에 당장 실천할 수 있는 구체적인 행동 제안.
        4. **Another Perspective (또 다른 시선)**:
           - 메인 테마와 연결되지만 다른 관점을 가진 셰익스피어의 다른 캐릭터나 대사 소개.
        5. **Weekly Preview (이번 주 예고)**:
           - 남은 요일들의 테마를 매력적으로 예고.

        [필수 응답 형식]
        반드시 아래의 JSON 포맷으로만 응답해야 합니다. 마크다운이나 추가 설명 금지.
        {{
            "title": "{theme['name']}",
            "intro": "도입부 텍스트...",
            "quote": {{
                "text": "English Quote...",
                "translation": "한국어 번역...",
                "source": "작품명, 화자"
            }},
            "insight": {{
                "context": "문학적 배경...",
                "interpretation": "현대적 재해석...",
                "action": "실천 가이드..."
            }},
            "second_perspective": {{
                "title": "캐릭터/주제",
                "content": "내용..."
            }},
            "weekly_preview": [
                "화요일: ...",
                "수요일: ..."
            ]
        }}
        """

        req_id = await send_request("tools/call", {
            "name": "notebook_query",
            "arguments": {
                "notebook_id": NOTEBOOK_ID,
                "query": prompt
            }
        })

        # Wait for response (Timeout set to 15 seconds to trigger fallback quickly if stuck)
        start_wait = time.time()
        while True:
            # If generating takes > 60s, we might get a TimeoutError from wait_for.
            # But here we just check in the loop.
            try:
                resp = await asyncio.wait_for(read_response(), timeout=60.0)
            except asyncio.TimeoutError:
                raise Exception("Generation timed out")

            if resp is None:
                raise Exception("Subprocess exited unexpectedly during generation")

            if resp.get("id") == req_id:
                if "error" in resp:
                    print(json.dumps({"error": resp['error']}))
                else:
                    content = resp.get("result", {}).get("content", [])
                    found_json = False
                    for item in content:
                        if item.get("type") == "text":
                            raw_text = item["text"]
                            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
                            try:
                                data = json.loads(clean_text)
                                
                                # Handle nested JSON in 'answer'
                                if "answer" in data and isinstance(data["answer"], str):
                                    try:
                                        nested = json.loads(data["answer"])
                                        data = nested
                                    except:
                                        pass

                                # Enrich data
                                data["meta"] = {
                                    "date": datetime.now().strftime("%Y-%m-%d"),
                                    "theme": theme['name'],
                                    "generated_at": time.time()
                                }
                                
                                os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
                                
                                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                
                                print(json.dumps(data, ensure_ascii=False))
                                found_json = True
                            except json.JSONDecodeError:
                                print(json.dumps({"error": "Invalid JSON", "raw": raw_text}, ensure_ascii=False))
                    
                    if not found_json:
                         print(json.dumps({"error": "No text content found"}))
                         return create_fallback_issue(theme)
                break

    except Exception as e:
        print(f"❌ [Gen] Generation failed (using fallback): {str(e)}")
        return create_fallback_issue(theme)
    finally:
        try:
            process.terminate()
            await process.wait()
        except:
            pass

    return fallback_data


# --- 7-Day Masterpiece Anthology (Fallback Library) ---
FALLBACK_LIBRARY = {
    0: { # Monday: Leadership (Henry V)
        "title": "Monday Motivation (리더십과 동기부여)",
        "intro": "한 주의 시작, 위대한 왕의 목소리로 꺠어납시다.",
        "quote": {
            "text": "We few, we happy few, we band of brothers; For he to-day that sheds his blood with me Shall be my brother.",
            "translation": "우리는 소수다, 행복한 소수다, 우리는 형제들이다. 오늘 나와 함께 피를 흘리는 자는 나의 형제가 될 것이다.",
            "source": "Henry V, Act 4, Scene 3"
        },
        "insight": {
            "context": "수적 열세에 처한 아쟁쿠르 전투 직전, 헨리 5세가 지친 병사들에게 전하는 전설적인 연설입니다.",
            "interpretation": "고난은 불행이 아니라, 훗날 전설로 남을 '소수만이 누리는 특권'입니다. 함께 고생하는 동료야말로 진정한 형제입니다.",
            "action": "이번 주, 힘든 프로젝트를 '나만의 전설을 쓸 기회'로 재정의하고 팀원들을 격려해보세요."
        },
        "second_perspective": {
            "title": "Brutus (Julius Caesar)",
            "content": "성공보다 원칙을 중시한 리더, 브루투스. '나는 명예와 죽음을 똑같이 바라보리라'는 그의 결의를 기억하세요."
        },
        "weekly_preview": ["화요일: 로미오와 줄리엣의 낭만 (Romance)", "수요일: 베네딕의 위트 (Wit)"]
    },
    1: { # Tuesday: Romance (Romeo & Juliet)
        "title": "Tuesday Romance (사랑과 낭만)",
        "intro": "화요일, 셰익스피어가 노래하는 영원한 사랑의 언어에 빠져보세요.",
        "quote": {
            "text": "My bounty is as boundless as the sea, My love as deep; the more I give to thee, The more I have, for both are infinite.",
            "translation": "내 관대함은 바다처럼 끝이 없고, 내 사랑은 바다만큼 깊어라. 당신에게 주면 줄수록 나에겐 더 많이 생겨나니, 둘 다 무한하기 때문이라.",
            "source": "Romeo and Juliet, Act 2, Scene 2"
        },
        "insight": {
            "context": "줄리엣이 로미오에게 자신의 사랑을 고백하는 발코니 장면의 절정입니다.",
            "interpretation": "진정한 사랑(혹은 열정)은 퍼내도 마르지 않는 샘물과 같습니다. 계산하지 않고 전부를 던질 때, 우리는 더 큰 에너지로 채워집니다.",
            "action": "오늘 하루, 사랑하는 사람이나 몰입하는 일에 아낌없이, 계산 없이 마음을 쏟아보세요."
        },
        "second_perspective": {
            "title": "Orsino (Twelfth Night)",
            "content": "사랑이 음악이라면, 계속 연주하라! (If music be the food of love, play on!) 짝사랑조차 예술로 승화시킨 공작의 열정."
        },
        "weekly_preview": ["수요일: 한여름 밤의 위트", "목요일: 햄릿의 사색"]
    },
    2: { # Wednesday: Wit (Much Ado About Nothing)
        "title": "Witty Wednesday (위트와 해학)",
        "intro": "일주일의 중간, 웃음과 재치로 지친 마음을 환기시키세요.",
        "quote": {
            "text": "I had rather hear my dog bark at a crow than a man swear he loves me.",
            "translation": "남자가 내게 사랑을 맹세하는 꼴을 보느니, 차라리 까마귀를 보고 짖어대는 내 개 소리를 듣겠어.",
            "source": "Much Ado About Nothing, Beatrice"
        },
        "insight": {
            "context": "독신주의자 베아트리스가 베네딕과의 설전에서 내뱉는 촌철살인의 대사입니다.",
            "interpretation": "뻔한 칭찬이나 가식적인 고백보다, 시끄럽더라도 '진실한 개 짖는 소리'가 낫다는 통쾌한 일갈입니다. 솔직함이 최고의 위트입니다.",
            "action": "오늘은 복잡한 격식 대신, 있는 그대로의 솔직한 농담으로 주변 분위기를 밝혀보세요."
        },
        "second_perspective": {
            "title": "Puck (Midsummer Night's Dream)",
            "content": "인간들이란 참 어리석기도 하지! (Lord, what fools these mortals be!) 숲속의 요정이 인간사를 보며 던지는 장난스런 조롱."
        },
        "weekly_preview": ["목요일: 삶과 죽음의 철학", "금요일: 리어왕의 분노"]
    },
    3: { # Thursday: Thought (Hamlet)
        "title": "Thoughtful Thursday (인생과 철학)",
        "intro": "목요일, 깊은 사색을 통해 삶의 의미를 되물어봅니다.",
        "quote": {
            "text": "There is nothing either good or bad, but thinking makes it so.",
            "translation": "세상에 좋고 나쁜 것은 없다. 다만 생각이 그렇게 만들 뿐이다.",
            "source": "Hamlet, Act 2, Scene 2"
        },
        "insight": {
            "context": "햄릿이 덴마크를 '감옥'이라고 부르며 로젠크란츠에게 전하는 말입니다.",
            "interpretation": "상황 그 자체보다 중요한 것은 그것을 바라보는 우리의 '관점'입니다. 감옥도 왕국도 모두 마음먹기에 달려 있다는 극기(克己)의 철학입니다.",
            "action": "오늘 닥친 문제(Problem)를 도전(Challenge)이라는 단어로 바꿔 생각해보세요. 세상이 다르게 보일 수 있습니다."
        },
        "second_perspective": {
            "title": "Prospero (The Tempest)",
            "content": "우리는 꿈과 같은 존재이며, 우리의 짧은 인생은 잠으로 둘러싸여 있다. (We are such stuff as dreams are made on...)"
        },
        "weekly_preview": ["금요일: 세상을 향한 풍자", "주말: 희극과 휴식"]
    },
    4: { # Friday: Furious/Satire (King Lear)
        "title": "Furious Friday (풍자와 카타르시스)",
        "intro": "금요일, 세상을 향한 날카로운 외침으로 스트레스를 날려버리세요.",
        "quote": {
            "text": "When we are born, we cry that we are come To this great stage of fools.",
            "translation": "우리가 태어날 때 우는 것은, 이 거대한 광대들의 무대에 나온 것이 슬퍼서이다.",
            "source": "King Lear, Act 4, Scene 6"
        },
        "insight": {
            "context": "모든 것을 잃고 미쳐버린 리어왕이 인간 세상의 부조리함을 꿰뚫어보며 하는 통탄의 말입니다.",
            "interpretation": "세상이 마치 바보들의 연극 같다는 지적. 하지만 역설적으로, 그렇기에 우리는 이 연극을 너무 심각하게 받아들이지 말고 '주인공'으로서 당당히 즐겨야 합니다.",
            "action": "이번 주 부조리했던 일들에 대해 크게 한 번 웃어넘기세요. 광대들의 무대에서 가장 빛나는 배우는 바로 당신입니다."
        },
        "second_perspective": {
            "title": "Timon (Timon of Athens)",
            "content": "인간이라는 종족을 혐오하라! (I am Misanthropos, and hate mankind.) 배신에 치를 떠는 티몬의 극단적이지만 시원한 분노."
        },
        "weekly_preview": ["주말: 셰익스피어의 위트와 휴식", "월요일: 새로운 리더십"]
    },
    5: { # Saturday: Wit/Relax (Twelfth Night)
        "title": "Weekend Wit (주말의 위트)",
        "intro": "즐거운 주말, 가벼운 마음으로 희극의 세계로 떠나봅시다.",
        "quote": {
            "text": "Be not afraid of greatness. Some are born great, some achieve greatness, and others have greatness thrust upon them.",
            "translation": "위대함을 두려워하지 말라. 누군가는 위대하게 태어나고, 누군가는 위대함을 성취하며, 누군가는 위대함을 떠안게 된다.",
            "source": "Twelfth Night, Act 2, Scene 5"
        },
        "insight": {
            "context": "말볼리오가 편지를 읽으며 착각에 빠지는 장면이지만, 말 자체는 인생의 진리를 담고 있습니다.",
            "interpretation": "어떤 경로로든 당신에게 주어진 역할과 기회를 피하지 마세요. 주말은 당신 안에 숨겨진 '위대함'을 발견하고 즐기기에 가장 좋은 시간입니다.",
            "action": "오늘 하루, 당신이 생각하는 '위대한 휴식'을 자신에게 선물하세요."
        },
        "second_perspective": {
            "title": "Bottom (Midsummer Night's Dream)",
            "content": "당나귀 머리를 하고도 여왕의 사랑을 받는 행운. 인생은 때로는 유쾌한 꿈과 같습니다."
        },
        "weekly_preview": ["일요일: 고요한 사색", "월요일: 헨리 5세의 용기"]
    },
    6: { # Sunday: Reflection (The Tempest)
        "title": "Sunday Reflection (일요일의 사색)",
        "intro": "고요한 일요일, 폭풍우가 지나간 자리에서 평화를 찾습니다.",
        "quote": {
            "text": "Our revels now are ended... We are such stuff As dreams are made on, and our little life Is rounded with a sleep.",
            "translation": "우리의 축제는 이제 끝났다... 우리는 꿈과 같은 존재이며, 우리의 짧은 인생은 잠으로 둘러싸여 있다.",
            "source": "The Tempest, Prospero"
        },
        "insight": {
            "context": "셰익스피어의 마지막 희곡에서 프로스페로가 마법의 책을 덮으며 인생의 덧없음과 아름다움을 이야기합니다.",
            "interpretation": "한 주의 치열했던 모든 일들도 결국 꿈처럼 지나갑니다. 집착을 내려놓고 편안한 '잠(휴식)'을 받아들일 때, 우리는 내일을 위한 새로운 꿈을 꿀 수 있습니다.",
            "action": "오늘 밤은 모든 걱정을 내려놓고, 가장 편안하고 깊은 잠을 청해보세요."
        },
        "second_perspective": {
            "title": "Sonnet 18",
            "content": "Shall I compare thee to a summer's day? (그대를 여름날에 비유할까요?) 영원히 시들지 않는 아름다움을 노래하며 한 주를 마무리하세요."
        },
        "weekly_preview": ["월요일: 다시 시작하는 용기", "화요일: 뜨거운 열정"]
    }
}

def create_fallback_issue(theme):
    """Fallback content when AI generation fails (e.g. CI/CD)"""
    print(f"⚠️ Generating fallback content for {theme['name']} from Anthology...")
    
    # Select content based on day index (0=Mon, 6=Sun)
    # We match theme name to find the index key if possible, or just calculate day again.
    from datetime import datetime, timedelta
    kst_now = datetime.utcnow() + timedelta(hours=9)
    day_idx = kst_now.weekday()
    
    # Use the library, verify key exists, else default to 0
    content = FALLBACK_LIBRARY.get(day_idx, FALLBACK_LIBRARY[0])
    
    # Construct data structure
    fallback_data = {
        "title": content["title"],
        "intro": content["intro"],
        "quote": content["quote"],
        "insight": content["insight"],
        "second_perspective": content["second_perspective"],
        "weekly_preview": content["weekly_preview"],
        "meta": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "theme": theme['name'],
            "generated_at": time.time(),
            "is_fallback": True,
            "source": "The Shakespeare Anthology (Fallback Library)"
        }
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fallback_data, f, ensure_ascii=False, indent=2)
    
    return fallback_data

if __name__ == "__main__":
    asyncio.run(generate_issue())
