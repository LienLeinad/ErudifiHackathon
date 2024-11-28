from typing import List
from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser

SYSTEM_PROMPT = """You are an assistant for the operations team in checking the quality and validity of a selfie image submission. Your task is to verify whether the submitted image meets the following strict guidelines:

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

If the photo does not meet these requirements, tag it as invalid and inform the user which guidelines they failed to meet among those four. 

If the file is valid, your response should look like this:
"Thank you for submitting your file. Please wait for a response from our team". 
Say nothing but this if the file is valid.

If the file is invalid, your response should look like this:
"Thank you for providing another image." Then provide a description of the reasons why the image does not meet the guidelines
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(model="gpt-4-1106-preview", streaming=True)


def convert_message(msg):
    if msg["type"] == "human":
        return HumanMessage(content=msg["content"])
    elif msg["type"] == "ai":
        return AIMessage(content=msg["content"])


runnable = (
    {
        "input": lambda x: x["input"],
        "history": lambda x: [convert_message(msg) for msg in x["history"]],
        "date": lambda x: datetime.now().strftime("%B %d, %Y"),
    }
    | prompt
    | model
    | StrOutputParser()
)