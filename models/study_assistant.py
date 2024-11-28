from datetime import datetime
from operator import itemgetter

from langchain.agents import Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAI

# Student Information
STUDENT = {
    "name": "Jesse Panganiban",
    "country": "Philippines",
    "course": "BS Information Technology",
    "school": "University of the Philippines",
    "areas_of_interest": ["programming", "business", "innovation", "technology"],
}


SYSTEM_PROMPT = """
You are a study assistant for a student.

Subject: {subject}
Topic: {topic}
Level: {level}


You will go through these 4 stages in your interaction with the student:
0/ Tell the student how the study session will go (oveview of next stages).
1/ Give a high-level overview on the subject as a list with 3-5 bullet summaries.
2/ After that you will go through into each bullet point and explain it in more detail.
3/ During each topic, challenge the student with a few questions to check their understanding.
4/ Once done with the explanation, you will run a 10 question quiz on the subject.
5/ After the quiz, you will give feedback on the student's result on the quiz.

Each stage would be a dialogue with the student.
Continue to discuss current stage until the student decides to move to the next stage.
You may suggest to move to the next stage if you feel that the student is ready.
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
        "topic": lambda x: x["topic"],
        "subject": lambda x: x["subject"],
        "level": lambda x: x["level"],
        "history": lambda x: [convert_message(msg) for msg in x["history"]],
        "date": lambda x: datetime.now().strftime("%B %d, %Y"),
    }
    | prompt
    | model
    | StrOutputParser()
)

if __name__ == "__main__":
    print("Tell me which subject you'd like to discuss")

    def stream_response(response):
        full_response = ""
        for chunk in response:
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n")
        return full_response

    end_convo = False
    while not end_convo:
        user_message = input(">>> ")
        stream_resp = runnable.stream({"input": user_message})
        full_resp = stream_response(stream_resp)
        if "[[END]]" in full_resp:
            end_convo = True
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(full_resp)
