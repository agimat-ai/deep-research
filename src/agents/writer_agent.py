from agents import Agent
from pydantic import BaseModel, Field

from src.prompts import WRITER_AGENT_INSTRUCTIONS


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="Writer Agent",
    instructions=WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
