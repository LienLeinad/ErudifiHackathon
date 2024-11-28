from enum import Enum
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
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


class DataCheckerResponse(BaseModel):
    classification: Classification
    feedback: str = Field(..., description=FEEDBACK_GUIDELINES)


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
