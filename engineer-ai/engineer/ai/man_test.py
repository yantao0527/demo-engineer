import shutil
import re
import os
from pathlib import Path


from engineer.ai.project import Project
from engineer.ai.clarify import Clarify
from engineer.ai.code import Code
from engineer.ai.entrypoint import Entrypoint
from engineer.ai.task import (
    task_create_project_with_prompt,
    task_generate_project_code,
)
from engineer.ai.analysis import Analysis

def test_clarify():
    from engineer.ai.prompt import (
        prompt_example,
    )
    step = Clarify()
    output = step.question(prompt_example)
    print(output)
    output = step.assumpt()
    print(output)
    print()
    print(step.history())


def test_print_files(files):
    for (filename, content) in files:
        print()
        print(filename)
        print("----------------------")
        print(content)
        
def test_code_from_prompt():
    from engineer.ai.prompt import prompt_example
    step2 = Code()
    output = step2.from_prompt(prompt_example)
    test_print_files(output)
    step3 = Entrypoint()
    content = step3.generate(step2.code_content)
    print(content)


# load prompt from an exist project
def test_get_ai_prompt(root):
    project = Project(root)
    project.load_all_file()
    output = project.get_ai_prompt()
    print(output)

def test_create_project_with_prompt():
    project = Project(TEST_ROOT)
    project.set_ai_prompt("This is a prompt")
    project.save_all_file()

def test_save_src():
    project = Project(TEST_ROOT)
    project.set_src_file("app.js", "This is a test file")
    project.set_src_file("style.css", "This is a css file")
    project.save_all_file()

def test_generate_code_and_save():
    project = Project(TEST_ROOT)
    project.set_ai_prompt(TEST_PROMPT)
    project.save_all_file()
    
    task_generate_project_code(TEST_ROOT)

def test_parse_code():
    log = Path("../projects/test_test/ai_log/code_output.log")
    output = log.read_text()
    #print(output)

    step = Code()
    files = step.parse(output)
    test_print_files(files)


def test_env_clear():
    if Path(TEST_ROOT).is_dir():
        shutil.rmtree(TEST_ROOT)

def test_analysis_code_index():
    step = Analysis()
    isload = step.load_vectordb(TEST_GITHUB)
    if isload:
        step.delete_dataset()
        print("Delete dataset")
    dir = step.github_clone()
    print(dir)
    step.index_codebase(dir)
    return step

def test_analysis_load():
    step = Analysis()
    isload = step.load_vectordb(TEST_GITHUB)
    print("isLoad: ")
    print(isload)
    return step

def test_analysis_code_qa(step):
    questions = [
        "Which modules of langchain do the code use?",
        "Is the implementation of the class `Project` too complicated? How to improve it?",
        "What do the file `man_test.py` do?",
    ]
    result = step.question(questions)
    for (question, answer) in result:
        print()
        print("Question: " + question)
        print("Answer:" + answer)
    
#TEST_ROOT="/tmp/projects/example"
TEST_ROOT="../projects/test_test"
TEST_PROMPT="We are writing snake in python. MVC components split in separate files. Keyboard control."
TEST_GITHUB="https://github.com/yantao0527/demo-engineer.git"

if __name__ == "__main__":
    

    from dotenv import load_dotenv
    load_dotenv()

    # test_code_from_prompt()

    # test_get_ai_prompt(""../projects/example")

    # test_env_clear()
    # test_create_project_with_prompt()
    # test_get_ai_prompt(TEST_ROOT)
    # test_save_src()

    # test_env_clear()
    # test_generate_code_and_save()

    # test_parse_code()

    # test_clarify()

    step = test_analysis_load()
    #step = test_analysis_code_index()
    test_analysis_code_qa(step)

