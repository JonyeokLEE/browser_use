import asyncio
import os
from dotenv import load_dotenv

from browser_use import Agent, Controller, ActionResult
from browser_use.browser.browser import Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)


# 1) Controller 인스턴스 생성
controller = Controller()

# 2) 모든 input_text 액션을 터미널 입력으로 대체하는 훅 정의
@controller.action("input_text")
def ask_input_text(index: int, text: str) -> ActionResult:
    # index: 몇 번째 요소인지, text: 기본값(기억된 값)
    answer = input(f"[필드 {index}] 입력할 값을 알려주세요 (기본값: '{text}')\n> ")
    return ActionResult(extracted_content=answer, include_in_memory=True)

@controller.action("Ask user for information")
def ask_user(question: str) -> ActionResult:
    answer = input(f"{question}\n> ")
    return ActionResult(extracted_content=answer,  include_in_memory=True)

controller.action("Ask user for information")(ask_user)

async def main():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY") or input("Gemini API 키를 입력하세요: ")
    os.environ["GEMINI_API_KEY"] = key

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=key
    )

    browser = Browser(config=BrowserConfig())

    task = (
        "입력 필드에 채울 때는 반드시 input_text 훅을 통해 받은 값을 사용할 것."
        "1. 구글 로그인 페이지(https://accounts.google.com/)로 이동하세요. "
        "2. 페이지 위에 있는 모든 로그인 입력 필드(아이디, 비밀번호 등)를 자동으로 인식합니다. 필드가 하나라도 존재하면, 각 필드마다 터미널에 “무엇을 입력할까요?”라고 물어보고, 받은 값을 해당 필드에 채워 넣으세요. 이때, 반드시 사용자의 입력만을 사용하세요."
        "3. 더 이상 입력할 필드가 없을 때까지, 모든 필드를 인식해서 Step 2를 반복하세요."
        "4. 더 이상 입력할 칸이 없을 때, 다음 단계로 넘어갈 수 있는 버튼을 누르세요."
        "5. 로그인이 완료되어 다음 페이지로 넘어가 로그인 상태로 유지가 된다면 성공!"
        "6. 만약 로그인 상태가 완성되지 않았다면, Step 2부터 다시 반복하세요,"
        "7. 만약 로그인이 완료되어 성공하였다면, 터미널에 성공했다는 축하 메세지와 함께 정상적인 종료"

        "로그인이 정상적으로 완료되었는지 확인하기 위해, 로그인 된 상태에서 사용자의 계정 정보를 접근할 수 있는지 확인한다. 사용자 계정 정보에 등록되어있는 사용자의 이름을 알아내어서 터미널로 출력하고 종료한다."

        "다음은 필수 조건이다."
        "   반드시 Ask user for information 액션을 호출해 한국어로 물어본다.\n"
        "   (예: '구글 이메일을 입력해 주세요')\n"
        " 사용자가 입력해 준 값을 해당 필드에 채우고 그 상태를 유지한 채로 다음 단계로 진행한다.\n"
        " 사용자가 입력해준 값을 지우면 안된다"
    )
    agent = Agent(
        task=task,
        llm=llm,
        controller=controller,
        browser=browser,
        #enable_memory=False,
    )

    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
