import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Let AI help us 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    LangChain is an open-source framwork that buid applications with LLMs through composability.
    Agents can be used for a variety of tasks. Agents combine the decision making ability
    of a language model with tools in order to create a system that can execute and 
    implement solutions on your behalf.
    
    **👈 Select a demo from the sidebar** to see some examples
    of what AI agent can do!

    ### What about the demo?
    - The [sources](https://github.com/yantao0527/demo-engineer) of the demo
    - The Author [Frank Yan](https://www.upwork.com/freelancers/~01eea029b1550734f4?viewMode=1) on Upwork
    ### Tech stack of the demo
    - [LangChain Documentation](https://python.langchain.com/en/latest/index.html)
    - [streamlit.io](https://streamlit.io)
"""
)