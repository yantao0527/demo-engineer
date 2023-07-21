import webbrowser
from time import sleep
import os
import logging

from engineer.ai.step import CodeStep

#logging.basicConfig(level = logging.DEBUG,format='%(levelname)s-%(message)s')

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def demo_engineer():
    # Page title
    title = '🧩 DemoEngineer'
    st.set_page_config(page_title=title)
    st.title(title)

    # Text input
    demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')
    empty_idea = st.empty()
    demo_idea = empty_idea.text_area('Enter your prompt', placeholder = 'Type your demo idea here', height=100)

    PROGRESS_BAR_INFO = {
        "start": {"text": "Preparing environment...", "percentage": 5},
        "clarify": {"text": "Clarifying prompt...", "percentage": 35},
        "code": {"text": "Generating Code...", "percentage": 85},
        "entry": {"text": "Generating Entrypoint...", "percentage": 95},
        "successed": {"text": "Successed", "percentage": 100},
        "failed": {"text": "Failed", "percentage": 100},
    }

    def progressBar(key, bar=None):
        info = PROGRESS_BAR_INFO[key]
        if bar:
            bar.progress(info["percentage"], text=info["text"])
        else:
            return st.progress(info["percentage"], text=info["text"])
        
    def step_progress(demo_title, demo_idea):
        ws = os.getenv("PROJECT_WORKSPACE")
        step = CodeStep(ws, demo_title, demo_idea)
        bar = progressBar("start")

        step.clarify()
        progressBar("clarify", bar)

        prompt_content = step.make_prompt()
        with st.expander("Log: Clarified Prompt"):
            st.text(prompt_content)

        code_content = step.gen_code()
        with st.expander("Log: Code Output"):
            st.text(code_content)

        step.parse_files()

        step.gen_entry()
        progressBar("entry", bar)

        step.save()
        progressBar("successed", bar)

        src_files = step.list_src_file()
        tabs = st.tabs([x[0] for x in src_files])
        for idx, tab in enumerate(tabs):
            with tab:
                st.code(src_files[idx][1])
        st.balloons()

    cols = st.columns([1, 1])
    if cols[0].button('Submit') and demo_title and demo_idea:
        step_progress(demo_title, demo_idea)
    if cols[1].button('Example'):
        demo_idea = empty_idea.text_area(
                'Enter your prompt', 
                "We are writing snake in python. MVC components split in separate files. Keyboard control.", 
                height=100
            )
        step_progress("snake", demo_idea)

if __name__ == '__main__':
    demo_engineer()
