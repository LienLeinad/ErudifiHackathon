from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """You are a world-class instructor for a prestigious university.
Your task is to create a lesson plan appropriate for the level of instruction.
-----
{format_instructions}
"""


class Activity(BaseModel):
    step: int = Field(..., description="Step number")
    title: str = Field(..., description="Title of the activity")
    duration: str = Field(..., description="Duration of the activity")
    description: str = Field(
        ..., description="Details of the activity. Explain what the students will do."
    )


class ReadingMaterial(BaseModel):
    title: str = Field(..., description="Title of the reading material")
    url: str = Field(..., description="URL of the reading material")


class LessonPlan(BaseModel):
    title: str = Field(..., description="Title of the lesson plan")
    objectives: str = Field(
        ..., description="A lengthy description for the objectives for the lesson"
    )
    prerequisites: List[str] = Field(..., description="Prerequisites for the lesson")
    materials: List[str] = Field(
        ..., description="List of materials needed to conduct the lesson."
    )
    activities: List[Activity] = Field(
        ...,
        description="Step-by-step activities for the whole lesson. Add as many activities as needed to complete the lesson.",
    )
    assessment: List[Activity] = Field(
        ..., description="Activities to assess the students' learning."
    )
    reading_materials: List[ReadingMaterial] = Field(
        ..., description="Reading materials for the students to read before the lesson."
    )


output_parser = PydanticOutputParser(pydantic_object=LessonPlan)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "Lesson Plan Title: {title}\nObjectives: {objectives}\nInstruction Level: {level}\nApproach: {approach}",
        ),
    ]
)
prompt = prompt.partial(format_instructions=output_parser.get_format_instructions())
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
runnable = prompt | llm | output_parser


if __name__ == "__main__":

    def lesson_plan_printer(lesson_plan: LessonPlan):
        print(f"Title: {lesson_plan.title}")
        print(f"Objectives: {lesson_plan.objectives}")
        print(f"Materials: {lesson_plan.materials}")
        print(f"Procedure: {lesson_plan.activities}")
        print(f"Assessment: {lesson_plan.assessment}")
        print(f"Additional Resources: {lesson_plan.reading_materials}")

    resp = runnable.invoke(
        {
            "title": "A developer primer into Langchain",
            "level": "Beginner",
            "approach": "Hands-on Workshop",
        }
    )
    lesson_plan_printer(resp)
