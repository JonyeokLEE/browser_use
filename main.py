"""from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())"""

# run_agent.py
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

async def main():
    # ① Gemini LLM 인스턴스 생성
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # ② 에이전트에게 수행할 작업(task) 정의
    task = (
        "유튜브에 접속하여, "
        "로그인을 먼저 해줘. 로그인을 할 때 사용자가 직접 입력을 해서 로그인 상태가 될 때 까지 기다려."
        "로그인이 완료된다면, 검색창에 혁종이 채널을 검색하여 혁종이 채널을 들어가서"
        "가장 최근에 올라온 영상을 찾아 TEST라는 댓글을 달아줘"
    )

    # ③ Agent 생성 및 실행
    agent = Agent(task=task, llm=llm)  # Agent의 기본 설정 사용 :contentReference[oaicite:1]{index=1}
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
