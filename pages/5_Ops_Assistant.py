
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

selfie_with_id_guidelines = """
    GUIDELINES
    1. The image must be clear and well-lit.
    2. The photo must show a person facing the camera and holding a physical ID.
    3. The person's hands should be visible, holding the ID.
    4. Both the person's face and the ID should be fully visible in the same frame.
    5. Obstructions: The person's face must not be obstructed, except for eyewear if necessary.

    Examples of invalid image files are the following: 
    - A standalone ID card without a person holding this ID card
    - A photo where the ID is not held in the person's hands.
    - A photo of an object, background, or any unrelated subject.
"""

guidelines_dict = {
    "Selfie w/ ID": selfie_with_id_guidelines,
    "Assessment File": """ Insert Some guidelines here """
}
def get_image_description(uploaded_file, file_type):
    # Encode the uploaded image in base64
    encoded_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

    guidelines = guidelines_dict.get(file_type)
    response = ""
    for chunk in runnable.stream({"file_type": file_type, "guidelines": guidelines, "image_url": f"data:image/png;base64,{encoded_image}"}):
        response += chunk
    return response
    # response = client.chat.completions.create(
    #     model=model_choice,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {"type": "text", "text": SYSTEM_PROMPT},
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
    #                 },
    #             ],
    #         }
    #     ],
    #     max_tokens=300,
    # )

# Streamlit app layout
st.title("Image Description using GPT-4o and GPT-4o Mini")
st.write("Upload an image and get a description using GPT-4o or GPT-4o Mini.")

# Textbox for updating OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY", "")

if api_key:
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Upload image button
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    # File type dropdown
    file_type = st.selectbox("Choose File Type", ["Assessment File", "Selfie w/ ID"])

    if uploaded_file is not None:
        try:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("")
            st.write("Classifying...")

            # Get the image description
            description = get_image_description(uploaded_file, file_type)
            st.write(description)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Please provide a valid OpenAI API key.")