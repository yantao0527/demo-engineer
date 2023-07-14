from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(temperature=0)
