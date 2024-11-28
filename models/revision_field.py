from datetime import date
from enum import Enum
from typing import Optional

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """You are an assistant for the operations team in checking the quality and validity of a selfie image submission. Your task is to verify whether the submitted image meets the following strict guidelines:

GUIDELINES
{guidelines}

{format_instructions}
"""


class Classification(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"


FEEDBACK_GUIDELINES = """Provide some suggestions on how to improve the quality of their photo based on the guidelines that their uploaded file did not meet.
Ensure that you are using a tentative tone instead of an authoritative tone. 
Keep it short. Afterwards, suggest retaking the photo
"""


class FileType(str, Enum):
    ASSESSMENT_FILE = "Assessment File"
    SELFIE_WITH_ID_FILE = "Selfie with ID File"
    BANK_STATEMENT = "Bank Statement"
    PAYSLIP = "Payslip"
    INVOICE = "Invoice"
    FINANCIAL_STATEMENT = "Financial Statement"
    TAX_RETURN = "Tax Return"
    INVALID = "Invalid"


class DataCheckerResponse(BaseModel):
    classification: Classification
    feedback: str = Field(..., description=FEEDBACK_GUIDELINES)
    file_type: FileType = Field(..., description="File type of the image uploaded")
    total_income: Optional[float] = Field(
        description="Total Gross Monthly Income amount in the statement if it is present in the document"
    )
    date_issued: Optional[date] = Field(
        ..., description="Date when the file is issued, if applicable and readable"
    )
    first_name: Optional[str] = Field(
        ..., description="First name of the issuant of the file"
    )
    last_name: Optional[str] = Field(
        ..., description="Last name of the issuant of the file"
    )


parser = JsonOutputParser(pydantic_object=DataCheckerResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            template=[
                {"type": "image_url", "image_url": "{image_url}"},
            ]
        ),
    ]
)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())
model = ChatOpenAI(model="gpt-4o-mini", streaming=True)


runnable = prompt | model | parser
