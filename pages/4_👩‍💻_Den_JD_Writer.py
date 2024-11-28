import streamlit as st
import streamlit_pydantic as sp

from models.jd_writer import runnable

st.set_page_config(
    page_title="Den (JD Writer)",
    page_icon="🎓",
)

HELPTEXT = """# 👩‍💻 Den (Job Descrtion Writer)

Den is a junior job description writer that will help you write a job description for the role that you're hiring for.

Den will ask you a series of questions to better understand the role that you're hiring for. Once done, Den will generate a job description for you.

Built with ❤️ by Erudifi EPD
"""


st.title("👩‍💻 Den (Job Descrtion Writer)")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown(HELPTEXT)

for message in st.session_state.messages:
    with st.chat_message(message["type"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    # Display user message in chat message container
    st.session_state.messages.append({"type": "human", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in runnable.stream({"input": prompt, "history": st.session_state.messages}):
            full_response += chunk
            message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response)

        st.session_state.messages.append({"type": "ai", "content": full_response})