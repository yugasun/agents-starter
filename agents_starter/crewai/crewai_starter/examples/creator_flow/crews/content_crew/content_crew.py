# src/guide_creator_flow/crews/content_crew/content_crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .....llm.client import model_client


@CrewBase
class ContentCrew:
    """Content writing crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            llm=model_client,
            config=self.agents_config["content_writer"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def content_reviewer(self) -> Agent:
        return Agent(
            llm=model_client,
            config=self.agents_config["content_reviewer"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def write_section_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_section_task"]  # type: ignore[index]
        )

    @task
    def review_section_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_section_task"],  # type: ignore[index]
            context=[self.write_section_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the content writing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
