from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()

def search():
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    result = agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")
    print("\n\n", result)

if __name__ == '__main__':
    search()

