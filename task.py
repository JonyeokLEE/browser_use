import asyncio
import os
from dotenv import load_dotenv

from browser_use import Agent, Controller, ActionResult
from langchain_google_genai import ChatGoogleGenerativeAI   # Gemini LLM

# ──────────────────── 1. 환경 변수 로드 ────────────────────
load_dotenv()                         # .env 파일에 GEMINI_API_KEY 등을 넣어 두세요
GEMINI_MODEL = "gemini-2.0-flash" # 필요 시 다른 버전으로 교체

# ──────────────────── 2. 사용자-입력용 커스텀 액션 정의 ────────────────────
controller = Controller()


@controller.action("Ask user for information")
def ask_user(question: str) -> str:
    answer = input(f"\n{question}\n입력 ➜ ")
    # 👇 꼭 include_in_memory=True로 반환
    return ActionResult(
        extracted_content=answer,
        include_in_memory=True  # ← 이 줄이 있어야 LLM이 기억합니다
    )

# ──────────────────── 3. LLM 및 Agent 생성 ────────────────────
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0.0,
)

def build_agent(task: str) -> Agent:
    """
    원하는 작업(task) 문자열만 넘기면
    Ask-user 액션이 내장된 Agent 인스턴스를 돌려준다.
    """
    return Agent(
        task=task,
        llm=llm,
        controller=controller,
        enable_memory=True,
    )

# ──────────────────── 4. 실행 예시 ────────────────────
async def main():
    with open("script_kr.md", "r", encoding="utf-8") as f:
        task = f.read()

    agent = build_agent(task)
    await agent.run(max_steps=50)

if __name__ == "__main__":
    asyncio.run(main())
