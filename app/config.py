from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="openai/gpt-oss-120b:free",
    temperature=0.2,
)
