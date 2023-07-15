import shutil
import re
from pathlib import Path


from engineer.ai.project import Project
from engineer.ai.code import Code
from engineer.ai.task import (
    task_create_project_with_prompt,
    task_generate_project_code,
)

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

#TEST_ROOT="/tmp/projects/example"
TEST_ROOT="../projects/test_test"
TEST_PROMPT="We are writing snake in python. MVC components split in separate files. Keyboard control."

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    test_code_from_prompt()

    #test_get_ai_prompt(""../projects/example")

    # test_env_clear()
    # test_create_project_with_prompt()
    # test_get_ai_prompt(TEST_ROOT)
    # test_save_src()

    # test_env_clear()
    # test_generate_code_and_save()

    # test_parse_code()

