from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# import sys
# import io
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

load_dotenv()

def chat_history():
    st.set_page_config(page_title="Chat History")
    st.header("Chat History")

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    history = st.container()
    with history:
        # display message history
        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                message(msg.content, is_user=True, key=str(i) + '_user_')
            else:
                message(msg.content, is_user=False, key=str(i) + '_ai_')

    user_input = st.text_input("Your message: ")
    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with history:
            message(user_input, is_user=True)
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(
            AIMessage(content=response.content))
        with history:
            message(response.content, is_user=False)


if __name__ == '__main__':
    chat_history()

