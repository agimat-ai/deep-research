import asyncio
from collections.abc import AsyncGenerator

from agents import Runner, gen_trace_id, trace

from src.agents.email_agent import email_agent
from src.agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from src.agents.search_agent import search_agent
from src.agents.writer_agent import ReportData, writer_agent

class ResearchManager:

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """Run deep research and stream status updates plus final markdown."""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            trace_url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print(f"View trace: {trace_url}")
            yield f"View trace: {trace_url}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan web searches for the incoming query."""
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Execute all planned searches concurrently."""
        print("Searching...")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results: list[str] = []
        for completed_count, task in enumerate(asyncio.as_completed(tasks), start=1):
            result = await task
            if result is not None:
                results.append(result)
            print(f"Searching... {completed_count}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Run one search task and return a summary, if successful."""
        search_input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                search_input,
            )
            return str(result.final_output)
        except Exception as error:
            print(f"Search failed for '{item.query}': {error}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the final report from aggregated search results."""
        print("Thinking about report...")
        report_input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            report_input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        """Send the final report via the email agent."""
        print("Writing email...")
        await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")