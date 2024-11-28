from enum import Enum

import streamlit as st
import streamlit_pydantic as sp
from pydantic import BaseModel, Field

from models.lesson_planner import LessonPlan, runnable

HELPTEXT = """# 👨‍🏫 Alyssa (Lesson Planner)

This is a tool to help you create a lesson plan for your class. It will ask you for the title of the lesson plan, the instruction level, and the approach for the lesson plan. It will then generate a lesson plan for you.

## Instructions
- Title: Provide a descriptive title for your lesson plan (ie. A developer primer into Langchain)
- Objectives: Provide a description of your objectives for the students (ie. At the end of this lesson, the students should be able to...)
- Instruction Level: Provide the level of instruction for the lesson plan. You can choose from the drop-down.
- Approach: Provide the approach for the lesson plan. You can choose from the drop-down.

Built with ❤️ by Erudifi EPD
"""


class LessonPlanLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class LessonPlanApproach(str, Enum):
    WORKSHOP = "Hands-on Workshop"
    LECTURE = "Lecture"
    DISCUSSION = "Discussion"


class LessonPlanInput(BaseModel):
    title: str = Field(..., description="Title of the lesson plan")
    objectives: str = Field(..., description="A description for the objectives for the lesson")
    level: LessonPlanLevel = Field(..., description="Instruction level")
    approach: LessonPlanApproach = Field(..., description="Approach for the lesson plan")


st.title("👨‍🏫 Lesson Planner")

with st.sidebar:
    st.markdown(HELPTEXT)

lessonplan_input = sp.pydantic_form(key="lesson_plan", model=LessonPlanInput)
if lessonplan_input:
    resp: LessonPlan = runnable.invoke({
        "title": lessonplan_input.title,
        "objectives": lessonplan_input.objectives,
        "level": lessonplan_input.level,
        "approach": lessonplan_input.approach,
    })

    st.header(resp.title)
    st.markdown(resp.objectives)

    prerequisites, activities, assessment, resources = st.tabs(["📚 Prerequisites", "👨‍💻 Activities", "🎯 Assessment", "📗 Resources"])

    with prerequisites:
        st.subheader("Prerequisites")
        for prerequisite in resp.prerequisites:
            st.markdown(prerequisite)

        st.subheader("Materials")
        for material in resp.materials:
            st.markdown(material)

    with activities:
        for activity in resp.activities:
            st.subheader(f"{activity.title}")
            st.markdown(f"**Duration:** {activity.duration}")
            st.markdown(activity.description)

    with assessment:
        for activity in resp.assessment:
            st.subheader(f"{activity.title}")
            st.markdown(f"**Duration:** {activity.duration}")
            st.markdown(activity.description)

    with resources:
        for resource in resp.reading_materials:
            st.subheader(resource.title)
            st.markdown(resource.url)