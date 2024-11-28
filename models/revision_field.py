from datetime import datetime
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """You are an assistant for the operations team in checking the quality and validity of a selfie image submission. Your task is to verify whether the submitted image meets the following strict guidelines:

{guidelines}

If the photo does not meet these requirements, tag it as invalid and inform the user which guidelines they failed to meet among those four. 

If the file is valid, your response should look like this:
"Thank you for submitting your {file_type}. Please wait for a response from our team". 
Say nothing but this if the file is valid.

If the file is invalid, your response should look like this:
"Thank you for providing another image." Then provide a description of the reasons why the image does not meet the guidelines
"""


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


model = ChatOpenAI(model="gpt-4o-mini", streaming=True)


def convert_message(msg):
    if msg["type"] == "human":
        return HumanMessage(content=msg["content"])
    elif msg["type"] == "ai":
        return AIMessage(content=msg["content"])


runnable = prompt | model | StrOutputParser()

# runnable = (
#     {
#         "input": lambda x: x["input"],
#         "history": lambda x: [convert_message(msg) for msg in x["history"]],
#         "date": lambda x: datetime.now().strftime("%B %d, %Y"),
#     }
#     | prompt
#     | model
#     | StrOutputParser()
# )
