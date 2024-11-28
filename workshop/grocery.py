import json
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """You are a Grocery List maker.
Given a dish, you will give me a list of ingredients I can buy at the market.
Quantities will be in their respective units (g, kg, pcs)
{format_instructions}
"""


class GroceryItem(BaseModel):
    name: str = Field(..., description="Name of the ingredient")
    quantity: str = Field(..., description="Quantity of the ingredient")
    unit: str = Field(..., description="Unit of the ingredient")


class GroceryList(BaseModel):
    items: List[GroceryItem] = Field(
        ..., description="List of ingredients for the dish"
    )


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Description of the page: {input}"),
    ]
)
parser = JsonOutputParser(pydantic_object=GroceryList)
prompt = prompt.partial(format_instructions=parser.get_format_instructions())
llm = ChatOpenAI(model="gpt-4o", temperature=0)
runnable = prompt | llm | parser

if __name__ == "__main__":
    # print(parser.get_format_instructions())
    resp = runnable.invoke({"input": "Chicken Adobo"})
    print(json.dumps(resp))
