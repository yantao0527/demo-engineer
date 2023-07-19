from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

# import sys
# import io
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def search():
    st.set_page_config(page_title="Search and Calculate")
    st.header("Ask and Calculate")

    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    user_question = st.text_input("Ask a question and calculate", value="Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")
    if st.button('Run') and user_question:
        # output = io.StringIO()
        # original_stdout = sys.stdout
        # sys.stdout = output

        result = agent.run(user_question)
        st.write(result)

        # sys.stdout = original_stdout
        # st.write(output.getvalue())

if __name__ == '__main__':
    search()

