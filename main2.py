# main2.py
import os
import asyncio
from dotenv import load_dotenv
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ① Gemini LLM 인스턴스 생성 (system message를 human message로 변환)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    convert_system_message_to_human=True,
)

# ② Task를 단계별로 분해하는 함수 (invoke 사용)
async def breakdown_task(user_task: str) -> str:
    messages = [
        ("system", "You are a browser automation planner."),
        ("human", f"""
Break down this task into the 최소 단계로 번호 매겨진 리스트로 작성해주세요.
로그인이 필요하면 '[WAIT] Pause for user to manually login.' 단 한 줄만 포함하세요.
Task: {user_task}
""".strip()),
    ]
    # invoke는 sync/async 모두 지원합니다. async 컨텍스트이므로 await 사용
    ai_msg = await llm.invoke(messages)
    return ai_msg.content.strip()

async def main():
    # ③ 실제로 수행하고 싶은 작업 정의
    user_task = (
        "유튜브에 접속하여, 로그인 화면에서 사용자가 직접 로그인할 수 있도록 기다려준 뒤, "
        "검색창에 '혁종이 채널' 검색 → 채널 진입 → 가장 최근 영상 학습 → 착한 댓글 작성"
    )

    # ④ 계획(plan) 생성
    plan = await breakdown_task(user_task)
    print("=== 생성된 실행 계획 ===")
    print(plan)

    # ⑤ Agent 실행 (plan 안의 [WAIT] 단계에서 멈춥니다)
    agent = Agent(task=plan, llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
