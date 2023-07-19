from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
# from langchain.llms.openai import OpenAI

import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

DB = os.getenv("DATABASE")

def sql_agent():
    st.set_page_config(page_title="SQL Agent")
    st.header("SQL Agent")

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

    st.markdown(
        """
        It's [MySQL sample database](https://www.mysqltutorial.org/mysql-sample-database.aspx) 
        that contains typical business data 
        such as customers, products, sales orders, sales order line items, 
        etc. You can ask the example questions below:
        - Describe the Order related table and how they are related
        - Describe the PurchaseDetails table
        - Find the top 5 products with the highest total sales revenue
        - List the top 3 countries with the highest number of orders

"""
    )

    user_question = st.text_input("Ask the question about the example db:")
    if user_question:
        ai_answer = agent_executor.run(user_question)
        st.write(ai_answer)

if __name__ == '__main__':
    sql_agent()
