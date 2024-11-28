import streamlit as st
import streamlit_pydantic as sp

from models.revision_field import runnable

st.set_page_config(
    page_title="Patricia (Operations Assistant)",
    page_icon="🎓",
)

HELPTEXT = """# 👩‍💻 Patricia (Operations Assistant)

Patricia is a operations assistant that will help you check the files received from the borrower.

Patricia will provide you feedback of the file you sent.
Built with ❤️ by Erudifi EPD
"""

import base64
import os

import streamlit as st
from openai import OpenAI

selfie_with_id_guidelines = """1. The image must be clear and well-lit.
2. The photo must show a person facing the camera and holding a physical ID.
3. The person's hands should be visible, holding the ID.
4. Both the person's face and the ID should be fully visible in the same frame.
5. Obstructions: The person's face must not be obstructed, except for eyewear if necessary.

Examples of invalid image files are the following: 
- A standalone ID card without a person holding this ID card
- A photo where the ID is not held in the person's hands.
- A photo of an object, background, or any unrelated subject.
"""
assessment_file_guidelines = """1. The image must be clear and well-lit.
2. The image must contain a real person's name as a text.
3. The image must contain student number.
4. The image must contain a tuition numerical value.
"""

guidelines_dict = {
    "Selfie w/ ID": selfie_with_id_guidelines,
    "Assessment File": assessment_file_guidelines,
}


# Streamlit app layout
st.title("Revisions Required")
st.write("Upload your revision field")
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
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
            st.write("")
            st.write("Classifying...")

            # Get the image description
            encoded_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

            guidelines = guidelines_dict.get(file_type)
            response = runnable.invoke(
                {
                    "guidelines": guidelines,
                    "image_url": f"data:image/png;base64,{encoded_image}",
                }
            )
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Please provide a valid OpenAI API key.")
