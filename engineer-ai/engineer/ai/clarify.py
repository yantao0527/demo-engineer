from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict


from engineer.ai.prompt import (
    clarify_question,
)

class Clarify:
    def question(self, input):
        system_message_prompt = SystemMessagePromptTemplate.from_template(clarify_question)
        placeholder = MessagesPlaceholder(variable_name="history")
        human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, placeholder, human_message_prompt])

        llm = ChatOpenAI(temperature=0)
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation = ConversationChain(memory=self.memory, prompt=chat_prompt, llm=llm)
        output = self.conversation.predict(input=input)
        return output

    def assumpt(self):
        output = self.conversation.predict(input="Make your own assumptions and state them explicitly before starting")
        return output
    
    def history(self):
        dicts = messages_to_dict(self.memory.chat_memory.messages)
        return messages_from_dict(dicts)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

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



