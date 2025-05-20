from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel
from ...llm.client import model_client


class ResearchState(BaseModel):
    topic: str = ""
    depth: str = "medium"
    results: str = ""


class ResearchFlow(Flow[ResearchState]):
    @start()
    def get_parameters(self):
        # In a real app, this might come from user input
        self.state.topic = "Artificial Intelligence Ethics"
        self.state.depth = "deep"
        return "Parameters set"

    @listen(get_parameters)
    def execute_research(self, _):
        # Create agents
        researcher = Agent(
            llm=model_client,
            role="Research Specialist",
            goal=f"Research {self.state.topic} in {self.state.depth} detail",
            backstory="You are an expert researcher with a talent for finding accurate information.",
        )

        writer = Agent(
            llm=model_client,
            role="Content Writer",
            goal="Transform research into clear, engaging content",
            backstory="You excel at communicating complex ideas clearly and concisely.",
        )

        # Create tasks
        research_task = Task(
            description=f"Research {self.state.topic} with {self.state.depth} analysis",
            expected_output="Comprehensive research notes in markdown format",
            agent=researcher,
        )

        writing_task = Task(
            description=f"Create a summary on {self.state.topic} based on the research",
            expected_output="Well-written article in markdown format",
            agent=writer,
            context=[research_task],
        )

        # Create and run crew
        research_crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,
            verbose=True,
        )

        # Run crew and store result in state
        result = research_crew.kickoff()
        self.state.results = result.raw

        return "Research completed"

    @listen(execute_research)
    def summarize_results(self, _):
        # Access the stored results
        result_length = len(self.state.results)
        return f"Research on {self.state.topic} completed with {result_length} characters of results."
