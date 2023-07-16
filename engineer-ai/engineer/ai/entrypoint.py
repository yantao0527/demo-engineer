import re
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

from engineer.ai.prompt import (
    generate_code,
    philosphy,
    entrypoint_generate,
)


class Entrypoint:
    def generate(self, prev_code_output):
        system_message_prompt = SystemMessagePromptTemplate.from_template(entrypoint_generate)
        human_message_prompt = HumanMessagePromptTemplate.from_template("Information about the codebase:\n\n{input}")

        all_messages = [system_message_prompt, human_message_prompt]
        chat_prompt = ChatPromptTemplate.from_messages(all_messages)

        prompt = chat_prompt.format_messages(input=prev_code_output)
        #print(prompt)

        chat = ChatOpenAI(temperature=0)
        output = chat.predict_messages(prompt)
        self.code_content = output.content

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, output.content, re.DOTALL)
        return "\n".join(match.group(1) for match in matches)
