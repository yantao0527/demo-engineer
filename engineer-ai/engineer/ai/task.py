from engineer.ai.project import Project
from engineer.ai.code import Code
from engineer.ai.entrypoint import Entrypoint

def task_create_project_with_prompt(root: str, prompt: str):
    project = Project(root)
    project.load_all_file()
    project.set_ai_prompt(prompt)
    step = Code()
    files = step.from_prompt(prompt)
    for (filename, content) in files:
        project.set_src_file(filename, content)
    project.set_log_file("code_prompt.log", step.prompt_content)
    project.set_log_file("code_output.log", step.code_content)

    step3 = Entrypoint()
    content = step3.generate(step.code_content)
    project.set_src_file("run.sh", content)
    project.save_all_file()
    return project

def task_generate_project_code(root: str):
    project = Project(root)
    project.load_all_file()
    prompt = project.get_ai_prompt()
    step = Code()
    files = step.from_prompt(prompt)
    for (filename, content) in files:
        project.set_src_file(filename, content)
    project.set_log_file("code_prompt.log", step.prompt_content)
    project.set_log_file("code_output.log", step.code_content)

    step3 = Entrypoint()
    content = step3.generate(step.code_content)
    project.set_src_file("run.sh", content)
    project.save_all_file()
    return project
