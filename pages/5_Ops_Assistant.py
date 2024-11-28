import base64
import os
from enum import Enum

import streamlit as st
import streamlit_pydantic as sp
from pydantic import BaseModel, Field

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


selfie_with_id_guidelines = """1. The image must be clear and well-lit.
2. The photo must show a person facing the camera and holding a physical ID.
3. The person's hands should be visible, holding the ID.
4. The ID should show the front side containing the name of the person.
5. Both the person's face and the ID should be fully visible in the same frame.
6. The person's face must not be obstructed, except for eyewear if necessary.

Examples of invalid image files are the following: 
- A standalone ID card without a person holding this ID card
- A photo where the ID is not held in the person's hands.
- A photo of an object, background, or any unrelated subject.
"""
assessment_file_guidelines = """1. The image must be clear and well-lit.
2. The image must contain a person's name as a text.
3. The image must contain student number.
4. The image must contain a tuition fee.
"""
proof_of_income_guidelines = """
1. Classify as follows:
 * Income Tax Return BIR 2316
 * Certificate of Employment with monthly income
 * Payslips
 * Payroll bank account statement
 * DTI Permit
 * City Business Permit
 * Barangay Business Permit
 * Bank Statements
 * Income Tax Return 1701
 * Audited Financial Statements
 * Employment Contract
 * Remittance Receipts 
2. If classified as Payslips/Remittance Receipts/Bank Statements, date issued should NOT be beyond the last 3 months from today's date.
3. Person's name should be clearly shown in the image
"""

guidelines_dict = {
    "Selfie with ID File": selfie_with_id_guidelines,
    "Assessment File": assessment_file_guidelines,
    "Proof of Income File": proof_of_income_guidelines,
}


class FileTypeChoices(str, Enum):
    ASSESSMENT_FILE = "Assessment File"
    SELFIE_WITH_ID_FILE = "Selfie with ID File"
    PROOF_OF_INCOME_FILE = "Proof of Income File"


class RevisionFileInput(BaseModel):
    file_type: FileTypeChoices = Field(..., description="File Type uploaded")


# Streamlit app layout
st.title("Revisions Required")
st.write("Upload your revision field")
# Textbox for updating OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY", "")

if api_key:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    revision_file_input = sp.pydantic_form(
        key="revision_file_input", model=RevisionFileInput
    )

    if revision_file_input and uploaded_file:
        try:
            file_type = revision_file_input.file_type
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
