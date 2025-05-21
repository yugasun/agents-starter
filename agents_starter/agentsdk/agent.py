from agents import Agent

from .llm.client import model_client


class AgentSDK(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model_client
