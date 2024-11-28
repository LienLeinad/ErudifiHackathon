import streamlit as st
import streamlit_pydantic as sp

from models.study_assistant import runnable

st.set_page_config(
    page_title="Jade (Study Assistant)",
    page_icon="🧑‍🎓",
)

HELPTEXT = """# 🧑‍🎓 Jade (Study Assistant)

Jade is a junior study assistant that will help you with your study concerns.

Jade will give you a high-level overview of the topic you are studying.
After that, Jade will go through each bullet point and explain it in more detail.
Once done with the explanation, Jade will run a 10 question quiz on the subject.

Built with ❤️ by Erudifi EPD
"""


st.title("🧑‍🎓 Jade (Study Assistant)")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown(HELPTEXT)
    level = st.selectbox("Level", [
        "High School",
        "College",
        "Graduate School",
    ])
    subject = st.selectbox("Subject", [
        "Business",
        "Literature",
        "IT",
        "Engineering",
        "Chemistry",
        "Physics",
        "Biology",
    ])
    topic = st.text_input("Topic", "Business Accounting")

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
        for chunk in runnable.stream({
                "input": prompt,
                "history": st.session_state.messages,
                "subject": subject,
                "topic": topic,
                "level": level,
            }):
            full_response += chunk
            message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response)

        st.session_state.messages.append({"type": "ai", "content": full_response})