from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """You are a frontend developer that makes full pages with HTML and styling using TailwindCSS.
You only return the full HTML page output with no explanation.
Exclude ```html``` and write the HTML code only.
Avoid \n and \t in the code.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Description of the page: {input}"),
    ]
)
llm = ChatOpenAI(model="gpt-4o", temperature=0)
runnable = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    resp = runnable.invoke(
        {"input": "A landing page with a hero and a FAQ section with placeholders."}
    )
    print(resp)
