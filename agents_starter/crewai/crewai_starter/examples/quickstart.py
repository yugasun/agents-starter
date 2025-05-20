# Example: Research Crew for market analysis
from crewai import Agent, Crew, Process, Task

from ..utils import print_message
from ..llm.client import model_client


def run() -> None:
    # Create specialized agents
    researcher = Agent(
        llm=model_client,
        role="Market Research Specialist",
        goal="Find comprehensive market data on emerging technologies",
        backstory="You are an expert at discovering market trends and gathering data.",
    )

    analyst = Agent(
        llm=model_client,
        role="Market Analyst",
        goal="Analyze market data and identify key opportunities",
        backstory="You excel at interpreting market data and spotting valuable insights.",
    )

    # Define their tasks
    research_task = Task(
        description="Research the current market landscape for AI-powered healthcare solutions",
        expected_output="Comprehensive market data including key players, market size, and growth trends",
        agent=researcher,
    )

    # analysis_task = Task(
    #     description="Analyze the market data and identify the top 3 investment opportunities",
    #     expected_output="Analysis report with 3 recommended investment opportunities and rationale",
    #     agent=analyst,
    #     context=[research_task],
    # )

    # Create the crew
    market_analysis_crew = Crew(
        agents=[researcher, analyst],
        tasks=[
            research_task,
            # analysis_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    # Run the crew
    result = market_analysis_crew.kickoff()
    print_message(result)
