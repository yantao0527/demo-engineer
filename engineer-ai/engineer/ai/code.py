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
        #print(prompt)

        chat = ChatOpenAI(temperature=0)
        output = chat.predict_messages(prompt)
        self.output_content = output.content
        return self.output_content
    
    def parse(self, chat): # -> List[Tuple[str, str]]:
        # Get all ``` blocks and preceding filenames
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, chat, re.DOTALL)

        files = []
        for match in matches:
            # Strip the filename of any non-allowed characters and convert / to \
            path = re.sub(r'[<>"|?*]', "", match.group(1))

            # Remove leading and trailing brackets
            path = re.sub(r"^\[(.*)\]$", r"\1", path)

            # Remove leading and trailing backticks
            path = re.sub(r"^`(.*)`$", r"\1", path)

            # Remove trailing ]
            path = re.sub(r"\]$", "", path)

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


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    from engineer.ai.prompt import prompt_example
    step2 = Code()
    output = step2.from_prompt(prompt_example)
    print(output)
