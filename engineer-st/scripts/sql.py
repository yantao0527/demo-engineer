from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
# from langchain.llms.openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()

DB = os.getenv("DATABASE")

def sql_agent():
    db = SQLDatabase.from_uri(DB)

    # llm=OpenAI(temperature=0)
    from langchain.chat_models import ChatOpenAI
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    llm = ChatOpenAI(model_name="gpt-4")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )

    # Describing a table
    agent_executor.run("Describe the Order related table and how they are related")

    # Recovering from an error
    agent_executor.run("Describe the PurchaseDetails table")

    agent_executor.run("Find the top 5 products with the highest total sales revenue")

    agent_executor.run("List the top 3 countries with the highest number of orders")

if __name__ == '__main__':
    sql_agent()
