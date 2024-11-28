import streamlit as st

from models.customer_support import runnable

st.set_page_config(
    page_title="Jared (CS Agent)",
    page_icon="👨‍💼",
)

HELPTEXT = """# 👨‍💼Jared (CS Agent)

Jared is a junior customer support agent for Bukas, tasked to handle customer concerns and issues. His job is to aid our customer success team by frontlining customer concerns and issues.

## Cases It Can Cover
- Loan application concerns (unable to apply, application status, etc)
- Account concerns (unable to login, etc)
- Payment concerns (deferral requests, payment not reflected, etc)

## Example starting messages
- I'm unable to apply for a loan.
- My payment hasn't been reflected yet.
- I'm unable to pay this coming due date.
- I have an issue with my account.

Built with ❤️ by Erudifi EPD
"""

st.title("👨‍💼 Jared (CS Agent)")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown(HELPTEXT)

for message in st.session_state.messages:
    with st.chat_message(message["type"]):
        st.markdown(message["content"])

if prompt := st.chat_input("You concern: "):
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