from agents import Agent
from pydantic import BaseModel, Field

from src.config import load_settings
from src.prompts import PLANNER_INSTRUCTIONS_TEMPLATE

settings = load_settings()
INSTRUCTIONS = PLANNER_INSTRUCTIONS_TEMPLATE.format(count=settings.planner_search_count)


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")


planner_agent = Agent(
    name="Planner Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
