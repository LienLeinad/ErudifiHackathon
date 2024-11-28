
import streamlit as st
import streamlit_pydantic as sp

from models.revision_field import runnable
from models.revision_field import SYSTEM_PROMPT

st.set_page_config(
    page_title="Patricia (Operations Assistant)",
    page_icon="🎓",
)

HELPTEXT = """# 👩‍💻 Patricia (Operations Assistant)

Patricia is a operations assistant that will help you check the files received from the borrower.

Patricia will provide you feedback of the file you sent.
Built with ❤️ by Erudifi EPD
"""

import os
import streamlit as st
from openai import OpenAI
import base64



def get_image_description(client, uploaded_file, model_choice):
    # Encode the uploaded image in base64
    encoded_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

    # Create the GPT-4o or GPT-4o-mini API request
    response = client.chat.completions.create(
        model=model_choice,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    # Extract and return the description
    return response.choices[0].message.content

# Streamlit app layout
st.title("Image Description using GPT-4o and GPT-4o Mini")
st.write("Upload an image and get a description using GPT-4o or GPT-4o Mini.")

# Textbox for updating OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY", "")

if api_key:
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Dropdown for selecting the model
    model_choice = "gpt-4o-mini"

    # Upload image button
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("")
            st.write("Classifying...")

            # Get the image description
            description = get_image_description(client, uploaded_file, model_choice)
            st.write(description)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Please provide a valid OpenAI API key.")