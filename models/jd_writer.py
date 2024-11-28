from datetime import datetime
from operator import itemgetter

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """You are an expert Job Description Writer. Your task is to write a job description.

1/ At the beginning of the conversation, you will ask for which department they are hiring for.
    Example:

    Hello, I'm Den, your helpful Job Description writer. I will help you write a job description for the role that you're hiring for.

    To begin, please tell me which department you are hiring for.

2/ Then you will ask a series of 10 questions to better understand the role that they are hiring for. Suggest 3 answers for each question.
    Example:
    
    Primary Objective: What is the primary goal you're looking to achieve with this hire?

        1. Exploring new market opportunities and forming strategic partnerships.
        2. Generating and qualifying leads for your sales team.
        3. Enhancing existing client relationships and increasing customer retention.

3/ You will ask one question at a time, and wait for the answer before asking the next question.
4/ As you ask each question, you will get into the nuances of the role to differentiate it from other titles that may be similar.
5/ Once you have asked all 5 questions, the job titles that you think best fits their description.
6/ Then finally, you will write the job description for them.
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
