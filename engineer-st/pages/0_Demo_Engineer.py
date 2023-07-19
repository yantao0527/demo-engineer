import webbrowser
from time import sleep
import os
import shutil
import logging
from pathlib import Path

from engineer.ai.project import Project
from engineer.ai.clarify import Clarify
from engineer.ai.code import Code
from engineer.ai.entrypoint import Entrypoint

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
        
    def prepare_env(title):
        ws = os.getenv("PROJECT_WORKSPACE")
        root = ws + "/" + "_".join(title.split(" "))
        if Path(root).is_dir():
            shutil.rmtree(root)
        return root

    def step_progress(demo_title, demo_idea):
        bar = progressBar("start")
        root = prepare_env(demo_title)
        project = Project(root)
        project.load_all_file()
        project.set_ai_prompt(demo_idea)

        step1 = Clarify()
        step1.question(demo_idea)
        step1.assumpt()
        progressBar("clarify", bar)

        step2 = Code()
        prompt_messages = step2.make_prompt_from_clarify(step1)
        with st.expander("Log: Clarified Prompt"):
            st.text(step2.prompt_content)

        output = step2.generate_code_content(prompt_messages)
        progressBar("code", bar)
        with st.expander("Log: Code Output"):
            st.text(step2.code_content)

        files = step2.parse(output)
        for (filename, content) in files:
            project.set_src_file(filename, content)
        project.set_log_file("code_prompt.log", step2.prompt_content)
        project.set_log_file("code_output.log", step2.code_content)

        step3 = Entrypoint()
        content = step3.generate(step2.code_content)
        project.set_src_file("run.sh", content)
        progressBar("entry", bar)
        project.save_all_file()
        progressBar("successed", bar)

        src_files = project.list_src_file()
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
