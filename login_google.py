import asyncio
import base64
import json
import os
from dotenv import load_dotenv
from browser_use.browser.browser import Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import io
from PIL import Image

# .env에서 환경 변수 로드
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = None  # __main__에서 초기화됩니다.

async def analyze_screen_with_gemini(screenshot: str) -> dict:
    try:
        b64 = screenshot.split(",", 1)[1]
        img_bytes = base64.b64decode(b64)
        Image.open(io.BytesIO(img_bytes))

        prompt = """
이 화면은 Google 로그인 프로세스의 어느 단계인가요?
이 단계에서 필요한 입력 필드는 무엇인가요? (예: 이메일, 비밀번호, 전화번호 등)
JSON 형식으로:
{
  "stage": "단계 설명",
  "requiredField": "필요한 입력 필드 이름",
  "action": "취해야 할 행동(예: 입력, 버튼 클릭)",
  "buttonSelector": "버튼 선택자(가능하면)"
}
"""
        messages = [
            SystemMessage(content="당신은 웹 페이지 분석 전문가입니다."),
            HumanMessage(content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": screenshot}}
            ])
        ]
        resp = await asyncio.to_thread(llm.invoke, messages)
        txt = resp.content
        s, e = txt.find("{"), txt.rfind("}") + 1
        if s != -1 and e > s:
            return json.loads(txt[s:e])
    except Exception as ex:
        print(f"[analyze 오류] {ex}")

    return {"stage":"unknown","requiredField":"unknown","action":"unknown","buttonSelector":""}


async def google_login():
    browser_instance = Browser(
        config=BrowserConfig(
            # 필요시 Chrome 경로 지정
            # browser_binary_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
    )
    context = await browser_instance.new_context()
    page = await context.get_current_page()
    await page.goto("https://accounts.google.com/")

    try:
        login_complete = False

        while not login_complete:
            page = await context.get_current_page()

            # 1) 스크린샷 찍고 base64로 인코딩
            raw_bytes = await page.screenshot(type="png")
            b64 = base64.b64encode(raw_bytes).decode()
            shot = f"data:image/png;base64,{b64}"

            # 2) 화면 분석
            print("\n→ 화면 분석 중…")
            info = await analyze_screen_with_gemini(shot)
            stage = info.get("stage", "").lower()
            print(f"   단계: {info.get('stage')}")

            # 3) 로그인 완료 확인
            if any(k in stage for k in ("complete", "success", "logged in")):
                print("✅ 로그인 완료!")
                login_complete = True
                break

            # 4) 필요한 입력 처리
            field = info.get("requiredField")
            if field and field not in ("none", "unknown"):
                answer = input(f"{field}을(를) 입력하세요: ")

                # sel 변수 정의: 필드명에 따라 CSS 선택자 결정
                if any(x in field.lower() for x in ("email", "아이디", "이메일")):
                    sel = 'input[type="email"],input[name="identifier"],input#identifierId'
                elif any(x in field.lower() for x in ("password", "비밀번호")):
                    sel = 'input[type="password"]'
                elif any(x in field.lower() for x in ("phone", "전화번호")):
                    sel = 'input[type="tel"]'
                else:
                    sel = 'input:not([type="hidden"])'

                try:
                    await page.wait_for_selector(sel)
                    await page.fill(sel, answer)
                    print(f"   {field} 입력 완료")
                except Exception as e:
                    print(f"   입력 실패: {e}")

                # 입력 직후 Enter 키로 다음 단계 진행
                await page.keyboard.press("Enter")
                print("   Enter 키로 다음 단계 이동")
                await asyncio.sleep(2)
                continue  # 다시 스크린샷 → 분석

            # 5) 입력이 없으면 버튼 클릭
            btn = info.get("buttonSelector") or 'button[type="submit"],button#identifierNext,button#passwordNext'
            try:
                await page.wait_for_selector(btn)
                await page.click(btn)
                print("   버튼 클릭 완료")
            except Exception as e:
                print(f"   버튼 클릭 실패({btn}): {e} → Enter 키로 진행")
                await page.keyboard.press("Enter")
            await asyncio.sleep(2)

        # 6) 로그인 절차 완료
        print("모든 로그인 절차가 완료되었습니다.")

    except Exception as err:
        print(f"[google_login 오류] {err}")
    finally:
        await browser_instance.close()
        print("→ 브라우저 종료")


if __name__ == "__main__":
    # Gemini API 키 확인
    if not GEMINI_API_KEY:
        GEMINI_API_KEY = input("Gemini API 키를 입력하세요: ")
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

    # LLM 초기화 (Gemini 2.0 Flash 모델)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=GEMINI_API_KEY
    )

    # Google 로그인 자동화 실행
    asyncio.run(google_login())
