from engineer.ai.step import AnalysisStep

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def understanding():
    st.set_page_config(page_title="Code Understanding")
    st.header("Code Understanding")

    st.markdown(
        """
        It can answer questions in the context of an entire GitHub repository:
        1. Index the code base: Clone the target repository, load all files within, chunk the files, and execute the indexing process. 
           Optionally, you can skip this step and use an already indexed dataset.
        2. Ask questions: Define a list of questions to ask about the codebase, and then use the ConversationalRetrievalChain to 
           generate context-aware answers. The LLM (GPT-4) generates comprehensive, context-aware answers based on retrieved code snippets and conversation history.

"""
    )

    questions = [
        "Which modules of langchain do the code use?",
        "Is the implementation of the class `Project` too complicated? How to improve it?",
        "What do the file `man_test.py` do?",
    ]

    github_url = st.text_input("Github URL", value="https://github.com/yantao0527/demo-engineer.git")
    question_text = st.text_area("Question list", "\n".join(questions), height=150)
    force = st.checkbox("Force index if exist dataset")
    if st.button('Run') and github_url and question_text:
        step = AnalysisStep(github_url)
        if not step.ok:
            st.write("Create index...... according of size of the codebase, need a few minutes")
            step.make_index()
        elif force:
            st.write("Recreate index...... according of size of the codebase, need a few minutes")
            step.make_index()
        else:
            st.write("Skip creating index.")
        st.write("Answer all the questions...... according of number of questions, need a few minutes")
        result = step.question(question_text.split("\n"))
        st.write("Show Question And Answer Result")
        fmt_result = ["## {question}\n{answer}\n".format(question=x[0], answer=x[1]) for x in result]
        st.markdown("\n".join(fmt_result))

if __name__ == '__main__':
    understanding()

