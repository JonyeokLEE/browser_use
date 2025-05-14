import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(
			viewport_expansion=0,
		)
	)
)

task1 = (
        "유튜브에 접속하여, "
        "로그인을 먼저 해줘. 로그인을 할 때 사용자가 직접 입력을 해서 로그인 상태가 될 때 까지 기다려."
        "로그인이 완료된다면, 검색창에 혁종이 채널을 검색하여 혁종이 채널을 들어가서"
        "가장 최근에 올라온 영상을 찾아 TEST라는 댓글을 달아줘"
    )

async def run_task():
	agent = Agent(
		task=task1,
		llm=llm,
		max_actions_per_step=4,
		browser=browser,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_task())