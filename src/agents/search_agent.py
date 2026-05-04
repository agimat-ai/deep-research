from agents import Agent, ModelSettings, WebSearchTool

from src.prompts import SEARCH_AGENT_INSTRUCTIONS

AGENT_NAME = "Search Agent"

search_agent = Agent(
    name=AGENT_NAME,
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)
