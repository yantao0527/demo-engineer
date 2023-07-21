import shutil
from pathlib import Path

from engineer.ai.project import Project
from engineer.ai.clarify import Clarify
from engineer.ai.code import Code
from engineer.ai.entrypoint import Entrypoint

class CodeStep:

    def __init__(self, workspace, title, prompt):
        self.prepare_project(workspace, title, prompt)

    def prepare_root(self, workspace, title):
        root = workspace + "/" + "_".join(title.split(" "))
        if Path(root).is_dir():
            shutil.rmtree(root)
        return root

    def prepare_project(self, workspace, title, prompt):
        root = self.prepare_root(workspace, title)
        self.project = Project(root)
        self.project.load_all_file()
        self.project.set_ai_prompt(prompt)
        return self.project
    
    def clarify(self):
        self.step1 = Clarify()
        self.step1.question(self.project.get_ai_prompt())
        self.step1.assumpt()

    def make_prompt(self):
        self.step2 = Code()
        self.prompt_messages = self.step2.make_prompt_from_clarify(self.step1)
        return self.step2.prompt_content

    def gen_code(self):
        self.output = self.step2.generate_code_content(self.prompt_messages)
        return self.step2.code_content

    def parse_files(self):
        files = self.step2.parse(self.output)
        for (filename, content) in files:
            self.project.set_src_file(filename, content)
        self.project.set_log_file("code_prompt.log", self.step2.prompt_content)
        self.project.set_log_file("code_output.log", self.step2.code_content)

    def gen_entry(self):
        step3 = Entrypoint()
        content = step3.generate(self.step2.code_content)
        self.project.set_src_file("run.sh", content)

    def save(self):
        self.project.save_all_file()

    def list_src_file(self):
        return self.project.list_src_file()
    

from engineer.ai.analysis import Analysis

class AnalysisStep:
    def __init__(self, github_url):
        self.step = Analysis()
        self.ok = self.step.load_vectordb(github_url)
    
    def make_index(self):
        if self.ok:
            self.step.delete_dataset()
        root_dir = self.step.github_clone()
        self.step.index_codebase(root_dir)

    def question(self, questions):
        result = self.step.question(questions)
        return result