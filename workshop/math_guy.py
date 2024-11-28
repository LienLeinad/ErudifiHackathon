from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """You are a math guy. You can do math opereations using the tools below.
"""


@tool
def add(num1: int, num2: int):
    """Add two integers together."""
    return num1 + num2


@tool
def multiply(num1: int, num2: int):
    """Multiply two integers together."""
    return num1 * num2


def call_tools(msg: AIMessage):
    """Simple sequential tool calling helper."""
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])
    return tool_calls


tools = [add, multiply]
tool_map = {tool.name: tool for tool in tools}
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Description of the page: {input}"),
    ]
)
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm.bind_tools(tools)
runnable = prompt | llm | call_tools

if __name__ == "__main__":
    resp = runnable.invoke({"input": "Add 3 and 5"})
    print(resp)
