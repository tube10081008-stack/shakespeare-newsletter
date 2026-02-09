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
    # Use 'uv' from PATH based on OS
    uv_path = "uv" # In GitHub Actions, uv is installed to PATH
    
    # Determine Theme based on current day (KST)
    from datetime import timedelta
    kst_now = datetime.utcnow() + timedelta(hours=9)
    weekday = kst_now.weekday()
    theme = THEMES.get(weekday, THEMES[0])
    
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

def create_fallback_issue(theme):
    """Fallback content when AI generation fails (e.g. CI/CD)"""
    print(f"⚠️ Generating fallback content for {theme['name']}")
    
    # Save a default JSON
    fallback_data = {
        "title": f"{theme['name']} (Classic)",
        "intro": "오늘은 AI Bard가 잠시 휴식을 취하고 있습니다. 대신 셰익스피어의 불멸의 고전을 원문 그대로 전해드립니다.",
        "quote": {
            "text": "All the world's a stage,\nAnd all the men and women merely players.",
            "translation": "온 세상은 무대요,\n모든 남녀는 그저 배우일 뿐이다.",
            "source": "As You Like It, Jaques"
        },
        "insight": {
            "context": "인생을 연극에 비유한 이 유명한 독백은 우리가 각자의 시기에 맞춰 다양한 역할을 수행하며 살아감을 이야기합니다.",
            "interpretation": "지금 당신은 어떤 배역을 맡고 있나요? 주인공이든 조연이든, 당신의 연기는 그 자체로 의미가 있습니다.",
            "action": "오늘 하루, 내 인생이라는 연극의 '작가'가 되어 대본을 직접 써보세요."
        },
        "second_perspective": {
            "title": "Macbeth's Shadow",
            "content": "Life's but a walking shadow, a poor player... (인생은 걸어다니는 그림자일 뿐...)"
        },
        "weekly_preview": [
            "Tuesday: Romance",
            "Wednesday: Wit"
        ],
        "meta": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "theme": theme['name'],
            "generated_at": time.time(),
            "is_fallback": True
        }
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fallback_data, f, ensure_ascii=False, indent=2)
    
    return fallback_data

if __name__ == "__main__":
    asyncio.run(generate_issue())
