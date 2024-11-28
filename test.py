from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

SYSTEM_PROMPT = """You are a frontend developer that makes full pages with HTML and styling using Tailwind CSS. You only return the full HTML page output with no explanation.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
])
llm = ChatOpenAI(model="gpt-4o", temperature=0)

parser = StrOutputParser()
runnable = prompt | llm | parser

print(runnable.invoke(input=prompt))

