from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()


physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise and easy to understand manner. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{input}"""


math_template = """You are a very good mathematician. You are great at answering math questions. \
You are so good because you are able to break down hard problems into their component parts, \
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}"""

prompt_infos = [
    {
        "name": "physics", 
        "description": "Good for answering questions about physics", 
        "prompt_template": physics_template
    },
    {
        "name": "math", 
        "description": "Good for answering math questions", 
        "prompt_template": math_template
    }
]

chain = MultiPromptChain.from_prompts(OpenAI(), prompt_infos, verbose=True)

print(chain.run("What is black body radiation?"))

print(chain.run("What is the first prime number greater than 40 such that one plus the prime number is divisible by 3"))

print(chain.run("What is the name of the type of cloud that rins"))
