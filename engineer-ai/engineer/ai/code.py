import re

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from engineer.ai.prompt import (
    generate_code,
    philosphy,
    use_clarify,
)
from engineer.ai.clarify import Clarify

class Code:
    def from_prompt(self, prompt):
        step = Clarify()
        step.question(prompt)
        step.assumpt()
        output = self.from_clarify(step)
        print(output)
        return self.parse(output)

    def from_clarify(self, clarify: Clarify):
        prompt = generate_code + "\nUseful to know:\n" + philosphy
        system_message_prompt = SystemMessagePromptTemplate.from_template(prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")

        all_messages = [system_message_prompt] + clarify.history() + [human_message_prompt]
        chat_prompt = ChatPromptTemplate.from_messages(all_messages)

        prompt = chat_prompt.format_messages(input=use_clarify)
        self.prompt_content = chat_prompt.format(input=use_clarify)
        print(self.prompt_content)

        chat = ChatOpenAI(temperature=0)
        output = chat.predict_messages(prompt)
        self.code_content = output.content
        return self.code_content
    
    def parse_0(self, chat): # -> List[Tuple[str, str]]:
        # Get all ``` blocks and preceding filenames
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, chat, re.DOTALL)

        files = []
        for match in matches:
            print(match.group(1))
            # Strip the filename of any non-allowed characters and convert / to \
            path = re.sub(r'[<>"|?*]', "", match.group(1))

            # Remove leading and trailing brackets
            path = re.sub(r"^\[(.*)\]$", r"\1", path)

            # Remove leading and trailing backticks
            path = re.sub(r"^`(.*)`$", r"\1", path)

            # Remove trailing ]
            path = re.sub(r"\]$", "", path)
            print(path)

            # Get the code
            code = match.group(2)

            # Add the file to the list
            files.append((path, code))

        # Get all the text before the first ``` block
        readme = chat.split("```")[0]
        files.append(("README.md", readme))

        # Return the files
        self.output_files = files
        return files
    
    def parse(self, output):
        filename_pattern = re.compile(r"^.*`(.*)`")
        code_sep_pattern = re.compile(r"^```")
        def parse_filename(line):
            m = filename_pattern.match(line)
            if m:
                return m.group(1)
            return None
        def parse_code_sep(line):
            m = code_sep_pattern.match(line)
            return m != None
        code_flag = False
        code_result = []
        doc_result = []
        filename = None
        files = []
        for line in output.splitlines():
            if code_flag:
                if parse_code_sep(line):
                    code_flag = not code_flag
                    files.append( (filename, "\n".join(code_result)) )
                    filename = None
                else:
                    code_result.append(line)
            else:
                if not filename:
                    filename = parse_filename(line)
                if parse_code_sep(line):
                    code_flag = not code_flag
                    code_result = []
                else:
                    doc_result.append(line)
        files.append( ("code_readme.md", "\n".join(doc_result)) )
        self.output_files = files
        return files



if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    from engineer.ai.prompt import prompt_example
    step2 = Code()
    output = step2.from_prompt(prompt_example)
    print(output)
